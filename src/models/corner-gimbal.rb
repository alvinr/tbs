# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner Mechanism", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Corners") unless model.layers["Corners"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Pinhole") unless model.layers["Pinhole"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Corners ═══
  defn = model.definitions.add("Corners")
  ents = defn.entities
  # Depth slide rail Y BL
  grp = ents.add_group
  grp.name = "Depth slide rail Y BL"
  face = grp.entities.add_face([142.mm,1792.mm,15.mm], [158.mm,1792.mm,15.mm], [158.mm,2332.mm,15.mm], [142.mm,2332.mm,15.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Depth carriage BL
  grp = ents.add_group
  grp.name = "Depth carriage BL"
  face = grp.entities.add_face([128.mm,2232.mm,31.mm], [172.mm,2232.mm,31.mm], [172.mm,2292.mm,31.mm], [128.mm,2292.mm,31.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail BL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail BL"
  face = grp.entities.add_face([113.mm,2254.mm,33.mm], [127.mm,2254.mm,33.mm], [127.mm,2270.mm,33.mm], [113.mm,2270.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage BL
  grp = ents.add_group
  grp.name = "Vertical Z carriage BL"
  face = grp.entities.add_face([104.mm,2248.mm,73.mm], [136.mm,2248.mm,73.mm], [136.mm,2276.mm,73.mm], [104.mm,2276.mm,73.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail BL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail BL"
  face = grp.entities.add_face([150.mm,2256.mm,125.mm], [320.mm,2256.mm,125.mm], [320.mm,2268.mm,125.mm], [150.mm,2268.mm,125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage BL
  grp = ents.add_group
  grp.name = "Horizontal X carriage BL"
  face = grp.entities.add_face([128.mm,2251.mm,131.mm], [172.mm,2251.mm,131.mm], [172.mm,2273.mm,131.mm], [128.mm,2273.mm,131.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Horizontal X carriage BL"] || model.materials.add("Horizontal X carriage BL")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint BL
  grp = ents.add_group
  grp.name = "U-joint BL"
  face = grp.entities.add_face([138.mm,2250.mm,145.mm], [162.mm,2250.mm,145.mm], [162.mm,2274.mm,145.mm], [138.mm,2274.mm,145.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["U-joint BL"] || model.materials.add("U-joint BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Depth slide rail Y BR
  grp = ents.add_group
  grp.name = "Depth slide rail Y BR"
  face = grp.entities.add_face([4641.mm,1792.mm,15.mm], [4657.mm,1792.mm,15.mm], [4657.mm,2332.mm,15.mm], [4641.mm,2332.mm,15.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Depth carriage BR
  grp = ents.add_group
  grp.name = "Depth carriage BR"
  face = grp.entities.add_face([4627.mm,2232.mm,31.mm], [4671.mm,2232.mm,31.mm], [4671.mm,2292.mm,31.mm], [4627.mm,2292.mm,31.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail BR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail BR"
  face = grp.entities.add_face([4672.mm,2254.mm,33.mm], [4686.mm,2254.mm,33.mm], [4686.mm,2270.mm,33.mm], [4672.mm,2270.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage BR
  grp = ents.add_group
  grp.name = "Vertical Z carriage BR"
  face = grp.entities.add_face([4663.mm,2248.mm,73.mm], [4695.mm,2248.mm,73.mm], [4695.mm,2276.mm,73.mm], [4663.mm,2276.mm,73.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail BR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail BR"
  face = grp.entities.add_face([4479.mm,2256.mm,125.mm], [4649.mm,2256.mm,125.mm], [4649.mm,2268.mm,125.mm], [4479.mm,2268.mm,125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage BR
  grp = ents.add_group
  grp.name = "Horizontal X carriage BR"
  face = grp.entities.add_face([4627.mm,2251.mm,131.mm], [4671.mm,2251.mm,131.mm], [4671.mm,2273.mm,131.mm], [4627.mm,2273.mm,131.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Horizontal X carriage BL"] || model.materials.add("Horizontal X carriage BL")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint BR
  grp = ents.add_group
  grp.name = "U-joint BR"
  face = grp.entities.add_face([4637.mm,2250.mm,145.mm], [4661.mm,2250.mm,145.mm], [4661.mm,2274.mm,145.mm], [4637.mm,2274.mm,145.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["U-joint BL"] || model.materials.add("U-joint BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Depth slide rail Y TL
  grp = ents.add_group
  grp.name = "Depth slide rail Y TL"
  face = grp.entities.add_face([142.mm,1792.mm,2357.mm], [158.mm,1792.mm,2357.mm], [158.mm,2332.mm,2357.mm], [142.mm,2332.mm,2357.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Depth carriage TL
  grp = ents.add_group
  grp.name = "Depth carriage TL"
  face = grp.entities.add_face([128.mm,2232.mm,2333.mm], [172.mm,2232.mm,2333.mm], [172.mm,2292.mm,2333.mm], [128.mm,2292.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail TL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail TL"
  face = grp.entities.add_face([113.mm,2254.mm,2235.mm], [127.mm,2254.mm,2235.mm], [127.mm,2270.mm,2235.mm], [113.mm,2270.mm,2235.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage TL
  grp = ents.add_group
  grp.name = "Vertical Z carriage TL"
  face = grp.entities.add_face([104.mm,2248.mm,2265.mm], [136.mm,2248.mm,2265.mm], [136.mm,2276.mm,2265.mm], [104.mm,2276.mm,2265.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail TL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail TL"
  face = grp.entities.add_face([150.mm,2256.mm,2251.mm], [320.mm,2256.mm,2251.mm], [320.mm,2268.mm,2251.mm], [150.mm,2268.mm,2251.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage TL
  grp = ents.add_group
  grp.name = "Horizontal X carriage TL"
  face = grp.entities.add_face([128.mm,2251.mm,2237.mm], [172.mm,2251.mm,2237.mm], [172.mm,2273.mm,2237.mm], [128.mm,2273.mm,2237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Horizontal X carriage BL"] || model.materials.add("Horizontal X carriage BL")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint TL
  grp = ents.add_group
  grp.name = "U-joint TL"
  face = grp.entities.add_face([138.mm,2250.mm,2223.mm], [162.mm,2250.mm,2223.mm], [162.mm,2274.mm,2223.mm], [138.mm,2274.mm,2223.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["U-joint BL"] || model.materials.add("U-joint BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Depth slide rail Y TR
  grp = ents.add_group
  grp.name = "Depth slide rail Y TR"
  face = grp.entities.add_face([4641.mm,1792.mm,2357.mm], [4657.mm,1792.mm,2357.mm], [4657.mm,2332.mm,2357.mm], [4641.mm,2332.mm,2357.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Depth carriage TR
  grp = ents.add_group
  grp.name = "Depth carriage TR"
  face = grp.entities.add_face([4627.mm,2232.mm,2333.mm], [4671.mm,2232.mm,2333.mm], [4671.mm,2292.mm,2333.mm], [4627.mm,2292.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail TR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail TR"
  face = grp.entities.add_face([4672.mm,2254.mm,2235.mm], [4686.mm,2254.mm,2235.mm], [4686.mm,2270.mm,2235.mm], [4672.mm,2270.mm,2235.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage TR
  grp = ents.add_group
  grp.name = "Vertical Z carriage TR"
  face = grp.entities.add_face([4663.mm,2248.mm,2265.mm], [4695.mm,2248.mm,2265.mm], [4695.mm,2276.mm,2265.mm], [4663.mm,2276.mm,2265.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Depth carriage BL"] || model.materials.add("Depth carriage BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail TR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail TR"
  face = grp.entities.add_face([4479.mm,2256.mm,2251.mm], [4649.mm,2256.mm,2251.mm], [4649.mm,2268.mm,2251.mm], [4479.mm,2268.mm,2251.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Depth slide rail Y BL"] || model.materials.add("Depth slide rail Y BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage TR
  grp = ents.add_group
  grp.name = "Horizontal X carriage TR"
  face = grp.entities.add_face([4627.mm,2251.mm,2237.mm], [4671.mm,2251.mm,2237.mm], [4671.mm,2273.mm,2237.mm], [4627.mm,2273.mm,2237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Horizontal X carriage BL"] || model.materials.add("Horizontal X carriage BL")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint TR
  grp = ents.add_group
  grp.name = "U-joint TR"
  face = grp.entities.add_face([4637.mm,2250.mm,2223.mm], [4661.mm,2250.mm,2223.mm], [4661.mm,2274.mm,2223.mm], [4637.mm,2274.mm,2223.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["U-joint BL"] || model.materials.add("U-joint BL")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corners"
  inst.layer = model.layers["Corners"]

  # ═══ Film Plane ═══
  defn = model.definitions.add("Film Plane")
  ents = defn.entities
  # Film plane (ghost)
  grp = ents.add_group
  grp.name = "Film plane (ghost)"
  face = grp.entities.add_face([150.mm,2262.mm,155.mm], [4649.mm,2262.mm,155.mm], [4649.mm,2266.mm,155.mm], [150.mm,2266.mm,155.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2078.mm)
  mat = model.materials["Film plane (ghost)"] || model.materials.add("Film plane (ghost)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.14
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane"
  inst.layer = model.layers["Film Plane"]

  # ═══ Pinhole ═══
  defn = model.definitions.add("Pinhole")
  ents = defn.entities
  # Pinhole wall (far)
  grp = ents.add_group
  grp.name = "Pinhole wall (far)"
  face = grp.entities.add_face([0.mm,-14.mm,0.mm], [5893.mm,-14.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole wall (far)"] || model.materials.add("Pinhole wall (far)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.06
  grp.material = mat

  # Pinhole aperture
  grp = ents.add_group
  grp.name = "Pinhole aperture"
  face = grp.entities.add_face([2388.mm,-18.mm,1183.mm], [2410.mm,-18.mm,1183.mm], [2410.mm,4.mm,1183.mm], [2388.mm,4.mm,1183.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Pinhole aperture"] || model.materials.add("Pinhole aperture")
  mat.color = Sketchup::Color.new(16, 16, 20)
  mat.alpha = 1.0
  grp.material = mat

  # light cone — pinhole → 4 panel corners
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(150.mm, 2262.mm, 2233.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4649.mm, 2262.mm, 2233.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(150.mm, 2262.mm, 155.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4649.mm, 2262.mm, 155.mm))

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole"
  inst.layer = model.layers["Pinhole"]


# ── "Labeled" callouts (Labels tag) ──

tt = entities.add_text("PINHOLE (far wall) — the film plane faces it across the throw", Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Vector3d.new(60.mm, -50.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film plane 4499 x 2078 (mechanism ~140 top + bottom)", Geom::Point3d.new(2400.mm, 2262.mm, 1194.mm), Geom::Vector3d.new(60.mm, 45.mm, 20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("TOP pair vs BOTTOM pair depth = TILT", Geom::Point3d.new(150.mm, 2262.mm, 2388.mm), Geom::Vector3d.new(-60.mm, -40.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("LEFT pair vs RIGHT pair depth = SWING", Geom::Point3d.new(4649.mm, 2262.mm, 155.mm), Geom::Vector3d.new(60.mm, 40.mm, -20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("DEPTH slide (Y) — drives tilt + swing", Geom::Point3d.new(150.mm, 1962.mm, 115.mm), Geom::Vector3d.new(-55.mm, -40.mm, -10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("VERTICAL slide (Z) — absorbs TILT", Geom::Point3d.new(120.mm, 2262.mm, 175.mm), Geom::Vector3d.new(-60.mm, -40.mm, 10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("HORIZONTAL slide (X) — absorbs SWING", Geom::Point3d.new(270.mm, 2262.mm, 165.mm), Geom::Vector3d.new(55.mm, -40.mm, 5.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("U-joint (tilt + swing, twist locked)", Geom::Point3d.new(150.mm, 2250.mm, 155.mm), Geom::Vector3d.new(-55.mm, -45.mm, 15.mm))
tt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Corners", "Film Plane", "Pinhole", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── iso scenes (Overview / Corner detail / Labeled) ──
[["Overview", ["Corners", "Film Plane", "Pinhole"], [2400.mm, 1862.mm, 1194.mm, 6500.mm]], ["Corner detail", ["Corners", "Film Plane", "Pinhole"], [150.mm, 2262.mm, 185.mm, 620.mm]], ["Labeled", ["Corners", "Film Plane", "Pinhole", "Labels"], [2400.mm, 1862.mm, 1194.mm, 7200.mm]]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
  cdir = Geom::Vector3d.new(0.5, -0.7, 0.4); cdir.normalize!
  model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  page = model.pages.add(name)
  page.use_camera = true
}

# ── Tilt (side) — look along +X at the left edge: depth (Y) horizontal, height (Z) vertical ──
model.layers.each { |l| l.visible = (l == default_layer || ["Corners", "Film Plane", "Pinhole"].include?(l.name)) }
tc = Geom::Point3d.new(150.mm, 2262.mm, 1194.mm)
te = Geom::Point3d.new(-4050.mm, 2262.mm, 1194.mm)
model.active_view.camera = Sketchup::Camera.new(te, tc, Z_AXIS)
ps = model.pages.add("Tilt (side)"); ps.use_camera = true

# ── Swing (top) — top-down over the pinhole→panel span: width (X) and depth (Y) ──
sc = Geom::Point3d.new(2399.mm, 1131.mm, 0)
se = Geom::Point3d.new(2399.mm, 1131.mm, 9500.mm)
model.active_view.camera = Sketchup::Camera.new(se, sc, Y_AXIS)
ps2 = model.pages.add("Swing (top)"); ps2.use_camera = true

model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
