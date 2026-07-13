# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner U-Joint", true)
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

  model.layers.add("Rail & Carriage") unless model.layers["Rail & Carriage"]
  model.layers.add("Z + X Stage") unless model.layers["Z + X Stage"]
  model.layers.add("U-Joint") unless model.layers["U-Joint"]
  model.layers.add("Frame") unless model.layers["Frame"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Rail & Carriage ═══
  defn = model.definitions.add("Rail & Carriage")
  ents = defn.entities
  # Depth Rail HGR20 (Y focus)
  grp = ents.add_group
  grp.name = "Depth Rail HGR20 (Y focus)"
  face = grp.entities.add_face([-12.mm,-190.mm,0.mm], [12.mm,-190.mm,0.mm], [12.mm,190.mm,0.mm], [-12.mm,190.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Depth Rail HGR20 (Y focus)"] || model.materials.add("Depth Rail HGR20 (Y focus)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage HGH20CA
  grp = ents.add_group
  grp.name = "Carriage HGH20CA"
  face = grp.entities.add_face([-22.mm,-34.mm,18.mm], [22.mm,-34.mm,18.mm], [22.mm,34.mm,18.mm], [-22.mm,34.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Carriage HGH20CA"] || model.materials.add("Carriage HGH20CA")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Rail & Carriage"
  inst.layer = model.layers["Rail & Carriage"]

  # ═══ Z + X Stage ═══
  defn = model.definitions.add("Z + X Stage")
  ents = defn.entities
  # Z screw base bearing
  grp = ents.add_group
  grp.name = "Z screw base bearing"
  face = grp.entities.add_face([-14.mm,-14.mm,38.mm], [14.mm,-14.mm,38.mm], [14.mm,14.mm,38.mm], [-14.mm,14.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Depth Rail HGR20 (Y focus)"] || model.materials.add("Depth Rail HGR20 (Y focus)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z leadscrew (driven)
  grp = ents.add_group
  grp.name = "Vertical Z leadscrew (driven)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,0.mm,42.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(116.mm)
  mat = model.materials["Vertical Z leadscrew (driven)"] || model.materials.add("Vertical Z leadscrew (driven)")
  mat.color = Sketchup::Color.new(144, 152, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Z drive nut (rides screw)
  grp = ents.add_group
  grp.name = "Z drive nut (rides screw)"
  face = grp.entities.add_face([-18.mm,-18.mm,86.mm], [18.mm,-18.mm,86.mm], [18.mm,18.mm,86.mm], [-18.mm,18.mm,86.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Z drive nut (rides screw)"] || model.materials.add("Z drive nut (rides screw)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Floating X slide
  grp = ents.add_group
  grp.name = "Floating X slide"
  face = grp.entities.add_face([-26.mm,-12.mm,104.mm], [26.mm,-12.mm,104.mm], [26.mm,12.mm,104.mm], [-26.mm,12.mm,104.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(7.mm)
  mat = model.materials["Floating X slide"] || model.materials.add("Floating X slide")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Z + X Stage"
  inst.layer = model.layers["Z + X Stage"]

  # ═══ U-Joint ═══
  defn = model.definitions.add("U-Joint")
  ents = defn.entities
  # U-joint cross block
  grp = ents.add_group
  grp.name = "U-joint cross block"
  face = grp.entities.add_face([-11.mm,-11.mm,119.mm], [11.mm,-11.mm,119.mm], [11.mm,11.mm,119.mm], [-11.mm,11.mm,119.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["U-joint cross block"] || model.materials.add("U-joint cross block")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt pin (X)
  grp = ents.add_group
  grp.name = "Tilt pin (X)"
  ge = grp.entities
  circle = ge.add_circle([-30.mm,-4.mm,130.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["Tilt pin (X)"] || model.materials.add("Tilt pin (X)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing pin (Z)
  grp = ents.add_group
  grp.name = "Swing pin (Z)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,4.mm,104.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(52.mm)
  mat = model.materials["Tilt pin (X)"] || model.materials.add("Tilt pin (X)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke ear L
  grp = ents.add_group
  grp.name = "Out yoke ear L"
  face = grp.entities.add_face([-30.mm,-10.mm,120.mm], [-20.mm,-10.mm,120.mm], [-20.mm,10.mm,120.mm], [-30.mm,10.mm,120.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Z drive nut (rides screw)"] || model.materials.add("Z drive nut (rides screw)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke ear R
  grp = ents.add_group
  grp.name = "Out yoke ear R"
  face = grp.entities.add_face([20.mm,-10.mm,120.mm], [30.mm,-10.mm,120.mm], [30.mm,10.mm,120.mm], [20.mm,10.mm,120.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Z drive nut (rides screw)"] || model.materials.add("Z drive nut (rides screw)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke web
  grp = ents.add_group
  grp.name = "Out yoke web"
  face = grp.entities.add_face([-30.mm,10.mm,122.mm], [30.mm,10.mm,122.mm], [30.mm,18.mm,122.mm], [-30.mm,18.mm,122.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Z drive nut (rides screw)"] || model.materials.add("Z drive nut (rides screw)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Out yoke stub
  grp = ents.add_group
  grp.name = "Out yoke stub"
  face = grp.entities.add_face([-6.mm,17.mm,124.mm], [6.mm,17.mm,124.mm], [6.mm,43.mm,124.mm], [-6.mm,43.mm,124.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Z drive nut (rides screw)"] || model.materials.add("Z drive nut (rides screw)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke ear Bot
  grp = ents.add_group
  grp.name = "In yoke ear Bot"
  face = grp.entities.add_face([-9.mm,-9.mm,104.mm], [9.mm,-9.mm,104.mm], [9.mm,9.mm,104.mm], [-9.mm,9.mm,104.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Floating X slide"] || model.materials.add("Floating X slide")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke ear Top
  grp = ents.add_group
  grp.name = "In yoke ear Top"
  face = grp.entities.add_face([-9.mm,-9.mm,146.mm], [9.mm,-9.mm,146.mm], [9.mm,9.mm,146.mm], [-9.mm,9.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Floating X slide"] || model.materials.add("Floating X slide")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke web
  grp = ents.add_group
  grp.name = "In yoke web"
  face = grp.entities.add_face([-8.mm,-17.mm,104.mm], [8.mm,-17.mm,104.mm], [8.mm,-9.mm,104.mm], [-8.mm,-9.mm,104.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(52.mm)
  mat = model.materials["Floating X slide"] || model.materials.add("Floating X slide")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # In yoke foot
  grp = ents.add_group
  grp.name = "In yoke foot"
  face = grp.entities.add_face([-12.mm,-16.mm,100.mm], [12.mm,-16.mm,100.mm], [12.mm,12.mm,100.mm], [-12.mm,12.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Floating X slide"] || model.materials.add("Floating X slide")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "U-Joint"
  inst.layer = model.layers["U-Joint"]

  # ═══ Frame Corner ═══
  defn = model.definitions.add("Frame Corner")
  ents = defn.entities
  # Stub-to-frame plate
  grp = ents.add_group
  grp.name = "Stub-to-frame plate"
  face = grp.entities.add_face([-10.mm,40.mm,100.mm], [60.mm,40.mm,100.mm], [60.mm,50.mm,100.mm], [-10.mm,50.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Stub-to-frame plate"] || model.materials.add("Stub-to-frame plate")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle vert web
  grp = ents.add_group
  grp.name = "Frame Angle vert web"
  face = grp.entities.add_face([-5.mm,50.mm,124.mm], [45.mm,50.mm,124.mm], [45.mm,55.mm,124.mm], [-5.mm,55.mm,124.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(300.mm)
  mat = model.materials["Stub-to-frame plate"] || model.materials.add("Stub-to-frame plate")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle vert flange
  grp = ents.add_group
  grp.name = "Frame Angle vert flange"
  face = grp.entities.add_face([-5.mm,50.mm,124.mm], [0.mm,50.mm,124.mm], [0.mm,100.mm,124.mm], [-5.mm,100.mm,124.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(300.mm)
  mat = model.materials["Stub-to-frame plate"] || model.materials.add("Stub-to-frame plate")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle horiz web
  grp = ents.add_group
  grp.name = "Frame Angle horiz web"
  face = grp.entities.add_face([-5.mm,50.mm,124.mm], [315.mm,50.mm,124.mm], [315.mm,55.mm,124.mm], [-5.mm,55.mm,124.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Stub-to-frame plate"] || model.materials.add("Stub-to-frame plate")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle horiz flange
  grp = ents.add_group
  grp.name = "Frame Angle horiz flange"
  face = grp.entities.add_face([-5.mm,50.mm,124.mm], [315.mm,50.mm,124.mm], [315.mm,100.mm,124.mm], [-5.mm,100.mm,124.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Stub-to-frame plate"] || model.materials.add("Stub-to-frame plate")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Frame Corner"
  inst.layer = model.layers["Frame"]

  # ═══ Film Plane ═══
  defn = model.definitions.add("Film Plane")
  ents = defn.entities
  # Film Plane (ACM, ghost quarter)
  grp = ents.add_group
  grp.name = "Film Plane (ACM, ghost quarter)"
  face = grp.entities.add_face([0.mm,55.mm,124.mm], [880.mm,55.mm,124.mm], [880.mm,59.mm,124.mm], [0.mm,59.mm,124.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(740.mm)
  mat = model.materials["Film Plane (ACM, ghost quarter)"] || model.materials.add("Film Plane (ACM, ghost quarter)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.22
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane"
  inst.layer = model.layers["Film Plane"]


# ── "Labeled" scene callouts (Labels tag) ──

tt = entities.add_text("Single U-joint (Ruland US12-6-6-SS, 45deg, off-the-shelf)", Geom::Point3d.new(0.mm, 4.mm, 156.mm), Geom::Vector3d.new(55.mm, 45.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("TILT pin (X, horizontal)", Geom::Point3d.new(30.mm, -4.mm, 130.mm), Geom::Vector3d.new(55.mm, -40.mm, 10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("SWING pin (Z, vertical)", Geom::Point3d.new(0.mm, 4.mm, 104.mm), Geom::Vector3d.new(-55.mm, 40.mm, -20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("DRIVEN vertical Z leadscrew (holds tilt travel)", Geom::Point3d.new(0.mm, 0.mm, 60.mm), Geom::Vector3d.new(-60.mm, -40.mm, -8.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Floating X slide (horizontal arc)", Geom::Point3d.new(-26.mm, 0.mm, 108.mm), Geom::Vector3d.new(-55.mm, -45.mm, 0.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Depth rail (Y) — focus", Geom::Point3d.new(0.mm, 180.mm, 9.mm), Geom::Vector3d.new(40.mm, 55.mm, 10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film frame (2x2 angle) + film plane", Geom::Point3d.new(40.mm, 55.mm, 250.mm), Geom::Vector3d.new(60.mm, 45.mm, 40.mm))
tt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Rail & Carriage", "Z + X Stage", "U-Joint", "Frame", "Film Plane", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

dir = Geom::Vector3d.new(0.55, -0.72, 0.42); dir.normalize!
[["Overview", ["Rail & Carriage", "Z + X Stage", "U-Joint", "Frame", "Film Plane"], nil], ["Joint Detail", ["Z + X Stage", "U-Joint", "Frame"], [0.mm, 0.mm, 130.mm, 300.mm]], ["Labeled", ["Rail & Carriage", "Z + X Stage", "U-Joint", "Frame", "Film Plane", "Labels"], nil]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.55, -0.72, 0.42); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
    ctr = model.bounds.center
    eye = ctr.offset(dir, model.bounds.diagonal * 1.5)
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Film-Plane Corner U-Joint",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
