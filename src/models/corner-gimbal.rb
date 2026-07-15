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
  # Depth pipe rail Y (1.5in 304, grey) BL
  grp = ents.add_group
  grp.name = "Depth pipe rail Y (1.5in 304, grey) BL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,0.mm,39.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2362.mm)
  mat = model.materials["Depth pipe rail Y (1.5in 304, grey) BL"] || model.materials.add("Depth pipe rail Y (1.5in 304, grey) BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange BL 0
  grp = ents.add_group
  grp.name = "Pipe flange BL 0"
  face = grp.entities.add_face([105.mm,0.mm,-6.mm], [195.mm,0.mm,-6.mm], [195.mm,12.mm,-6.mm], [105.mm,12.mm,-6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange BL 2350
  grp = ents.add_group
  grp.name = "Pipe flange BL 2350"
  face = grp.entities.add_face([105.mm,2350.mm,-6.mm], [195.mm,2350.mm,-6.mm], [195.mm,2362.mm,-6.mm], [105.mm,2362.mm,-6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe wall plate BL PH
  grp = ents.add_group
  grp.name = "Pipe wall plate BL PH"
  face = grp.entities.add_face([100.mm,-48.mm,-11.mm], [200.mm,-48.mm,-11.mm], [200.mm,-40.mm,-11.mm], [100.mm,-40.mm,-11.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Pipe wall plate BL far
  grp = ents.add_group
  grp.name = "Pipe wall plate BL far"
  face = grp.entities.add_face([100.mm,2402.mm,-11.mm], [200.mm,2402.mm,-11.mm], [200.mm,2410.mm,-11.mm], [100.mm,2410.mm,-11.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Depth trolley cradle (red) BL
  grp = ents.add_group
  grp.name = "Depth trolley cradle (red) BL"
  face = grp.entities.add_face([124.mm,2236.mm,15.mm], [176.mm,2236.mm,15.mm], [176.mm,2284.mm,15.mm], [124.mm,2284.mm,15.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Depth trolley cradle (red) BL"] || model.materials.add("Depth trolley cradle (red) BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.35
  grp.material = mat

  # Trolley wheel BL 2238_-18
  grp = ents.add_group
  grp.name = "Trolley wheel BL 2238_-18"
  ge = grp.entities
  circle = ge.add_circle([128.mm,2238.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel BL 2238_18
  grp = ents.add_group
  grp.name = "Trolley wheel BL 2238_18"
  ge = grp.entities
  circle = ge.add_circle([164.mm,2238.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel BL 2256_-18
  grp = ents.add_group
  grp.name = "Trolley wheel BL 2256_-18"
  ge = grp.entities
  circle = ge.add_circle([128.mm,2256.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel BL 2256_18
  grp = ents.add_group
  grp.name = "Trolley wheel BL 2256_18"
  ge = grp.entities
  circle = ge.add_circle([164.mm,2256.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT ~280mm, green) BL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT ~280mm, green) BL"
  face = grp.entities.add_face([113.mm,2253.mm,33.mm], [129.mm,2253.mm,33.mm], [129.mm,2271.mm,33.mm], [113.mm,2271.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(282.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage BL
  grp = ents.add_group
  grp.name = "Vertical Z carriage BL"
  face = grp.entities.add_face([103.mm,2247.mm,70.mm], [137.mm,2247.mm,70.mm], [137.mm,2277.mm,70.mm], [103.mm,2277.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING ~260mm, purple) BL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING ~260mm, purple) BL"
  face = grp.entities.add_face([150.mm,2255.mm,83.mm], [410.mm,2255.mm,83.mm], [410.mm,2269.mm,83.mm], [150.mm,2269.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage BL
  grp = ents.add_group
  grp.name = "Horizontal X carriage BL"
  face = grp.entities.add_face([126.mm,2250.mm,89.mm], [174.mm,2250.mm,89.mm], [174.mm,2274.mm,89.mm], [126.mm,2274.mm,89.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint BL
  grp = ents.add_group
  grp.name = "U-joint BL"
  face = grp.entities.add_face([138.mm,2250.mm,105.mm], [162.mm,2250.mm,105.mm], [162.mm,2274.mm,105.mm], [138.mm,2274.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Depth pipe rail Y (1.5in 304, grey) BR
  grp = ents.add_group
  grp.name = "Depth pipe rail Y (1.5in 304, grey) BR"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,0.mm,39.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2362.mm)
  mat = model.materials["Depth pipe rail Y (1.5in 304, grey) BL"] || model.materials.add("Depth pipe rail Y (1.5in 304, grey) BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange BR 0
  grp = ents.add_group
  grp.name = "Pipe flange BR 0"
  face = grp.entities.add_face([4604.mm,0.mm,-6.mm], [4694.mm,0.mm,-6.mm], [4694.mm,12.mm,-6.mm], [4604.mm,12.mm,-6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange BR 2350
  grp = ents.add_group
  grp.name = "Pipe flange BR 2350"
  face = grp.entities.add_face([4604.mm,2350.mm,-6.mm], [4694.mm,2350.mm,-6.mm], [4694.mm,2362.mm,-6.mm], [4604.mm,2362.mm,-6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe wall plate BR PH
  grp = ents.add_group
  grp.name = "Pipe wall plate BR PH"
  face = grp.entities.add_face([4599.mm,-48.mm,-11.mm], [4699.mm,-48.mm,-11.mm], [4699.mm,-40.mm,-11.mm], [4599.mm,-40.mm,-11.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Pipe wall plate BR far
  grp = ents.add_group
  grp.name = "Pipe wall plate BR far"
  face = grp.entities.add_face([4599.mm,2402.mm,-11.mm], [4699.mm,2402.mm,-11.mm], [4699.mm,2410.mm,-11.mm], [4599.mm,2410.mm,-11.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Depth trolley cradle (red) BR
  grp = ents.add_group
  grp.name = "Depth trolley cradle (red) BR"
  face = grp.entities.add_face([4623.mm,2236.mm,15.mm], [4675.mm,2236.mm,15.mm], [4675.mm,2284.mm,15.mm], [4623.mm,2284.mm,15.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Depth trolley cradle (red) BL"] || model.materials.add("Depth trolley cradle (red) BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.35
  grp.material = mat

  # Trolley wheel BR 2238_-18
  grp = ents.add_group
  grp.name = "Trolley wheel BR 2238_-18"
  ge = grp.entities
  circle = ge.add_circle([4627.mm,2238.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel BR 2238_18
  grp = ents.add_group
  grp.name = "Trolley wheel BR 2238_18"
  ge = grp.entities
  circle = ge.add_circle([4663.mm,2238.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel BR 2256_-18
  grp = ents.add_group
  grp.name = "Trolley wheel BR 2256_-18"
  ge = grp.entities
  circle = ge.add_circle([4627.mm,2256.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel BR 2256_18
  grp = ents.add_group
  grp.name = "Trolley wheel BR 2256_18"
  ge = grp.entities
  circle = ge.add_circle([4663.mm,2256.mm,61.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT ~280mm, green) BR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT ~280mm, green) BR"
  face = grp.entities.add_face([4672.mm,2253.mm,33.mm], [4688.mm,2253.mm,33.mm], [4688.mm,2271.mm,33.mm], [4672.mm,2271.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(282.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage BR
  grp = ents.add_group
  grp.name = "Vertical Z carriage BR"
  face = grp.entities.add_face([4662.mm,2247.mm,70.mm], [4696.mm,2247.mm,70.mm], [4696.mm,2277.mm,70.mm], [4662.mm,2277.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING ~260mm, purple) BR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING ~260mm, purple) BR"
  face = grp.entities.add_face([4389.mm,2255.mm,83.mm], [4649.mm,2255.mm,83.mm], [4649.mm,2269.mm,83.mm], [4389.mm,2269.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage BR
  grp = ents.add_group
  grp.name = "Horizontal X carriage BR"
  face = grp.entities.add_face([4625.mm,2250.mm,89.mm], [4673.mm,2250.mm,89.mm], [4673.mm,2274.mm,89.mm], [4625.mm,2274.mm,89.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint BR
  grp = ents.add_group
  grp.name = "U-joint BR"
  face = grp.entities.add_face([4637.mm,2250.mm,105.mm], [4661.mm,2250.mm,105.mm], [4661.mm,2274.mm,105.mm], [4637.mm,2274.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Depth pipe rail Y (1.5in 304, grey) TL
  grp = ents.add_group
  grp.name = "Depth pipe rail Y (1.5in 304, grey) TL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,0.mm,2349.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2362.mm)
  mat = model.materials["Depth pipe rail Y (1.5in 304, grey) BL"] || model.materials.add("Depth pipe rail Y (1.5in 304, grey) BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange TL 0
  grp = ents.add_group
  grp.name = "Pipe flange TL 0"
  face = grp.entities.add_face([105.mm,0.mm,2304.mm], [195.mm,0.mm,2304.mm], [195.mm,12.mm,2304.mm], [105.mm,12.mm,2304.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange TL 2350
  grp = ents.add_group
  grp.name = "Pipe flange TL 2350"
  face = grp.entities.add_face([105.mm,2350.mm,2304.mm], [195.mm,2350.mm,2304.mm], [195.mm,2362.mm,2304.mm], [105.mm,2362.mm,2304.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe wall plate TL PH
  grp = ents.add_group
  grp.name = "Pipe wall plate TL PH"
  face = grp.entities.add_face([100.mm,-48.mm,2299.mm], [200.mm,-48.mm,2299.mm], [200.mm,-40.mm,2299.mm], [100.mm,-40.mm,2299.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Pipe wall plate TL far
  grp = ents.add_group
  grp.name = "Pipe wall plate TL far"
  face = grp.entities.add_face([100.mm,2402.mm,2299.mm], [200.mm,2402.mm,2299.mm], [200.mm,2410.mm,2299.mm], [100.mm,2410.mm,2299.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Depth trolley cradle (red) TL
  grp = ents.add_group
  grp.name = "Depth trolley cradle (red) TL"
  face = grp.entities.add_face([124.mm,2236.mm,2325.mm], [176.mm,2236.mm,2325.mm], [176.mm,2284.mm,2325.mm], [124.mm,2284.mm,2325.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Depth trolley cradle (red) BL"] || model.materials.add("Depth trolley cradle (red) BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.35
  grp.material = mat

  # Trolley wheel TL 2238_-18
  grp = ents.add_group
  grp.name = "Trolley wheel TL 2238_-18"
  ge = grp.entities
  circle = ge.add_circle([128.mm,2238.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel TL 2238_18
  grp = ents.add_group
  grp.name = "Trolley wheel TL 2238_18"
  ge = grp.entities
  circle = ge.add_circle([164.mm,2238.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel TL 2256_-18
  grp = ents.add_group
  grp.name = "Trolley wheel TL 2256_-18"
  ge = grp.entities
  circle = ge.add_circle([128.mm,2256.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel TL 2256_18
  grp = ents.add_group
  grp.name = "Trolley wheel TL 2256_18"
  ge = grp.entities
  circle = ge.add_circle([164.mm,2256.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT ~280mm, green) TL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT ~280mm, green) TL"
  face = grp.entities.add_face([113.mm,2253.mm,2073.mm], [129.mm,2253.mm,2073.mm], [129.mm,2271.mm,2073.mm], [113.mm,2271.mm,2073.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(282.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage TL
  grp = ents.add_group
  grp.name = "Vertical Z carriage TL"
  face = grp.entities.add_face([103.mm,2247.mm,2268.mm], [137.mm,2247.mm,2268.mm], [137.mm,2277.mm,2268.mm], [103.mm,2277.mm,2268.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING ~260mm, purple) TL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING ~260mm, purple) TL"
  face = grp.entities.add_face([150.mm,2255.mm,2291.mm], [410.mm,2255.mm,2291.mm], [410.mm,2269.mm,2291.mm], [150.mm,2269.mm,2291.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage TL
  grp = ents.add_group
  grp.name = "Horizontal X carriage TL"
  face = grp.entities.add_face([126.mm,2250.mm,2277.mm], [174.mm,2250.mm,2277.mm], [174.mm,2274.mm,2277.mm], [126.mm,2274.mm,2277.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint TL
  grp = ents.add_group
  grp.name = "U-joint TL"
  face = grp.entities.add_face([138.mm,2250.mm,2263.mm], [162.mm,2250.mm,2263.mm], [162.mm,2274.mm,2263.mm], [138.mm,2274.mm,2263.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Depth pipe rail Y (1.5in 304, grey) TR
  grp = ents.add_group
  grp.name = "Depth pipe rail Y (1.5in 304, grey) TR"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,0.mm,2349.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2362.mm)
  mat = model.materials["Depth pipe rail Y (1.5in 304, grey) BL"] || model.materials.add("Depth pipe rail Y (1.5in 304, grey) BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange TR 0
  grp = ents.add_group
  grp.name = "Pipe flange TR 0"
  face = grp.entities.add_face([4604.mm,0.mm,2304.mm], [4694.mm,0.mm,2304.mm], [4694.mm,12.mm,2304.mm], [4604.mm,12.mm,2304.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe flange TR 2350
  grp = ents.add_group
  grp.name = "Pipe flange TR 2350"
  face = grp.entities.add_face([4604.mm,2350.mm,2304.mm], [4694.mm,2350.mm,2304.mm], [4694.mm,2362.mm,2304.mm], [4604.mm,2362.mm,2304.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pipe wall plate TR PH
  grp = ents.add_group
  grp.name = "Pipe wall plate TR PH"
  face = grp.entities.add_face([4599.mm,-48.mm,2299.mm], [4699.mm,-48.mm,2299.mm], [4699.mm,-40.mm,2299.mm], [4599.mm,-40.mm,2299.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Pipe wall plate TR far
  grp = ents.add_group
  grp.name = "Pipe wall plate TR far"
  face = grp.entities.add_face([4599.mm,2402.mm,2299.mm], [4699.mm,2402.mm,2299.mm], [4699.mm,2410.mm,2299.mm], [4599.mm,2410.mm,2299.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pipe wall plate BL PH"] || model.materials.add("Pipe wall plate BL PH")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.5
  grp.material = mat

  # Depth trolley cradle (red) TR
  grp = ents.add_group
  grp.name = "Depth trolley cradle (red) TR"
  face = grp.entities.add_face([4623.mm,2236.mm,2325.mm], [4675.mm,2236.mm,2325.mm], [4675.mm,2284.mm,2325.mm], [4623.mm,2284.mm,2325.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Depth trolley cradle (red) BL"] || model.materials.add("Depth trolley cradle (red) BL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.35
  grp.material = mat

  # Trolley wheel TR 2238_-18
  grp = ents.add_group
  grp.name = "Trolley wheel TR 2238_-18"
  ge = grp.entities
  circle = ge.add_circle([4627.mm,2238.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel TR 2238_18
  grp = ents.add_group
  grp.name = "Trolley wheel TR 2238_18"
  ge = grp.entities
  circle = ge.add_circle([4663.mm,2238.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel TR 2256_-18
  grp = ents.add_group
  grp.name = "Trolley wheel TR 2256_-18"
  ge = grp.entities
  circle = ge.add_circle([4627.mm,2256.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Trolley wheel TR 2256_18
  grp = ents.add_group
  grp.name = "Trolley wheel TR 2256_18"
  ge = grp.entities
  circle = ge.add_circle([4663.mm,2256.mm,2327.mm], [1,0,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(8.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT ~280mm, green) TR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT ~280mm, green) TR"
  face = grp.entities.add_face([4672.mm,2253.mm,2073.mm], [4688.mm,2253.mm,2073.mm], [4688.mm,2271.mm,2073.mm], [4672.mm,2271.mm,2073.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(282.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z carriage TR
  grp = ents.add_group
  grp.name = "Vertical Z carriage TR"
  face = grp.entities.add_face([4662.mm,2247.mm,2268.mm], [4696.mm,2247.mm,2268.mm], [4696.mm,2277.mm,2268.mm], [4662.mm,2277.mm,2268.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Vertical Z slide rail (TILT ~280mm, green) BL"] || model.materials.add("Vertical Z slide rail (TILT ~280mm, green) BL")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING ~260mm, purple) TR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING ~260mm, purple) TR"
  face = grp.entities.add_face([4389.mm,2255.mm,2291.mm], [4649.mm,2255.mm,2291.mm], [4649.mm,2269.mm,2291.mm], [4389.mm,2269.mm,2291.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X carriage TR
  grp = ents.add_group
  grp.name = "Horizontal X carriage TR"
  face = grp.entities.add_face([4625.mm,2250.mm,2277.mm], [4673.mm,2250.mm,2277.mm], [4673.mm,2274.mm,2277.mm], [4625.mm,2274.mm,2277.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Horizontal X slide rail (SWING ~260mm, purple) BL"] || model.materials.add("Horizontal X slide rail (SWING ~260mm, purple) BL")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint TR
  grp = ents.add_group
  grp.name = "U-joint TR"
  face = grp.entities.add_face([4637.mm,2250.mm,2263.mm], [4661.mm,2250.mm,2263.mm], [4661.mm,2274.mm,2263.mm], [4637.mm,2274.mm,2263.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Pipe flange BL 0"] || model.materials.add("Pipe flange BL 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Floor
  grp = ents.add_group
  grp.name = "Floor"
  face = grp.entities.add_face([-100.mm,0.mm,-12.mm], [4899.mm,0.mm,-12.mm], [4899.mm,2512.mm,-12.mm], [-100.mm,2512.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.05
  grp.material = mat

  # Ceiling
  grp = ents.add_group
  grp.name = "Ceiling"
  face = grp.entities.add_face([-100.mm,0.mm,2388.mm], [4899.mm,0.mm,2388.mm], [4899.mm,2512.mm,2388.mm], [-100.mm,2512.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.05
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
  face = grp.entities.add_face([150.mm,2262.mm,125.mm], [4649.mm,2262.mm,125.mm], [4649.mm,2266.mm,125.mm], [150.mm,2266.mm,125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
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
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(150.mm, 2262.mm, 2263.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4649.mm, 2262.mm, 2263.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(150.mm, 2262.mm, 125.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4649.mm, 2262.mm, 125.mm))

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole"
  inst.layer = model.layers["Pinhole"]


# ── "Labeled" callouts (Labels tag) ──

tt = entities.add_text("PINHOLE (far wall) — the film plane faces it across the throw", Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Vector3d.new(60.mm, -50.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film plane 4499 x 2138 (mechanism ~110 top + bottom)", Geom::Point3d.new(2400.mm, 2262.mm, 1194.mm), Geom::Vector3d.new(60.mm, 45.mm, 20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("TOP pair vs BOTTOM pair depth = TILT", Geom::Point3d.new(150.mm, 2262.mm, 2388.mm), Geom::Vector3d.new(-60.mm, -40.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("LEFT pair vs RIGHT pair depth = SWING", Geom::Point3d.new(4649.mm, 2262.mm, 125.mm), Geom::Vector3d.new(60.mm, 40.mm, -20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("UPPER rails (ceiling) — TOP corners hang (tension)", Geom::Point3d.new(2400.mm, 1912.mm, 2388.mm), Geom::Vector3d.new(45.mm, -40.mm, 12.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("LOWER rails (floor) — BOTTOM corners bear (compression)", Geom::Point3d.new(2400.mm, 1912.mm, 0.mm), Geom::Vector3d.new(45.mm, -40.mm, -12.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("DEPTH slide (Y, GREY) — drives tilt + swing", Geom::Point3d.new(150.mm, 1962.mm, 85.mm), Geom::Vector3d.new(-55.mm, -40.mm, -10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("VERTICAL slide (Z, GREEN) — absorbs TILT", Geom::Point3d.new(120.mm, 2262.mm, 145.mm), Geom::Vector3d.new(-60.mm, -40.mm, 10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("HORIZONTAL slide (X, PURPLE) — absorbs SWING", Geom::Point3d.new(270.mm, 2262.mm, 135.mm), Geom::Vector3d.new(55.mm, -40.mm, 5.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("U-joint (tilt + swing, twist locked)", Geom::Point3d.new(150.mm, 2250.mm, 125.mm), Geom::Vector3d.new(-55.mm, -45.mm, 15.mm))
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
[["Overview", ["Corners", "Film Plane", "Pinhole"], [2400.mm, 1862.mm, 1194.mm, 6500.mm]], ["Corner detail", ["Corners", "Film Plane", "Pinhole"], [150.mm, 2262.mm, 155.mm, 620.mm]], ["Labeled", ["Corners", "Film Plane", "Pinhole", "Labels"], [2400.mm, 1862.mm, 1194.mm, 7200.mm]]].each { |name, tags, tgt|
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
