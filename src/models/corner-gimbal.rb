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

  model.layers.add("Bottom Corner") unless model.layers["Bottom Corner"]
  model.layers.add("Top Corner") unless model.layers["Top Corner"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Bottom Corner ═══
  defn = model.definitions.add("Bottom Corner")
  ents = defn.entities
  # Depth slide rail Y (~2.2m) (bot)
  grp = ents.add_group
  grp.name = "Depth slide rail Y (~2.2m) (bot)"
  face = grp.entities.add_face([-10.mm,-1000.mm,2.mm], [10.mm,-1000.mm,2.mm], [10.mm,1000.mm,2.mm], [-10.mm,1000.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Depth slide rail Y (~2.2m) (bot)"] || model.materials.add("Depth slide rail Y (~2.2m) (bot)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Depth carriage body (bot)
  grp = ents.add_group
  grp.name = "Depth carriage body (bot)"
  face = grp.entities.add_face([-22.mm,-30.mm,16.mm], [22.mm,-30.mm,16.mm], [22.mm,30.mm,16.mm], [-22.mm,30.mm,16.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Depth grip tab L (bot)
  grp = ents.add_group
  grp.name = "Depth grip tab L (bot)"
  face = grp.entities.add_face([-20.mm,-30.mm,0.mm], [-12.mm,-30.mm,0.mm], [-12.mm,30.mm,0.mm], [-20.mm,30.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(17.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Depth grip tab R (bot)
  grp = ents.add_group
  grp.name = "Depth grip tab R (bot)"
  face = grp.entities.add_face([12.mm,-30.mm,0.mm], [20.mm,-30.mm,0.mm], [20.mm,30.mm,0.mm], [12.mm,30.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(17.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Depth cam clamp body (bot)
  grp = ents.add_group
  grp.name = "Depth cam clamp body (bot)"
  face = grp.entities.add_face([22.mm,30.mm,20.mm], [36.mm,30.mm,20.mm], [36.mm,44.mm,20.mm], [22.mm,44.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Depth clamp lever (bot)
  grp = ents.add_group
  grp.name = "Depth clamp lever (bot)"
  ge = grp.entities
  circle = ge.add_circle([28.mm,44.mm,27.mm], [0,1,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical slide rail Z (bot)
  grp = ents.add_group
  grp.name = "Vertical slide rail Z (bot)"
  face = grp.entities.add_face([-34.mm,-6.mm,20.mm], [-24.mm,-6.mm,20.mm], [-24.mm,6.mm,20.mm], [-34.mm,6.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(330.mm)
  mat = model.materials["Depth slide rail Y (~2.2m) (bot)"] || model.materials.add("Depth slide rail Y (~2.2m) (bot)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical carriage body (bot)
  grp = ents.add_group
  grp.name = "Vertical carriage body (bot)"
  face = grp.entities.add_face([-44.mm,-12.mm,150.mm], [-18.mm,-12.mm,150.mm], [-18.mm,12.mm,150.mm], [-44.mm,12.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical grip tab F (bot)
  grp = ents.add_group
  grp.name = "Vertical grip tab F (bot)"
  face = grp.entities.add_face([-44.mm,-15.mm,152.mm], [-18.mm,-15.mm,152.mm], [-18.mm,-6.mm,152.mm], [-44.mm,-6.mm,152.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical grip tab B (bot)
  grp = ents.add_group
  grp.name = "Vertical grip tab B (bot)"
  face = grp.entities.add_face([-44.mm,6.mm,152.mm], [-18.mm,6.mm,152.mm], [-18.mm,15.mm,152.mm], [-44.mm,15.mm,152.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical cam clamp body (bot)
  grp = ents.add_group
  grp.name = "Vertical cam clamp body (bot)"
  face = grp.entities.add_face([-47.mm,26.mm,158.mm], [-33.mm,26.mm,158.mm], [-33.mm,40.mm,158.mm], [-47.mm,40.mm,158.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical clamp lever (bot)
  grp = ents.add_group
  grp.name = "Vertical clamp lever (bot)"
  ge = grp.entities
  circle = ge.add_circle([-33.mm,40.mm,165.mm], [0,1,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage bracket to X-slide (bot)
  grp = ents.add_group
  grp.name = "Carriage bracket to X-slide (bot)"
  face = grp.entities.add_face([-30.mm,-8.mm,158.mm], [4.mm,-8.mm,158.mm], [4.mm,8.mm,158.mm], [-30.mm,8.mm,158.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Floating X slide (bot)
  grp = ents.add_group
  grp.name = "Floating X slide (bot)"
  face = grp.entities.add_face([-24.mm,-11.mm,160.mm], [24.mm,-11.mm,160.mm], [24.mm,11.mm,160.mm], [-24.mm,11.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint cross (bot)
  grp = ents.add_group
  grp.name = "U-joint cross (bot)"
  face = grp.entities.add_face([-10.mm,-10.mm,172.mm], [10.mm,-10.mm,172.mm], [10.mm,10.mm,172.mm], [-10.mm,10.mm,172.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["U-joint cross (bot)"] || model.materials.add("U-joint cross (bot)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt pin X (bot)
  grp = ents.add_group
  grp.name = "Tilt pin X (bot)"
  ge = grp.entities
  circle = ge.add_circle([-26.mm,-4.mm,182.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(52.mm)
  mat = model.materials["Tilt pin X (bot)"] || model.materials.add("Tilt pin X (bot)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing pin Z (bot)
  grp = ents.add_group
  grp.name = "Swing pin Z (bot)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,4.mm,168.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Tilt pin X (bot)"] || model.materials.add("Tilt pin X (bot)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke ear L (bot)
  grp = ents.add_group
  grp.name = "Out yoke ear L (bot)"
  face = grp.entities.add_face([-30.mm,-10.mm,172.mm], [-22.mm,-10.mm,172.mm], [-22.mm,10.mm,172.mm], [-30.mm,10.mm,172.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke ear R (bot)
  grp = ents.add_group
  grp.name = "Out yoke ear R (bot)"
  face = grp.entities.add_face([22.mm,-10.mm,172.mm], [30.mm,-10.mm,172.mm], [30.mm,10.mm,172.mm], [22.mm,10.mm,172.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke web (bot)
  grp = ents.add_group
  grp.name = "Out yoke web (bot)"
  face = grp.entities.add_face([-30.mm,10.mm,174.mm], [30.mm,10.mm,174.mm], [30.mm,18.mm,174.mm], [-30.mm,18.mm,174.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke stub (bot)
  grp = ents.add_group
  grp.name = "Out yoke stub (bot)"
  face = grp.entities.add_face([-6.mm,17.mm,176.mm], [6.mm,17.mm,176.mm], [6.mm,47.mm,176.mm], [-6.mm,47.mm,176.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke ear Lo (bot)
  grp = ents.add_group
  grp.name = "In yoke ear Lo (bot)"
  face = grp.entities.add_face([-9.mm,-9.mm,164.mm], [9.mm,-9.mm,164.mm], [9.mm,9.mm,164.mm], [-9.mm,9.mm,164.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke ear Hi (bot)
  grp = ents.add_group
  grp.name = "In yoke ear Hi (bot)"
  face = grp.entities.add_face([-9.mm,-9.mm,188.mm], [9.mm,-9.mm,188.mm], [9.mm,9.mm,188.mm], [-9.mm,9.mm,188.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke web (bot)
  grp = ents.add_group
  grp.name = "In yoke web (bot)"
  face = grp.entities.add_face([-8.mm,-17.mm,164.mm], [8.mm,-17.mm,164.mm], [8.mm,-9.mm,164.mm], [-8.mm,-9.mm,164.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(36.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # Stub-to-frame plate (bot)
  grp = ents.add_group
  grp.name = "Stub-to-frame plate (bot)"
  face = grp.entities.add_face([-10.mm,40.mm,160.mm], [60.mm,40.mm,160.mm], [60.mm,50.mm,160.mm], [-10.mm,50.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Stub-to-frame plate (bot)"] || model.materials.add("Stub-to-frame plate (bot)")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Bottom Corner"
  inst.layer = model.layers["Bottom Corner"]

  # ═══ Top Corner ═══
  defn = model.definitions.add("Top Corner")
  ents = defn.entities
  # Depth slide rail Y (~2.2m) (top)
  grp = ents.add_group
  grp.name = "Depth slide rail Y (~2.2m) (top)"
  face = grp.entities.add_face([-10.mm,-1000.mm,2372.mm], [10.mm,-1000.mm,2372.mm], [10.mm,1000.mm,2372.mm], [-10.mm,1000.mm,2372.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Depth slide rail Y (~2.2m) (bot)"] || model.materials.add("Depth slide rail Y (~2.2m) (bot)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Depth carriage body (top)
  grp = ents.add_group
  grp.name = "Depth carriage body (top)"
  face = grp.entities.add_face([-22.mm,-30.mm,2356.mm], [22.mm,-30.mm,2356.mm], [22.mm,30.mm,2356.mm], [-22.mm,30.mm,2356.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Depth grip tab L (top)
  grp = ents.add_group
  grp.name = "Depth grip tab L (top)"
  face = grp.entities.add_face([-20.mm,-30.mm,2371.mm], [-12.mm,-30.mm,2371.mm], [-12.mm,30.mm,2371.mm], [-20.mm,30.mm,2371.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(17.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Depth grip tab R (top)
  grp = ents.add_group
  grp.name = "Depth grip tab R (top)"
  face = grp.entities.add_face([12.mm,-30.mm,2371.mm], [20.mm,-30.mm,2371.mm], [20.mm,30.mm,2371.mm], [12.mm,30.mm,2371.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(17.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Depth cam clamp body (top)
  grp = ents.add_group
  grp.name = "Depth cam clamp body (top)"
  face = grp.entities.add_face([22.mm,30.mm,2354.mm], [36.mm,30.mm,2354.mm], [36.mm,44.mm,2354.mm], [22.mm,44.mm,2354.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Depth clamp lever (top)
  grp = ents.add_group
  grp.name = "Depth clamp lever (top)"
  ge = grp.entities
  circle = ge.add_circle([28.mm,44.mm,2361.mm], [0,1,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical slide rail Z (top)
  grp = ents.add_group
  grp.name = "Vertical slide rail Z (top)"
  face = grp.entities.add_face([-34.mm,-6.mm,2038.mm], [-24.mm,-6.mm,2038.mm], [-24.mm,6.mm,2038.mm], [-34.mm,6.mm,2038.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(330.mm)
  mat = model.materials["Depth slide rail Y (~2.2m) (bot)"] || model.materials.add("Depth slide rail Y (~2.2m) (bot)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical carriage body (top)
  grp = ents.add_group
  grp.name = "Vertical carriage body (top)"
  face = grp.entities.add_face([-44.mm,-12.mm,2206.mm], [-18.mm,-12.mm,2206.mm], [-18.mm,12.mm,2206.mm], [-44.mm,12.mm,2206.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical grip tab F (top)
  grp = ents.add_group
  grp.name = "Vertical grip tab F (top)"
  face = grp.entities.add_face([-44.mm,-15.mm,2208.mm], [-18.mm,-15.mm,2208.mm], [-18.mm,-6.mm,2208.mm], [-44.mm,-6.mm,2208.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical grip tab B (top)
  grp = ents.add_group
  grp.name = "Vertical grip tab B (top)"
  face = grp.entities.add_face([-44.mm,6.mm,2208.mm], [-18.mm,6.mm,2208.mm], [-18.mm,15.mm,2208.mm], [-44.mm,15.mm,2208.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Depth carriage body (bot)"] || model.materials.add("Depth carriage body (bot)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical cam clamp body (top)
  grp = ents.add_group
  grp.name = "Vertical cam clamp body (top)"
  face = grp.entities.add_face([-47.mm,26.mm,2216.mm], [-33.mm,26.mm,2216.mm], [-33.mm,40.mm,2216.mm], [-47.mm,40.mm,2216.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical clamp lever (top)
  grp = ents.add_group
  grp.name = "Vertical clamp lever (top)"
  ge = grp.entities
  circle = ge.add_circle([-33.mm,40.mm,2223.mm], [0,1,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Depth cam clamp body (bot)"] || model.materials.add("Depth cam clamp body (bot)")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage bracket to X-slide (top)
  grp = ents.add_group
  grp.name = "Carriage bracket to X-slide (top)"
  face = grp.entities.add_face([-30.mm,-8.mm,2216.mm], [4.mm,-8.mm,2216.mm], [4.mm,8.mm,2216.mm], [-30.mm,8.mm,2216.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Floating X slide (top)
  grp = ents.add_group
  grp.name = "Floating X slide (top)"
  face = grp.entities.add_face([-24.mm,-11.mm,2220.mm], [24.mm,-11.mm,2220.mm], [24.mm,11.mm,2220.mm], [-24.mm,11.mm,2220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint cross (top)
  grp = ents.add_group
  grp.name = "U-joint cross (top)"
  face = grp.entities.add_face([-10.mm,-10.mm,2196.mm], [10.mm,-10.mm,2196.mm], [10.mm,10.mm,2196.mm], [-10.mm,10.mm,2196.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["U-joint cross (bot)"] || model.materials.add("U-joint cross (bot)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt pin X (top)
  grp = ents.add_group
  grp.name = "Tilt pin X (top)"
  ge = grp.entities
  circle = ge.add_circle([-26.mm,-4.mm,2206.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(52.mm)
  mat = model.materials["Tilt pin X (bot)"] || model.materials.add("Tilt pin X (bot)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing pin Z (top)
  grp = ents.add_group
  grp.name = "Swing pin Z (top)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,4.mm,2190.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Tilt pin X (bot)"] || model.materials.add("Tilt pin X (bot)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke ear L (top)
  grp = ents.add_group
  grp.name = "Out yoke ear L (top)"
  face = grp.entities.add_face([-30.mm,-10.mm,2196.mm], [-22.mm,-10.mm,2196.mm], [-22.mm,10.mm,2196.mm], [-30.mm,10.mm,2196.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke ear R (top)
  grp = ents.add_group
  grp.name = "Out yoke ear R (top)"
  face = grp.entities.add_face([22.mm,-10.mm,2196.mm], [30.mm,-10.mm,2196.mm], [30.mm,10.mm,2196.mm], [22.mm,10.mm,2196.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke web (top)
  grp = ents.add_group
  grp.name = "Out yoke web (top)"
  face = grp.entities.add_face([-30.mm,10.mm,2198.mm], [30.mm,10.mm,2198.mm], [30.mm,18.mm,2198.mm], [-30.mm,18.mm,2198.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke stub (top)
  grp = ents.add_group
  grp.name = "Out yoke stub (top)"
  face = grp.entities.add_face([-6.mm,17.mm,2200.mm], [6.mm,17.mm,2200.mm], [6.mm,47.mm,2200.mm], [-6.mm,47.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Carriage bracket to X-slide (bot)"] || model.materials.add("Carriage bracket to X-slide (bot)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke ear Lo (top)
  grp = ents.add_group
  grp.name = "In yoke ear Lo (top)"
  face = grp.entities.add_face([-9.mm,-9.mm,2212.mm], [9.mm,-9.mm,2212.mm], [9.mm,9.mm,2212.mm], [-9.mm,9.mm,2212.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke ear Hi (top)
  grp = ents.add_group
  grp.name = "In yoke ear Hi (top)"
  face = grp.entities.add_face([-9.mm,-9.mm,2188.mm], [9.mm,-9.mm,2188.mm], [9.mm,9.mm,2188.mm], [-9.mm,9.mm,2188.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke web (top)
  grp = ents.add_group
  grp.name = "In yoke web (top)"
  face = grp.entities.add_face([-8.mm,-17.mm,2188.mm], [8.mm,-17.mm,2188.mm], [8.mm,-9.mm,2188.mm], [-8.mm,-9.mm,2188.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(36.mm)
  mat = model.materials["Floating X slide (bot)"] || model.materials.add("Floating X slide (bot)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # Stub-to-frame plate (top)
  grp = ents.add_group
  grp.name = "Stub-to-frame plate (top)"
  face = grp.entities.add_face([-10.mm,40.mm,2168.mm], [60.mm,40.mm,2168.mm], [60.mm,50.mm,2168.mm], [-10.mm,50.mm,2168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Stub-to-frame plate (bot)"] || model.materials.add("Stub-to-frame plate (bot)")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Top Corner"
  inst.layer = model.layers["Top Corner"]

  # ═══ Film Plane ═══
  defn = model.definitions.add("Film Plane")
  ents = defn.entities
  # Frame angle web
  grp = ents.add_group
  grp.name = "Frame angle web"
  face = grp.entities.add_face([-5.mm,50.mm,150.mm], [0.mm,50.mm,150.mm], [0.mm,100.mm,150.mm], [-5.mm,100.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2088.mm)
  mat = model.materials["Stub-to-frame plate (bot)"] || model.materials.add("Stub-to-frame plate (bot)")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame angle flange
  grp = ents.add_group
  grp.name = "Frame angle flange"
  face = grp.entities.add_face([-5.mm,50.mm,150.mm], [45.mm,50.mm,150.mm], [45.mm,55.mm,150.mm], [-5.mm,55.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2088.mm)
  mat = model.materials["Stub-to-frame plate (bot)"] || model.materials.add("Stub-to-frame plate (bot)")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Film plane (ghost)
  grp = ents.add_group
  grp.name = "Film plane (ghost)"
  face = grp.entities.add_face([0.mm,53.mm,150.mm], [620.mm,53.mm,150.mm], [620.mm,57.mm,150.mm], [0.mm,57.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2088.mm)
  mat = model.materials["Film plane (ghost)"] || model.materials.add("Film plane (ghost)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane"
  inst.layer = model.layers["Film Plane"]


# ── "Labeled" scene callouts (Labels tag) ──

tt = entities.add_text("CEILING rail — TOP corners HANG = TENSION", Geom::Point3d.new(0.mm, -170.mm, 2388.mm), Geom::Vector3d.new(40.mm, -60.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("FLOOR rail — BOTTOM corners BEAR = COMPRESSION", Geom::Point3d.new(0.mm, -170.mm, 0.mm), Geom::Vector3d.new(40.mm, -60.mm, -30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("NO screws / handwheels — PUSH to slide, CAM-CLAMP to lock", Geom::Point3d.new(0.mm, 300.mm, 1494.mm), Geom::Vector3d.new(55.mm, 50.mm, 20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Single U-joint (Ruland US12-6-6-SS) — tilt X + swing Z", Geom::Point3d.new(-30.mm, -4.mm, 200.mm), Geom::Vector3d.new(-60.mm, -40.mm, 10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Depth friction slide (~2.2m) + cam clamp", Geom::Point3d.new(22.mm, 400.mm, 156.mm), Geom::Vector3d.new(55.mm, 45.mm, 0.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Vertical friction slide + cam clamp", Geom::Point3d.new(-36.mm, 40.mm, 260.mm), Geom::Vector3d.new(-60.mm, -45.mm, 0.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Floating X slide (free)", Geom::Point3d.new(24.mm, 0.mm, 170.mm), Geom::Vector3d.new(55.mm, 45.mm, 0.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film plane 4499 x 2088 (mechanism ~150 top + bottom)", Geom::Point3d.new(300.mm, 53.mm, 1194.mm), Geom::Vector3d.new(60.mm, 45.mm, 0.mm))
tt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Bottom Corner", "Top Corner", "Film Plane", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

dir = Geom::Vector3d.new(0.55, -0.72, 0.30); dir.normalize!
[["Overview", ["Bottom Corner", "Top Corner", "Film Plane"], nil], ["Bottom Corner", ["Bottom Corner", "Film Plane"], [0.mm, 0.mm, 150.mm, 360.mm]], ["Top Corner", ["Top Corner", "Film Plane"], [0.mm, 0.mm, 2238.mm, 360.mm]], ["Labeled", ["Bottom Corner", "Top Corner", "Film Plane", "Labels"], nil]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.55, -0.72, 0.30); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
    ctr = model.bounds.center
    eye = ctr.offset(dir, model.bounds.diagonal * 1.4)
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
