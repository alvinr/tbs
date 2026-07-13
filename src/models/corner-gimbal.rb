# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner Gimbal", true)
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
  model.layers.add("Cross-Slide") unless model.layers["Cross-Slide"]
  model.layers.add("Gimbal") unless model.layers["Gimbal"]
  model.layers.add("Frame") unless model.layers["Frame"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Rail & Carriage ═══
  defn = model.definitions.add("Rail & Carriage")
  ents = defn.entities
  # Depth Rail HGR20
  grp = ents.add_group
  grp.name = "Depth Rail HGR20"
  face = grp.entities.add_face([-12.mm,-190.mm,0.mm], [12.mm,-190.mm,0.mm], [12.mm,190.mm,0.mm], [-12.mm,190.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Depth Rail HGR20"] || model.materials.add("Depth Rail HGR20")
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

  # ═══ Cross-Slide ═══
  defn = model.definitions.add("Cross-Slide")
  ents = defn.entities
  # X Cross-Slide (float)
  grp = ents.add_group
  grp.name = "X Cross-Slide (float)"
  face = grp.entities.add_face([-34.mm,-16.mm,42.mm], [34.mm,-16.mm,42.mm], [34.mm,16.mm,42.mm], [-34.mm,16.mm,42.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Z Cross-Slide (float)
  grp = ents.add_group
  grp.name = "Z Cross-Slide (float)"
  face = grp.entities.add_face([-30.mm,-14.mm,50.mm], [30.mm,-14.mm,50.mm], [30.mm,14.mm,50.mm], [-30.mm,14.mm,50.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Z Cross-Slide (float)"] || model.materials.add("Z Cross-Slide (float)")
  mat.color = Sketchup::Color.new(184, 200, 216)
  mat.alpha = 1.0
  grp.material = mat

  # Slide Yoke Lug L
  grp = ents.add_group
  grp.name = "Slide Yoke Lug L"
  face = grp.entities.add_face([-34.mm,-11.mm,58.mm], [-22.mm,-11.mm,58.mm], [-22.mm,11.mm,58.mm], [-34.mm,11.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Slide Yoke Lug R
  grp = ents.add_group
  grp.name = "Slide Yoke Lug R"
  face = grp.entities.add_face([22.mm,-11.mm,58.mm], [34.mm,-11.mm,58.mm], [34.mm,11.mm,58.mm], [22.mm,11.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Cross-Slide"
  inst.layer = model.layers["Cross-Slide"]

  # ═══ Gimbal Joint ═══
  defn = model.definitions.add("Gimbal Joint")
  ents = defn.entities
  # Gimbal Block
  grp = ents.add_group
  grp.name = "Gimbal Block"
  face = grp.entities.add_face([-18.mm,-18.mm,60.mm], [18.mm,-18.mm,60.mm], [18.mm,18.mm,60.mm], [-18.mm,18.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(54.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Pin O24 (shoulder bolt)
  grp = ents.add_group
  grp.name = "Tilt Pin O24 (shoulder bolt)"
  ge = grp.entities
  circle = ge.add_circle([-36.mm,0.mm,74.mm], [1,0,0], 12.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(72.mm)
  mat = model.materials["Tilt Pin O24 (shoulder bolt)"] || model.materials.add("Tilt Pin O24 (shoulder bolt)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Pin Head
  grp = ents.add_group
  grp.name = "Tilt Pin Head"
  face = grp.entities.add_face([-42.mm,-14.mm,60.mm], [-36.mm,-14.mm,60.mm], [-36.mm,14.mm,60.mm], [-42.mm,14.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Tilt Pin O24 (shoulder bolt)"] || model.materials.add("Tilt Pin O24 (shoulder bolt)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Pin Nut
  grp = ents.add_group
  grp.name = "Tilt Pin Nut"
  face = grp.entities.add_face([36.mm,-13.mm,61.mm], [44.mm,-13.mm,61.mm], [44.mm,13.mm,61.mm], [36.mm,13.mm,61.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Tilt Pin Nut"] || model.materials.add("Tilt Pin Nut")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Bushing L
  grp = ents.add_group
  grp.name = "Tilt Bushing L"
  ge = grp.entities
  circle = ge.add_circle([-24.mm,0.mm,74.mm], [1,0,0], 15.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(6.mm)
  mat = model.materials["Tilt Bushing L"] || model.materials.add("Tilt Bushing L")
  mat.color = Sketchup::Color.new(90, 62, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Bushing R
  grp = ents.add_group
  grp.name = "Tilt Bushing R"
  ge = grp.entities
  circle = ge.add_circle([18.mm,0.mm,74.mm], [1,0,0], 15.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(6.mm)
  mat = model.materials["Tilt Bushing L"] || model.materials.add("Tilt Bushing L")
  mat.color = Sketchup::Color.new(90, 62, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Pin O24 (shoulder bolt)
  grp = ents.add_group
  grp.name = "Swing Pin O24 (shoulder bolt)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,0.mm,90.mm], [0,0,1], 12.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(40.mm)
  mat = model.materials["Tilt Pin O24 (shoulder bolt)"] || model.materials.add("Tilt Pin O24 (shoulder bolt)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Pin Head
  grp = ents.add_group
  grp.name = "Swing Pin Head"
  face = grp.entities.add_face([-14.mm,-14.mm,130.mm], [14.mm,-14.mm,130.mm], [14.mm,14.mm,130.mm], [-14.mm,14.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Tilt Pin O24 (shoulder bolt)"] || model.materials.add("Tilt Pin O24 (shoulder bolt)")
  mat.color = Sketchup::Color.new(176, 112, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Pin Nut
  grp = ents.add_group
  grp.name = "Swing Pin Nut"
  face = grp.entities.add_face([-13.mm,-13.mm,82.mm], [13.mm,-13.mm,82.mm], [13.mm,13.mm,82.mm], [-13.mm,13.mm,82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Tilt Pin Nut"] || model.materials.add("Tilt Pin Nut")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Swing Bushing
  grp = ents.add_group
  grp.name = "Swing Bushing"
  ge = grp.entities
  circle = ge.add_circle([0.mm,0.mm,118.mm], [0,0,1], 15.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(8.mm)
  mat = model.materials["Tilt Bushing L"] || model.materials.add("Tilt Bushing L")
  mat.color = Sketchup::Color.new(90, 62, 0)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Gimbal Joint"
  inst.layer = model.layers["Gimbal"]

  # ═══ Frame Corner ═══
  defn = model.definitions.add("Frame Corner")
  ents = defn.entities
  # Frame Yoke Back
  grp = ents.add_group
  grp.name = "Frame Yoke Back"
  face = grp.entities.add_face([-16.mm,18.mm,84.mm], [16.mm,18.mm,84.mm], [16.mm,26.mm,84.mm], [-16.mm,26.mm,84.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(52.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Yoke Lug Lower
  grp = ents.add_group
  grp.name = "Frame Yoke Lug Lower"
  face = grp.entities.add_face([-16.mm,-6.mm,84.mm], [16.mm,-6.mm,84.mm], [16.mm,18.mm,84.mm], [-16.mm,18.mm,84.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Yoke Lug Upper
  grp = ents.add_group
  grp.name = "Frame Yoke Lug Upper"
  face = grp.entities.add_face([-16.mm,-6.mm,130.mm], [16.mm,-6.mm,130.mm], [16.mm,18.mm,130.mm], [-16.mm,18.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["X Cross-Slide (float)"] || model.materials.add("X Cross-Slide (float)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle vert leg
  grp = ents.add_group
  grp.name = "Frame Angle vert leg"
  face = grp.entities.add_face([-5.mm,22.mm,144.mm], [45.mm,22.mm,144.mm], [45.mm,27.mm,144.mm], [-5.mm,27.mm,144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(300.mm)
  mat = model.materials["Frame Angle vert leg"] || model.materials.add("Frame Angle vert leg")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle vert flange
  grp = ents.add_group
  grp.name = "Frame Angle vert flange"
  face = grp.entities.add_face([-5.mm,22.mm,144.mm], [0.mm,22.mm,144.mm], [0.mm,72.mm,144.mm], [-5.mm,72.mm,144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(300.mm)
  mat = model.materials["Frame Angle vert leg"] || model.materials.add("Frame Angle vert leg")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle horiz leg
  grp = ents.add_group
  grp.name = "Frame Angle horiz leg"
  face = grp.entities.add_face([-5.mm,22.mm,144.mm], [315.mm,22.mm,144.mm], [315.mm,27.mm,144.mm], [-5.mm,27.mm,144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame Angle vert leg"] || model.materials.add("Frame Angle vert leg")
  mat.color = Sketchup::Color.new(42, 107, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Frame Angle horiz flange
  grp = ents.add_group
  grp.name = "Frame Angle horiz flange"
  face = grp.entities.add_face([-5.mm,22.mm,144.mm], [315.mm,22.mm,144.mm], [315.mm,72.mm,144.mm], [-5.mm,72.mm,144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Frame Angle vert leg"] || model.materials.add("Frame Angle vert leg")
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
  face = grp.entities.add_face([0.mm,27.mm,144.mm], [900.mm,27.mm,144.mm], [900.mm,31.mm,144.mm], [0.mm,31.mm,144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(750.mm)
  mat = model.materials["Film Plane (ACM, ghost quarter)"] || model.materials.add("Film Plane (ACM, ghost quarter)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.22
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane"
  inst.layer = model.layers["Film Plane"]


# ── "Labeled" scene callouts (Labels tag) ──

tt = entities.add_text("TILT pin O24 (horizontal)", Geom::Point3d.new(36.mm, 0.mm, 74.mm), Geom::Vector3d.new(70.mm, -40.mm, -30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("SWING pin O24 (vertical)", Geom::Point3d.new(0.mm, 0.mm, 130.mm), Geom::Vector3d.new(60.mm, 40.mm, 40.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Gimbal block (2 offset bores)", Geom::Point3d.new(18.mm, -18.mm, 90.mm), Geom::Vector3d.new(60.mm, -50.mm, 0.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Floating X-Z cross-slide", Geom::Point3d.new(-30.mm, -16.mm, 50.mm), Geom::Vector3d.new(-60.mm, -40.mm, -10.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Depth rail (travel = depth)", Geom::Point3d.new(0.mm, 180.mm, 9.mm), Geom::Vector3d.new(20.mm, 60.mm, 20.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film frame (2x2 angle) + ACM", Geom::Point3d.new(20.mm, 27.mm, 250.mm), Geom::Vector3d.new(60.mm, 40.mm, 40.mm))
tt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Rail & Carriage", "Cross-Slide", "Gimbal", "Frame", "Film Plane", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

dir = Geom::Vector3d.new(0.55, -0.72, 0.42); dir.normalize!
[["Overview", ["Rail & Carriage", "Cross-Slide", "Gimbal", "Frame", "Film Plane"], nil], ["Joint Detail", ["Cross-Slide", "Gimbal", "Frame"], [0.mm, 0.mm, 95.mm, 320.mm]], ["Labeled", ["Rail & Carriage", "Cross-Slide", "Gimbal", "Frame", "Film Plane", "Labels"], nil]].each { |name, tags, tgt|
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
{ success: true, model: "Film-Plane Corner Gimbal",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
