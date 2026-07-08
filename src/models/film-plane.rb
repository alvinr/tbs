# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane (Option A)", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Sketchfab metadata — fill-only-if-blank; never overwrites existing values ──
model.name = "TBS-001 Film Plane Model" if model.name.to_s.strip.empty?
model.description = "The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This has a **view-camera-style moveable film plane** \u2014 a mechanism with **four independently actuated corners**" if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 Film Plane Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This has a **view-camera-style moveable film plane** \u2014 a mechanism with **four independently actuated corners**") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "bb5394a8983a491fa541088b901c24f8") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Corner Mechanism") unless model.layers["Corner Mechanism"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("IBC Cantilever") unless model.layers["IBC Cantilever"]
  model.layers.add("Corner Detail") unless model.layers["Corner Detail"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.22
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.08
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Pinhole Wall (context)
  grp = ents.add_group
  grp.name = "Pinhole Wall (context)"
  face = grp.entities.add_face([-40.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-40.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole Wall (context)"] || model.materials.add("Pinhole Wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ Near-wall equipment (ghost) ═══
  defn = model.definitions.add("Near-wall equipment (ghost)")
  ents = defn.entities
  # Electrical Panel (EP) [ghost]
  grp = ents.add_group
  grp.name = "Electrical Panel (EP) [ghost]"
  face = grp.entities.add_face([1829.mm,0.mm,1150.mm], [2129.mm,0.mm,1150.mm], [2129.mm,160.mm,1150.mm], [1829.mm,160.mm,1150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(410.mm)
  mat = model.materials["Electrical Panel (EP) [ghost]"] || model.materials.add("Electrical Panel (EP) [ghost]")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 0.28
  grp.material = mat

  # Battery 1 [ghost]
  grp = ents.add_group
  grp.name = "Battery 1 [ghost]"
  face = grp.entities.add_face([1829.mm,0.mm,160.mm], [1984.mm,0.mm,160.mm], [1984.mm,172.mm,160.mm], [1829.mm,172.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 1 [ghost]"] || model.materials.add("Battery 1 [ghost]")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Battery 2 [ghost]
  grp = ents.add_group
  grp.name = "Battery 2 [ghost]"
  face = grp.entities.add_face([2004.mm,0.mm,160.mm], [2159.mm,0.mm,160.mm], [2159.mm,172.mm,160.mm], [2004.mm,172.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 1 [ghost]"] || model.materials.add("Battery 1 [ghost]")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Power panel (interior face) [ghost]
  grp = ents.add_group
  grp.name = "Power panel (interior face) [ghost]"
  face = grp.entities.add_face([1250.mm,0.mm,1830.mm], [1590.mm,0.mm,1830.mm], [1590.mm,20.mm,1830.mm], [1250.mm,20.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Electrical Panel (EP) [ghost]"] || model.materials.add("Electrical Panel (EP) [ghost]")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 0.28
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Near-wall equipment (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ Processing Tray ═══
  defn = model.definitions.add("Processing Tray")
  ents = defn.entities
  # Tray Shim Base
  grp = ents.add_group
  grp.name = "Tray Shim Base"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Tray Shim Base"] || model.materials.add("Tray Shim Base")
  mat.color = Sketchup::Color.new(216, 208, 188)
  mat.alpha = 0.9
  grp.material = mat

  # Processing Tray Floor A
  grp = ents.add_group
  grp.name = "Processing Tray Floor A"
  ge = grp.entities
  f = ge.add_face([170.mm,80.mm,42.295.mm], [4629.mm,80.mm,20.mm], [4629.mm,2280.mm,31.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Processing Tray Floor B
  grp = ents.add_group
  grp.name = "Processing Tray Floor B"
  ge = grp.entities
  f = ge.add_face([170.mm,80.mm,42.295.mm], [4629.mm,2280.mm,31.mm], [170.mm,2280.mm,53.295.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,31.1475.mm], [4629.mm,80.mm,31.1475.mm], [4629.mm,82.mm,31.1475.mm], [170.mm,82.mm,31.1475.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2278.mm,42.1475.mm], [4629.mm,2278.mm,42.1475.mm], [4629.mm,2280.mm,42.1475.mm], [170.mm,2280.mm,42.1475.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,47.795.mm], [172.mm,80.mm,47.795.mm], [172.mm,2280.mm,47.795.mm], [170.mm,2280.mm,47.795.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,25.5.mm], [4629.mm,80.mm,25.5.mm], [4629.mm,2280.mm,25.5.mm], [4627.mm,2280.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Chemistry Bath
  grp = ents.add_group
  grp.name = "Chemistry Bath"
  face = grp.entities.add_face([172.mm,82.mm,36.6475.mm], [4627.mm,82.mm,36.6475.mm], [4627.mm,2278.mm,36.6475.mm], [172.mm,2278.mm,36.6475.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Chemistry Bath"] || model.materials.add("Chemistry Bath")
  mat.color = Sketchup::Color.new(46, 111, 160)
  mat.alpha = 0.45
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Corner Mechanism ═══
  defn = model.definitions.add("Corner Mechanism")
  ents = defn.entities
  # HGR20 Rail TL
  grp = ents.add_group
  grp.name = "HGR20 Rail TL"
  face = grp.entities.add_face([138.mm,0.mm,2280.mm], [162.mm,0.mm,2280.mm], [162.mm,2362.mm,2280.mm], [138.mm,2362.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TL
  grp = ents.add_group
  grp.name = "Leadscrew TL"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([184.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail TR
  grp = ents.add_group
  grp.name = "HGR20 Rail TR"
  face = grp.entities.add_face([4637.mm,0.mm,2280.mm], [4661.mm,0.mm,2280.mm], [4661.mm,2362.mm,2280.mm], [4637.mm,2362.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TR
  grp = ents.add_group
  grp.name = "Leadscrew TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BL
  grp = ents.add_group
  grp.name = "HGR20 Rail BL"
  face = grp.entities.add_face([138.mm,0.mm,152.mm], [162.mm,0.mm,152.mm], [162.mm,2362.mm,152.mm], [138.mm,2362.mm,152.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BL
  grp = ents.add_group
  grp.name = "Leadscrew BL"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([184.mm,100.mm,160.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BR
  grp = ents.add_group
  grp.name = "HGR20 Rail BR"
  face = grp.entities.add_face([4637.mm,0.mm,152.mm], [4661.mm,0.mm,152.mm], [4661.mm,2362.mm,152.mm], [4637.mm,2362.mm,152.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BR
  grp = ents.add_group
  grp.name = "Leadscrew BR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,160.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TL near
  grp = ents.add_group
  grp.name = "Saddle back-plate TL near"
  face = grp.entities.add_face([75.mm,0.mm,2213.mm], [225.mm,0.mm,2213.mm], [225.mm,8.mm,2213.mm], [75.mm,8.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TL near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TL near"
  face = grp.entities.add_face([75.mm,-48.mm,2213.mm], [225.mm,-48.mm,2213.mm], [225.mm,-40.mm,2213.mm], [75.mm,-40.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TL near
  grp = ents.add_group
  grp.name = "Saddle seat TL near"
  face = grp.entities.add_face([126.mm,0.mm,2278.mm], [174.mm,0.mm,2278.mm], [174.mm,110.mm,2278.mm], [126.mm,110.mm,2278.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TL near
  grp = ents.add_group
  grp.name = "Saddle gusset TL near"
  ge = grp.entities
  f = ge.add_face([150.mm,110.mm,2278.mm], [150.mm,0.mm,2278.mm], [150.mm,0.mm,2158.mm])
  f.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL near
  grp = ents.add_group
  grp.name = "Thumb screw TL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,25.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL near
  grp = ents.add_group
  grp.name = "Thumb screw TL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,85.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TL far
  grp = ents.add_group
  grp.name = "Saddle back-plate TL far"
  face = grp.entities.add_face([75.mm,2354.mm,2213.mm], [225.mm,2354.mm,2213.mm], [225.mm,2362.mm,2213.mm], [75.mm,2362.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TL far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TL far"
  face = grp.entities.add_face([75.mm,2402.mm,2213.mm], [225.mm,2402.mm,2213.mm], [225.mm,2410.mm,2213.mm], [75.mm,2410.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TL far
  grp = ents.add_group
  grp.name = "Saddle seat TL far"
  face = grp.entities.add_face([126.mm,2252.mm,2278.mm], [174.mm,2252.mm,2278.mm], [174.mm,2362.mm,2278.mm], [126.mm,2362.mm,2278.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TL far
  grp = ents.add_group
  grp.name = "Saddle gusset TL far"
  ge = grp.entities
  f = ge.add_face([150.mm,2252.mm,2278.mm], [150.mm,2362.mm,2278.mm], [150.mm,2362.mm,2158.mm])
  f.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL far
  grp = ents.add_group
  grp.name = "Thumb screw TL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2277.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL far
  grp = ents.add_group
  grp.name = "Thumb screw TL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2337.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TR near
  grp = ents.add_group
  grp.name = "Saddle back-plate TR near"
  face = grp.entities.add_face([4574.mm,0.mm,2213.mm], [4724.mm,0.mm,2213.mm], [4724.mm,8.mm,2213.mm], [4574.mm,8.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TR near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR near"
  face = grp.entities.add_face([4574.mm,-48.mm,2213.mm], [4724.mm,-48.mm,2213.mm], [4724.mm,-40.mm,2213.mm], [4574.mm,-40.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TR near
  grp = ents.add_group
  grp.name = "Saddle seat TR near"
  face = grp.entities.add_face([4625.mm,0.mm,2278.mm], [4673.mm,0.mm,2278.mm], [4673.mm,110.mm,2278.mm], [4625.mm,110.mm,2278.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TR near
  grp = ents.add_group
  grp.name = "Saddle gusset TR near"
  ge = grp.entities
  f = ge.add_face([4649.mm,110.mm,2278.mm], [4649.mm,0.mm,2278.mm], [4649.mm,0.mm,2158.mm])
  f.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TR far
  grp = ents.add_group
  grp.name = "Saddle back-plate TR far"
  face = grp.entities.add_face([4574.mm,2354.mm,2213.mm], [4724.mm,2354.mm,2213.mm], [4724.mm,2362.mm,2213.mm], [4574.mm,2362.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TR far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR far"
  face = grp.entities.add_face([4574.mm,2402.mm,2213.mm], [4724.mm,2402.mm,2213.mm], [4724.mm,2410.mm,2213.mm], [4574.mm,2410.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TR far
  grp = ents.add_group
  grp.name = "Saddle seat TR far"
  face = grp.entities.add_face([4625.mm,2252.mm,2278.mm], [4673.mm,2252.mm,2278.mm], [4673.mm,2362.mm,2278.mm], [4625.mm,2362.mm,2278.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TR far
  grp = ents.add_group
  grp.name = "Saddle gusset TR far"
  ge = grp.entities
  f = ge.add_face([4649.mm,2252.mm,2278.mm], [4649.mm,2362.mm,2278.mm], [4649.mm,2362.mm,2158.mm])
  f.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate BL near
  grp = ents.add_group
  grp.name = "Saddle back-plate BL near"
  face = grp.entities.add_face([75.mm,0.mm,85.mm], [225.mm,0.mm,85.mm], [225.mm,8.mm,85.mm], [75.mm,8.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate BL near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BL near"
  face = grp.entities.add_face([75.mm,-48.mm,85.mm], [225.mm,-48.mm,85.mm], [225.mm,-40.mm,85.mm], [75.mm,-40.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat BL near
  grp = ents.add_group
  grp.name = "Saddle seat BL near"
  face = grp.entities.add_face([126.mm,0.mm,150.mm], [174.mm,0.mm,150.mm], [174.mm,110.mm,150.mm], [126.mm,110.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset BL near
  grp = ents.add_group
  grp.name = "Saddle gusset BL near"
  ge = grp.entities
  f = ge.add_face([150.mm,110.mm,150.mm], [150.mm,0.mm,150.mm], [150.mm,0.mm,30.mm])
  f.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL near
  grp = ents.add_group
  grp.name = "Thumb screw BL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,25.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL near
  grp = ents.add_group
  grp.name = "Thumb screw BL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,85.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate BL far
  grp = ents.add_group
  grp.name = "Saddle back-plate BL far"
  face = grp.entities.add_face([75.mm,2354.mm,85.mm], [225.mm,2354.mm,85.mm], [225.mm,2362.mm,85.mm], [75.mm,2362.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate BL far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BL far"
  face = grp.entities.add_face([75.mm,2402.mm,85.mm], [225.mm,2402.mm,85.mm], [225.mm,2410.mm,85.mm], [75.mm,2410.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat BL far
  grp = ents.add_group
  grp.name = "Saddle seat BL far"
  face = grp.entities.add_face([126.mm,2252.mm,150.mm], [174.mm,2252.mm,150.mm], [174.mm,2362.mm,150.mm], [126.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset BL far
  grp = ents.add_group
  grp.name = "Saddle gusset BL far"
  ge = grp.entities
  f = ge.add_face([150.mm,2252.mm,150.mm], [150.mm,2362.mm,150.mm], [150.mm,2362.mm,30.mm])
  f.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL far
  grp = ents.add_group
  grp.name = "Thumb screw BL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2277.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL far
  grp = ents.add_group
  grp.name = "Thumb screw BL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2337.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,10.mm,58.mm], [4574.mm,10.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,58.mm], [4724.mm,-50.mm,58.mm], [4724.mm,-40.mm,58.mm], [4574.mm,-40.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,55.mm,58.mm], [4574.mm,55.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,148.mm], [4679.mm,0.mm,148.mm], [4679.mm,55.mm,148.mm], [4619.mm,55.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z188"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z188"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,58.mm], [4724.mm,2352.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,58.mm], [4724.mm,2402.mm,58.mm], [4724.mm,2412.mm,58.mm], [4574.mm,2412.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(177.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,58.mm], [4724.mm,2307.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,148.mm], [4679.mm,2307.mm,148.mm], [4679.mm,2362.mm,148.mm], [4619.mm,2362.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z188"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z188
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z188"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,188.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Mechanism"
  inst.layer = model.layers["Corner Mechanism"]

  # ═══ Walkways ═══
  defn = model.definitions.add("Walkways")
  ents = defn.entities
  # Walkway Near (left section)
  grp = ents.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([470.mm,8.mm,115.mm], [1055.mm,8.mm,115.mm], [1055.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1055.mm,10.mm,115.mm], [2169.mm,10.mm,115.mm], [2169.mm,500.mm,115.mm], [1055.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2169.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [2169.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [470.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out (drum exit)
  grp = ents.add_group
  grp.name = "Walkway Left punch-out (drum exit)"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 plate"
  face = grp.entities.add_face([638.mm,0.mm,0.mm], [758.mm,0.mm,0.mm], [758.mm,8.mm,0.mm], [638.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,8.mm,0.mm], [2466.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2526.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 arm"
  face = grp.entities.add_face([2522.mm,8.mm,105.mm], [2530.mm,8.mm,105.mm], [2530.mm,300.mm,105.mm], [2522.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,8.mm,0.mm], [2522.mm,8.mm,105.mm], [2522.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,8.mm,0.mm], [2923.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 arm"
  face = grp.entities.add_face([2979.mm,8.mm,105.mm], [2987.mm,8.mm,105.mm], [2987.mm,300.mm,105.mm], [2979.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,8.mm,0.mm], [2979.mm,8.mm,105.mm], [2979.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
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
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,220.mm,0.mm], [165.mm,220.mm,0.mm], [165.mm,280.mm,0.mm], [115.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.mm,230.mm,75.mm], [470.mm,230.mm,75.mm], [470.mm,270.mm,75.mm], [165.mm,270.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,770.mm,0.mm], [165.mm,770.mm,0.mm], [165.mm,830.mm,0.mm], [115.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.mm,770.mm,75.mm], [770.mm,770.mm,75.mm], [770.mm,830.mm,75.mm], [165.mm,830.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1150.mm,0.mm], [165.mm,1150.mm,0.mm], [165.mm,1210.mm,0.mm], [115.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.mm,1150.mm,75.mm], [770.mm,1150.mm,75.mm], [770.mm,1210.mm,75.mm], [165.mm,1210.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1530.mm,0.mm], [165.mm,1530.mm,0.mm], [165.mm,1590.mm,0.mm], [115.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.mm,1530.mm,75.mm], [770.mm,1530.mm,75.mm], [770.mm,1590.mm,75.mm], [165.mm,1590.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,2080.mm,0.mm], [165.mm,2080.mm,0.mm], [165.mm,2140.mm,0.mm], [115.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.mm,2090.mm,75.mm], [470.mm,2090.mm,75.mm], [470.mm,2130.mm,75.mm], [165.mm,2130.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkways"
  inst.layer = model.layers["Walkways"]

  # ═══ IBC Cantilever Arms ═══
  defn = model.definitions.add("IBC Cantilever Arms")
  ents = defn.entities
  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,70.mm], [4654.mm,1046.mm,70.mm], [4654.mm,1086.mm,70.mm], [4329.mm,1086.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4369.mm,1046.mm,95.mm], [4589.mm,1046.mm,95.mm], [4589.mm,1086.mm,95.mm], [4369.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1086.mm,95.mm], [4629.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,45.mm], [4708.mm,1038.mm,45.mm], [4708.mm,1046.mm,45.mm], [4650.mm,1046.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1086
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1086"
  face = grp.entities.add_face([4650.mm,1086.mm,45.mm], [4708.mm,1086.mm,45.mm], [4708.mm,1094.mm,45.mm], [4650.mm,1094.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,70.mm], [4654.mm,1266.mm,70.mm], [4654.mm,1306.mm,70.mm], [4329.mm,1306.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4369.mm,1266.mm,95.mm], [4589.mm,1266.mm,95.mm], [4589.mm,1306.mm,95.mm], [4369.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4654.mm,1266.mm,95.mm], [4654.mm,1306.mm,95.mm], [4629.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4650.mm,1258.mm,45.mm], [4708.mm,1258.mm,45.mm], [4708.mm,1266.mm,45.mm], [4650.mm,1266.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1306
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1306"
  face = grp.entities.add_face([4650.mm,1306.mm,45.mm], [4708.mm,1306.mm,45.mm], [4708.mm,1314.mm,45.mm], [4650.mm,1314.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
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
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Cantilever Arms"
  inst.layer = model.layers["IBC Cantilever"]

  # ═══ Corner Detail (TR) ═══
  defn = model.definitions.add("Corner Detail (TR)")
  ents = defn.entities
  # Detail Rail TR
  grp = ents.add_group
  grp.name = "Detail Rail TR"
  face = grp.entities.add_face([2887.mm,100.mm,2280.mm], [2911.mm,100.mm,2280.mm], [2911.mm,2300.mm,2280.mm], [2887.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Leadscrew TR
  grp = ents.add_group
  grp.name = "Detail Leadscrew TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([2933.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Detail (TR)"
  inst.layer = model.layers["Corner Detail"]

  # ═══ Corner Detail Swing (TR) ═══
  defn = model.definitions.add("Corner Detail Swing (TR)")
  ents = defn.entities
  # Swing Rail TR
  grp = ents.add_group
  grp.name = "Swing Rail TR"
  face = grp.entities.add_face([1137.mm,100.mm,2280.mm], [1161.mm,100.mm,2280.mm], [1161.mm,2300.mm,2280.mm], [1137.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Leadscrew TR
  grp = ents.add_group
  grp.name = "Swing Leadscrew TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([1183.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Detail Swing (TR)"
  inst.layer = model.layers["Corner Detail"]

  # ═══ Corner Detail Static (TR) ═══
  defn = model.definitions.add("Corner Detail Static (TR)")
  ents = defn.entities
  # Static Rail TR
  grp = ents.add_group
  grp.name = "Static Rail TR"
  face = grp.entities.add_face([-1488.mm,100.mm,2280.mm], [-1464.mm,100.mm,2280.mm], [-1464.mm,2300.mm,2280.mm], [-1488.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Static Leadscrew TR
  grp = ents.add_group
  grp.name = "Static Leadscrew TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([-1442.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Static Carriage TR
  grp = ents.add_group
  grp.name = "Static Carriage TR"
  face = grp.entities.add_face([-1502.mm,1379.7039226776096.mm,2270.mm], [-1450.mm,1379.7039226776096.mm,2270.mm], [-1450.mm,1443.7039226776096.mm,2270.mm], [-1502.mm,1443.7039226776096.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Static Drive Nut TR
  grp = ents.add_group
  grp.name = "Static Drive Nut TR"
  face = grp.entities.add_face([-1456.mm,1397.7039226776096.mm,2276.mm], [-1428.mm,1397.7039226776096.mm,2276.mm], [-1428.mm,1425.7039226776096.mm,2276.mm], [-1456.mm,1425.7039226776096.mm,2276.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Static X cross-slide TR (SWING)
  grp = ents.add_group
  grp.name = "Static X cross-slide TR (SWING)"
  face = grp.entities.add_face([-1492.mm,1395.7039226776096.mm,2294.mm], [-1442.463161939676.mm,1395.7039226776096.mm,2294.mm], [-1442.463161939676.mm,1427.7039226776096.mm,2294.mm], [-1492.mm,1427.7039226776096.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Detail X cross-slide TR (SWING)"] || model.materials.add("Detail X cross-slide TR (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # Static X slider TR
  grp = ents.add_group
  grp.name = "Static X slider TR"
  face = grp.entities.add_face([-1474.463161939676.mm,1391.7039226776096.mm,2292.mm], [-1442.463161939676.mm,1391.7039226776096.mm,2292.mm], [-1442.463161939676.mm,1431.7039226776096.mm,2292.mm], [-1474.463161939676.mm,1431.7039226776096.mm,2292.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Static Z cross-slide TR (TILT)
  grp = ents.add_group
  grp.name = "Static Z cross-slide TR (TILT)"
  face = grp.entities.add_face([-1467.463161939676.mm,1396.7039226776096.mm,2207.8329485162067.mm], [-1449.463161939676.mm,1396.7039226776096.mm,2207.8329485162067.mm], [-1449.463161939676.mm,1426.7039226776096.mm,2207.8329485162067.mm], [-1467.463161939676.mm,1426.7039226776096.mm,2207.8329485162067.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(96.16705148379333.mm)
  mat = model.materials["Detail Z cross-slide TR (TILT)"] || model.materials.add("Detail Z cross-slide TR (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Static Z slider TR
  grp = ents.add_group
  grp.name = "Static Z slider TR"
  face = grp.entities.add_face([-1471.463161939676.mm,1393.7039226776096.mm,2207.8329485162067.mm], [-1445.463161939676.mm,1393.7039226776096.mm,2207.8329485162067.mm], [-1445.463161939676.mm,1429.7039226776096.mm,2207.8329485162067.mm], [-1471.463161939676.mm,1429.7039226776096.mm,2207.8329485162067.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Static Rod-End TR
  grp = ents.add_group
  grp.name = "Static Rod-End TR"
  face = grp.entities.add_face([-1475.463161939676.mm,1394.7039226776096.mm,2206.8329485162067.mm], [-1441.463161939676.mm,1394.7039226776096.mm,2206.8329485162067.mm], [-1441.463161939676.mm,1428.7039226776096.mm,2206.8329485162067.mm], [-1475.463161939676.mm,1428.7039226776096.mm,2206.8329485162067.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Static Flat-corner ghost TR
  grp = ents.add_group
  grp.name = "Static Flat-corner ghost TR"
  face = grp.entities.add_face([-1489.mm,1398.7039226776096.mm,2275.mm], [-1463.mm,1398.7039226776096.mm,2275.mm], [-1463.mm,1424.7039226776096.mm,2275.mm], [-1489.mm,1424.7039226776096.mm,2275.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Flat-corner ghost TR"] || model.materials.add("Detail Flat-corner ghost TR")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Detail Static (TR)"
  inst.layer = model.layers["Corner Detail"]

  # ═══ Rotate Rail (TR) ═══
  defn = model.definitions.add("Rotate Rail (TR)")
  ents = defn.entities
  # Rotate Rail TR
  grp = ents.add_group
  grp.name = "Rotate Rail TR"
  face = grp.entities.add_face([4637.mm,100.mm,2280.mm], [4661.mm,100.mm,2280.mm], [4661.mm,2300.mm,2280.mm], [4637.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Rotate Carriage TR
  grp = ents.add_group
  grp.name = "Rotate Carriage TR"
  face = grp.entities.add_face([4623.mm,1149.mm,2270.mm], [4675.mm,1149.mm,2270.mm], [4675.mm,1213.mm,2270.mm], [4623.mm,1213.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rotate Rod-End TR
  grp = ents.add_group
  grp.name = "Rotate Rod-End TR"
  face = grp.entities.add_face([4633.mm,1165.mm,2272.mm], [4665.mm,1165.mm,2272.mm], [4665.mm,1197.mm,2272.mm], [4633.mm,1197.mm,2272.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Rotate Rail (TR)"
  inst.layer = model.layers["Corner Detail"]


# ── Film Plane (Dynamic Component — click to swing: left forward / right back) ──

# ═══ Film Plane — DYNAMIC COMPONENT (click to swing: left forward / right back) ═══
fp_defn = model.definitions.add("Film Plane")
ents = fp_defn.entities
  # Film Plane Screen (muslin)
  grp = ents.add_group
  grp.name = "Film Plane Screen (muslin)"
  face = grp.entities.add_face([-2249.5.mm,-6.mm,-1064.mm], [2249.5.mm,-6.mm,-1064.mm], [2249.5.mm,6.mm,-1064.mm], [-2249.5.mm,6.mm,-1064.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2128.mm)
  mat = model.materials["Film Plane Screen (muslin)"] || model.materials.add("Film Plane Screen (muslin)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.3
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  ge = grp.entities
  vec = Geom::Vector3d.new(4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([-2249.5.mm,0.mm,1064.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Bottom
  grp = ents.add_group
  grp.name = "FP Frame Bottom"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,-1064.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2128.mm)
  circle = ge.add_circle([-2249.5.mm,0.mm,1064.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2128.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,1064.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TL (HGH20CA)"
  face = grp.entities.add_face([-2275.5.mm,-32.mm,1052.mm], [-2223.5.mm,-32.mm,1052.mm], [-2223.5.mm,32.mm,1052.mm], [-2275.5.mm,32.mm,1052.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TL
  grp = ents.add_group
  grp.name = "Drive Nut TL"
  face = grp.entities.add_face([-2229.5.mm,-14.mm,1051.mm], [-2201.5.mm,-14.mm,1051.mm], [-2201.5.mm,14.mm,1051.mm], [-2229.5.mm,14.mm,1051.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TL
  grp = ents.add_group
  grp.name = "Rod-End TL"
  face = grp.entities.add_face([-2265.5.mm,-16.mm,1048.mm], [-2233.5.mm,-16.mm,1048.mm], [-2233.5.mm,16.mm,1048.mm], [-2265.5.mm,16.mm,1048.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TR (HGH20CA)"
  face = grp.entities.add_face([2223.5.mm,-32.mm,1052.mm], [2275.5.mm,-32.mm,1052.mm], [2275.5.mm,32.mm,1052.mm], [2223.5.mm,32.mm,1052.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TR
  grp = ents.add_group
  grp.name = "Drive Nut TR"
  face = grp.entities.add_face([2269.5.mm,-14.mm,1051.mm], [2297.5.mm,-14.mm,1051.mm], [2297.5.mm,14.mm,1051.mm], [2269.5.mm,14.mm,1051.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TR
  grp = ents.add_group
  grp.name = "Rod-End TR"
  face = grp.entities.add_face([2233.5.mm,-16.mm,1048.mm], [2265.5.mm,-16.mm,1048.mm], [2265.5.mm,16.mm,1048.mm], [2233.5.mm,16.mm,1048.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BL (HGH20CA)"
  face = grp.entities.add_face([-2275.5.mm,-32.mm,-1076.mm], [-2223.5.mm,-32.mm,-1076.mm], [-2223.5.mm,32.mm,-1076.mm], [-2275.5.mm,32.mm,-1076.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BL
  grp = ents.add_group
  grp.name = "Drive Nut BL"
  face = grp.entities.add_face([-2229.5.mm,-14.mm,-1077.mm], [-2201.5.mm,-14.mm,-1077.mm], [-2201.5.mm,14.mm,-1077.mm], [-2229.5.mm,14.mm,-1077.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BL
  grp = ents.add_group
  grp.name = "Rod-End BL"
  face = grp.entities.add_face([-2265.5.mm,-16.mm,-1080.mm], [-2233.5.mm,-16.mm,-1080.mm], [-2233.5.mm,16.mm,-1080.mm], [-2265.5.mm,16.mm,-1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BR (HGH20CA)"
  face = grp.entities.add_face([2223.5.mm,-32.mm,-1076.mm], [2275.5.mm,-32.mm,-1076.mm], [2275.5.mm,32.mm,-1076.mm], [2223.5.mm,32.mm,-1076.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BR
  grp = ents.add_group
  grp.name = "Drive Nut BR"
  face = grp.entities.add_face([2269.5.mm,-14.mm,-1077.mm], [2297.5.mm,-14.mm,-1077.mm], [2297.5.mm,14.mm,-1077.mm], [2269.5.mm,14.mm,-1077.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BR
  grp = ents.add_group
  grp.name = "Rod-End BR"
  face = grp.entities.add_face([2233.5.mm,-16.mm,-1080.mm], [2265.5.mm,-16.mm,-1080.mm], [2265.5.mm,16.mm,-1080.mm], [2233.5.mm,16.mm,-1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([2399.5.mm, 1181.mm, 1224.mm]))
fp_inst.name = "Film Plane"
fp_inst.layer = model.layers["Film Plane"]
fda = "dynamic_attributes"
[fp_defn, fp_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlane")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "pose", 0.0)
  e.set_attribute(fda, "rotz", 0.0)
end
fp_inst.set_attribute(fda, "_pose_access", "VIEW")
fp_inst.set_attribute(fda, "_pose_label", "Pose (0 flat / 1 swung)")
fp_inst.set_attribute(fda, "_rotz_formula", "15.0*pose")
fp_inst.set_attribute(fda, "onclick", 'ANIMATE("pose", 0, 1)')
fp_inst.set_attribute(fda, "_onclick_access", "NONE")


# ── Corner Slide TR (Dynamic Component — click: carriage slides along the rail) ──

# ═══ Corner Slide TR — DYNAMIC COMPONENT (click: carriage slides along the rail) ═══
cd_defn = model.definitions.add("Corner Slide TR")
ents = cd_defn.entities
  # Detail Carriage TR
  grp = ents.add_group
  grp.name = "Detail Carriage TR"
  face = grp.entities.add_face([2873.mm,1379.7039226776096.mm,2270.mm], [2925.mm,1379.7039226776096.mm,2270.mm], [2925.mm,1443.7039226776096.mm,2270.mm], [2873.mm,1443.7039226776096.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Drive Nut TR
  grp = ents.add_group
  grp.name = "Detail Drive Nut TR"
  face = grp.entities.add_face([2919.mm,1397.7039226776096.mm,2276.mm], [2947.mm,1397.7039226776096.mm,2276.mm], [2947.mm,1425.7039226776096.mm,2276.mm], [2919.mm,1425.7039226776096.mm,2276.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail X cross-slide TR (SWING)
  grp = ents.add_group
  grp.name = "Detail X cross-slide TR (SWING)"
  face = grp.entities.add_face([2883.mm,1395.7039226776096.mm,2294.mm], [2932.536838060324.mm,1395.7039226776096.mm,2294.mm], [2932.536838060324.mm,1427.7039226776096.mm,2294.mm], [2883.mm,1427.7039226776096.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Detail X cross-slide TR (SWING)"] || model.materials.add("Detail X cross-slide TR (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # Detail X slider TR
  grp = ents.add_group
  grp.name = "Detail X slider TR"
  face = grp.entities.add_face([2900.536838060324.mm,1391.7039226776096.mm,2292.mm], [2932.536838060324.mm,1391.7039226776096.mm,2292.mm], [2932.536838060324.mm,1431.7039226776096.mm,2292.mm], [2900.536838060324.mm,1431.7039226776096.mm,2292.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Z cross-slide TR (TILT)
  grp = ents.add_group
  grp.name = "Detail Z cross-slide TR (TILT)"
  face = grp.entities.add_face([2907.536838060324.mm,1396.7039226776096.mm,2207.8329485162067.mm], [2925.536838060324.mm,1396.7039226776096.mm,2207.8329485162067.mm], [2925.536838060324.mm,1426.7039226776096.mm,2207.8329485162067.mm], [2907.536838060324.mm,1426.7039226776096.mm,2207.8329485162067.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(96.16705148379333.mm)
  mat = model.materials["Detail Z cross-slide TR (TILT)"] || model.materials.add("Detail Z cross-slide TR (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Z slider TR
  grp = ents.add_group
  grp.name = "Detail Z slider TR"
  face = grp.entities.add_face([2903.536838060324.mm,1393.7039226776096.mm,2207.8329485162067.mm], [2929.536838060324.mm,1393.7039226776096.mm,2207.8329485162067.mm], [2929.536838060324.mm,1429.7039226776096.mm,2207.8329485162067.mm], [2903.536838060324.mm,1429.7039226776096.mm,2207.8329485162067.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Rod-End TR
  grp = ents.add_group
  grp.name = "Detail Rod-End TR"
  face = grp.entities.add_face([2899.536838060324.mm,1394.7039226776096.mm,2206.8329485162067.mm], [2933.536838060324.mm,1394.7039226776096.mm,2206.8329485162067.mm], [2933.536838060324.mm,1428.7039226776096.mm,2206.8329485162067.mm], [2899.536838060324.mm,1428.7039226776096.mm,2206.8329485162067.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Flat-corner ghost TR
  grp = ents.add_group
  grp.name = "Detail Flat-corner ghost TR"
  face = grp.entities.add_face([2886.mm,1398.7039226776096.mm,2275.mm], [2912.mm,1398.7039226776096.mm,2275.mm], [2912.mm,1424.7039226776096.mm,2275.mm], [2886.mm,1424.7039226776096.mm,2275.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Flat-corner ghost TR"] || model.materials.add("Detail Flat-corner ghost TR")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

cd_inst = entities.add_instance(cd_defn, Geom::Transformation.new)
cd_inst.name = "Corner Slide TR"
cd_inst.layer = model.layers["Corner Detail"]
cda = "dynamic_attributes"
[cd_defn, cd_inst].each do |e|
  e.set_attribute(cda, "_name", "CornerSlideTR")
  e.set_attribute(cda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(cda, "slide", 0.0)
  e.set_attribute(cda, "x", 0.0)
  e.set_attribute(cda, "y", 0.0)
  e.set_attribute(cda, "z", 0.0)
end
cd_inst.set_attribute(cda, "_slide_access", "VIEW")
cd_inst.set_attribute(cda, "_slide_label", "Slide carriage on rail")
cd_inst.set_attribute(cda, "_y_formula", "-400*slide")
cd_inst.set_attribute(cda, "onclick", 'ANIMATE("slide", 0, 1)')
cd_inst.set_attribute(cda, "_onclick_access", "NONE")
tsl = entities.add_text("RAIL SLIDE\n(click: carriage slides on rail)", Geom::Point3d.new(2916.536838060324.mm, 1411.7039226776096.mm, 2223.8329485162067.mm), Geom::Vector3d.new(220.mm, -700.mm, 350.mm))
tsl.layer = model.layers["Corner Detail"] rescue nil


# ── Partial film-plane ghost at the TR corner (static, posed) ──

# ── Partial film-plane ghost at the rail-slide corner (posed + offset ox; nested in the slide
#    DC so it rides the carriage — the plane corner stays attached to the rail as it slides) ──
cg_defn = model.definitions.add("Corner Plane Ghost TR")
ents = cg_defn.entities
  # Film Plane (partial ghost)
  grp = ents.add_group
  grp.name = "Film Plane (partial ghost)"
  face = grp.entities.add_face([1349.5.mm,-6.mm,164.mm], [2249.5.mm,-6.mm,164.mm], [2249.5.mm,6.mm,164.mm], [1349.5.mm,6.mm,164.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(900.mm)
  mat = model.materials["Swing Plane (partial ghost)"] || model.materials.add("Swing Plane (partial ghost)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.16
  grp.material = mat

  # FP Frame ghost (top)
  grp = ents.add_group
  grp.name = "FP Frame ghost (top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-900.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,1064.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Swing FP Frame (top)"] || model.materials.add("Swing FP Frame (top)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.35
  grp.material = mat

  # FP Frame ghost (right)
  grp = ents.add_group
  grp.name = "FP Frame ghost (right)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -900.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,1064.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Swing FP Frame (top)"] || model.materials.add("Swing FP Frame (top)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.35
  grp.material = mat

cg_t = Geom::Transformation.translation([649.5.mm, 1181.mm, 1224.mm]) *
       Geom::Transformation.rotation(ORIGIN, Z_AXIS, (15.0).degrees) *
       Geom::Transformation.rotation(ORIGIN, X_AXIS, (20.0).degrees)
cg_inst = cd_defn.entities.add_instance(cg_defn, cg_t)
cg_inst.name = "Corner Plane Ghost TR"
cg_inst.layer = model.layers["Corner Detail"]


# ── Corner Swing (2nd detail — click: corner traces the swing arc; carriage Y + X float) ──

# ═══ Corner Swing — DYNAMIC COMPONENT (click: corner traces the swing arc) ═══
cs_defn = model.definitions.add("Corner Swing")
ents = cs_defn.entities
  # Swing Carriage TR
  grp = ents.add_group
  grp.name = "Swing Carriage TR"
  face = grp.entities.add_face([1123.mm,1149.mm,2270.mm], [1175.mm,1149.mm,2270.mm], [1175.mm,1213.mm,2270.mm], [1123.mm,1213.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Drive Nut TR
  grp = ents.add_group
  grp.name = "Swing Drive Nut TR"
  face = grp.entities.add_face([1169.mm,1167.mm,2276.mm], [1197.mm,1167.mm,2276.mm], [1197.mm,1195.mm,2276.mm], [1169.mm,1195.mm,2276.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing X cross-slide TR (SWING float)
  grp = ents.add_group
  grp.name = "Swing X cross-slide TR (SWING float)"
  face = grp.entities.add_face([1049.mm,1165.mm,2294.mm], [1179.mm,1165.mm,2294.mm], [1179.mm,1197.mm,2294.mm], [1049.mm,1197.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Detail X cross-slide TR (SWING)"] || model.materials.add("Detail X cross-slide TR (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

cs_inst = entities.add_instance(cs_defn, Geom::Transformation.new)
cs_inst.name = "Corner Swing"
cs_inst.layer = model.layers["Corner Detail"]
csa = "dynamic_attributes"
# nested child — the floating slider (built flat, world coords)
cf_defn = model.definitions.add("Corner Swing Float")
ents = cf_defn.entities
  # Swing X slider TR
  grp = ents.add_group
  grp.name = "Swing X slider TR"
  face = grp.entities.add_face([1133.mm,1161.mm,2292.mm], [1165.mm,1161.mm,2292.mm], [1165.mm,1201.mm,2292.mm], [1133.mm,1201.mm,2292.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Z cross-slide TR
  grp = ents.add_group
  grp.name = "Swing Z cross-slide TR"
  face = grp.entities.add_face([1140.mm,1166.mm,2279.mm], [1158.mm,1166.mm,2279.mm], [1158.mm,1196.mm,2279.mm], [1140.mm,1196.mm,2279.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Z cross-slide TR (TILT)"] || model.materials.add("Detail Z cross-slide TR (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Z slider TR
  grp = ents.add_group
  grp.name = "Swing Z slider TR"
  face = grp.entities.add_face([1136.mm,1163.mm,2272.mm], [1162.mm,1163.mm,2272.mm], [1162.mm,1199.mm,2272.mm], [1136.mm,1199.mm,2272.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Rod-End TR
  grp = ents.add_group
  grp.name = "Swing Rod-End TR"
  face = grp.entities.add_face([1132.mm,1164.mm,2271.mm], [1166.mm,1164.mm,2271.mm], [1166.mm,1198.mm,2271.mm], [1132.mm,1198.mm,2271.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Plane (partial ghost)
  grp = ents.add_group
  grp.name = "Swing Plane (partial ghost)"
  face = grp.entities.add_face([49.mm,1175.mm,1188.mm], [1149.mm,1175.mm,1188.mm], [1149.mm,1187.mm,1188.mm], [49.mm,1187.mm,1188.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1100.mm)
  mat = model.materials["Swing Plane (partial ghost)"] || model.materials.add("Swing Plane (partial ghost)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.16
  grp.material = mat

  # Swing FP Frame (top)
  grp = ents.add_group
  grp.name = "Swing FP Frame (top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1100.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1149.mm,1181.mm,2288.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Swing FP Frame (top)"] || model.materials.add("Swing FP Frame (top)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.35
  grp.material = mat

  # Swing FP Frame (right)
  grp = ents.add_group
  grp.name = "Swing FP Frame (right)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1100.mm)
  circle = ge.add_circle([1149.mm,1181.mm,2288.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Swing FP Frame (top)"] || model.materials.add("Swing FP Frame (top)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.35
  grp.material = mat

cf_inst = cs_defn.entities.add_instance(cf_defn, Geom::Transformation.new)
cf_inst.name = "Corner Swing Float"
cf_inst.layer = model.layers["Corner Detail"]
[cs_defn, cs_inst].each do |e|
  e.set_attribute(csa, "_name", "CornerSwing")
  e.set_attribute(csa, "_lengthunits", "MILLIMETERS")
  e.set_attribute(csa, "swing", 0.0)
  e.set_attribute(csa, "x", 0.0); e.set_attribute(csa, "y", 0.0); e.set_attribute(csa, "z", 0.0)
end
cs_inst.set_attribute(csa, "_swing_access", "VIEW")
cs_inst.set_attribute(csa, "_swing_label", "Swing (corner arc)")
cs_inst.set_attribute(csa, "_y_formula", "2249.5*SIN(15.0*swing)")
cs_inst.set_attribute(csa, "onclick", 'ANIMATE("swing", 0, 1)')
cs_inst.set_attribute(csa, "_onclick_access", "NONE")
[cf_defn, cf_inst].each do |e|
  e.set_attribute(csa, "_name", "CornerSwingFloat")
  e.set_attribute(csa, "_lengthunits", "MILLIMETERS")
  e.set_attribute(csa, "x", 0.0); e.set_attribute(csa, "y", 0.0); e.set_attribute(csa, "z", 0.0)
end
cf_inst.set_attribute(csa, "_x_formula", "2249.5*(COS(15.0*CornerSwing!swing)-1)")
ts = entities.add_text("SWING ARC\n(carriage in Y + X float; click to animate)", Geom::Point3d.new(1149.mm, 1181.mm, 2288.mm), Geom::Vector3d.new(250.mm, -700.mm, 350.mm))
ts.layer = model.layers["Corner Detail"] rescue nil


# ── Rotate Plane (4th diagram — rail + partial plane; click rotates the plane about its corner) ──

# ═══ Rotate Plane — DYNAMIC COMPONENT (click: partial plane rotates about its corner) ═══
rp_defn = model.definitions.add("Rotate Plane")
ents = rp_defn.entities
  # Rotate Plane (partial)
  grp = ents.add_group
  grp.name = "Rotate Plane (partial)"
  face = grp.entities.add_face([-1100.mm,-6.mm,-1100.mm], [0.mm,-6.mm,-1100.mm], [0.mm,6.mm,-1100.mm], [-1100.mm,6.mm,-1100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1100.mm)
  mat = model.materials["Swing Plane (partial ghost)"] || model.materials.add("Swing Plane (partial ghost)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.16
  grp.material = mat

  # Rotate Frame (top)
  grp = ents.add_group
  grp.name = "Rotate Frame (top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1100.mm, 0.mm, 0.mm)
  circle = ge.add_circle([0.mm,0.mm,0.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Swing FP Frame (top)"] || model.materials.add("Swing FP Frame (top)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.35
  grp.material = mat

  # Rotate Frame (right)
  grp = ents.add_group
  grp.name = "Rotate Frame (right)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1100.mm)
  circle = ge.add_circle([0.mm,0.mm,0.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Swing FP Frame (top)"] || model.materials.add("Swing FP Frame (top)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.35
  grp.material = mat

rp_inst = entities.add_instance(rp_defn, Geom::Transformation.translation([4649.mm, 1181.mm, 2288.mm]))
rp_inst.name = "Rotate Plane"
rp_inst.layer = model.layers["Corner Detail"]
rpa = "dynamic_attributes"
[rp_defn, rp_inst].each do |e|
  e.set_attribute(rpa, "_name", "RotatePlane")
  e.set_attribute(rpa, "_lengthunits", "MILLIMETERS")
  e.set_attribute(rpa, "rotate", 0.0)
  e.set_attribute(rpa, "rotx", 0.0)
  e.set_attribute(rpa, "rotz", 0.0)
end
rp_inst.set_attribute(rpa, "_rotate_access", "VIEW")
rp_inst.set_attribute(rpa, "_rotate_label", "Rotate (0 flat / 1 tilt+swing)")
rp_inst.set_attribute(rpa, "_rotx_formula", "20.0*rotate")
rp_inst.set_attribute(rpa, "_rotz_formula", "15.0*rotate")
rp_inst.set_attribute(rpa, "onclick", 'ANIMATE("rotate", 0, 1)')
rp_inst.set_attribute(rpa, "_onclick_access", "NONE")
tr = entities.add_text("RAIL + PLANE\n(click: plane rotates about its corner)", Geom::Point3d.new(4649.mm, 1181.mm, 2288.mm), Geom::Vector3d.new(220.mm, -700.mm, 350.mm))
tr.layer = model.layers["Corner Detail"] rescue nil


# ── Corner-detail callouts (Corner Detail tag — shown on the STATIC detail) ──
t=entities.add_text("HGR20 rail - FIXED (depth guide)", Geom::Point3d.new(-1476.mm,1161.7039226776096.mm,2288.mm), Geom::Vector3d.new(10,0,11.0)); t.layer=model.layers["Corner Detail"] rescue nil
t=entities.add_text("Leadscrew - DEPTH / focus drive", Geom::Point3d.new(-1442.mm,711.7039226776096.mm,2288.mm), Geom::Vector3d.new(4.0,0,19.0)); t.layer=model.layers["Corner Detail"] rescue nil
t=entities.add_text("Carriage + drive nut
(click: slides on rail)", Geom::Point3d.new(-1496.mm,1411.7039226776096.mm,2276.mm), Geom::Vector3d.new(-10.0,0,-15.0)); t.layer=model.layers["Corner Detail"] rescue nil
t=entities.add_text("X cross-slide = SWING float (blue)", Geom::Point3d.new(-1467.231580969838.mm,1411.7039226776096.mm,2302.mm), Geom::Vector3d.new(-12.0,0,4.0)); t.layer=model.layers["Corner Detail"] rescue nil
t=entities.add_text("Z cross-slide = TILT float (green)", Geom::Point3d.new(-1458.463161939676.mm,1411.7039226776096.mm,2255.9164742581033.mm), Geom::Vector3d.new(17.0,0,-12.0)); t.layer=model.layers["Corner Detail"] rescue nil
t=entities.add_text("Rod-end -> rigid frame corner", Geom::Point3d.new(-1458.463161939676.mm,1411.7039226776096.mm,2223.8329485162067.mm), Geom::Vector3d.new(17.0,0,5.0)); t.layer=model.layers["Corner Detail"] rescue nil
t=entities.add_text("ghost = corner if it stayed on rail", Geom::Point3d.new(-1476.mm,1411.7039226776096.mm,2288.mm), Geom::Vector3d.new(-17.0,0,13.0)); t.layer=model.layers["Corner Detail"] rescue nil

# ── Component callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Film Plane" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("FILM PLANE
(rigid screen — click to swing:
left fwd / right back)", anc, Geom::Vector3d.new(0.mm, -1200.mm, 800.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Corner Mechanism" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("HGR20 RAILS + LEADSCREWS
(4 fixed corner depth-guides)", anc, Geom::Vector3d.new(1600.mm, -300.mm, 550.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Processing Tray" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PROCESSING TRAY", anc, Geom::Vector3d.new(-800.mm, 650.mm, 450.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Walkways" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("WALKWAYS", anc, Geom::Vector3d.new(-1600.mm, -450.mm, 700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(4491.5.mm, 1046.mm, 115.mm)
txt = entities.add_text("RIGHT-WALKWAY CANTILEVER ARMS
(off the IBC corridor uprights —
share the BR combined corner plate)", anc, Geom::Vector3d.new(-700.mm, -350.mm, 650.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways", "IBC Cantilever", "Corner Detail", "Labels"]; dl = model.layers[0]
model.layers.to_a.each { |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }

model.layers.each { |l| l.visible = true }
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(0.6, -0.74, 0.42); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["Overview", ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways", "IBC Cantilever"], nil, 0], ["No Container", ["Film Plane", "Corner Mechanism", "Processing Tray"], nil, 0], ["Corner detail (TR)", ["Corner Detail"], [1814.018419030162.mm, 1296.3519613388048.mm, 2255.9164742581033.mm], 350], ["Labeled", ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways", "IBC Cantilever", "Labels"], nil, 0]].each { |name, tags, tgt, so|
  model.layers.each { |l| l.visible = (l == dl || tags.include?(l.name)) }
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cam = Sketchup::Camera.new(t.offset(dir, so), t, Z_AXIS); cam.fov = 35
    model.active_view.camera = cam
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name); page.use_camera = true
}
model.layers.each { |l| l.visible = true }
model.layers["Corner Detail"].visible = false
model.layers["Labels"].visible = false

model.commit_operation

# Register the DC AFTER committing (redraw_with_undo opens its own operation).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  cls.redraw_with_undo(fp_inst) rescue nil if cls
end

{ success: true, model: "film-plane", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tilt: 20.0, swing: 15.0 }.to_json
