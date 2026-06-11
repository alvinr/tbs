model = Sketchup.active_model
model.start_operation("TBS-001 Fold-down Chem Shelf Study", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1
to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Equipment") unless model.layers["Equipment"]
  model.layers.add("Shelf Deployed") unless model.layers["Shelf Deployed"]
  model.layers.add("Shelf Stowed") unless model.layers["Shelf Stowed"]
  model.layers.add("Evap") unless model.layers["Evap"]
  model.layers.add("Tap") unless model.layers["Tap"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([900.mm,0.mm,-40.mm], [2500.mm,0.mm,-40.mm], [2500.mm,700.mm,-40.mm], [900.mm,700.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.22
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([900.mm,0.mm,2388.mm], [2500.mm,0.mm,2388.mm], [2500.mm,700.mm,2388.mm], [900.mm,700.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.08
  grp.material = mat

  # Pinhole wall (context)
  grp = ents.add_group
  grp.name = "Pinhole wall (context)"
  face = grp.entities.add_face([900.mm,-40.mm,0.mm], [2500.mm,-40.mm,0.mm], [2500.mm,0.mm,0.mm], [900.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole wall (context)"] || model.materials.add("Pinhole wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # Widened walkway grate (Z115-130)
  grp = ents.add_group
  grp.name = "Widened walkway grate (Z115-130)"
  face = grp.entities.add_face([1155.mm,0.mm,115.mm], [2629.mm,0.mm,115.mm], [2629.mm,500.mm,115.mm], [1155.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Widened walkway grate (Z115-130)"] || model.materials.add("Widened walkway grate (Z115-130)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 0.6
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ Pinhole-wall equipment ═══
  defn = model.definitions.add("Pinhole-wall equipment")
  ents = defn.entities
  # Battery bank (X1810-2310, Z150-650)
  grp = ents.add_group
  grp.name = "Battery bank (X1810-2310, Z150-650)"
  face = grp.entities.add_face([1810.mm,0.mm,150.mm], [2310.mm,0.mm,150.mm], [2310.mm,120.mm,150.mm], [1810.mm,120.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery bank (X1810-2310, Z150-650)"] || model.materials.add("Battery bank (X1810-2310, Z150-650)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.5
  grp.material = mat

  # Electrical panel (Z1500-2100)
  grp = ents.add_group
  grp.name = "Electrical panel (Z1500-2100)"
  face = grp.entities.add_face([1910.mm,0.mm,1500.mm], [2210.mm,0.mm,1500.mm], [2210.mm,160.mm,1500.mm], [1910.mm,160.mm,1500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(600.mm)
  mat = model.materials["Electrical panel (Z1500-2100)"] || model.materials.add("Electrical panel (Z1500-2100)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 0.4
  grp.material = mat

  # Power panel (flush, high)
  grp = ents.add_group
  grp.name = "Power panel (flush, high)"
  face = grp.entities.add_face([1250.mm,0.mm,1830.mm], [1590.mm,0.mm,1830.mm], [1590.mm,6.mm,1830.mm], [1250.mm,6.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Power panel (flush, high)"] || model.materials.add("Power panel (flush, high)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 0.35
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole-wall equipment"
  inst.layer = model.layers["Equipment"]

  # ═══ Chem Shelf (deployed) ═══
  defn = model.definitions.add("Chem Shelf (deployed)")
  ents = defn.entities
  # Chem shelf board (deployed)
  grp = ents.add_group
  grp.name = "Chem shelf board (deployed)"
  face = grp.entities.add_face([1180.mm,0.mm,1050.mm], [1780.mm,0.mm,1050.mm], [1780.mm,300.mm,1050.mm], [1180.mm,300.mm,1050.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Chem shelf board (deployed)"] || model.materials.add("Chem shelf board (deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Lip front
  grp = ents.add_group
  grp.name = "Lip front"
  face = grp.entities.add_face([1180.mm,294.mm,1075.mm], [1780.mm,294.mm,1075.mm], [1780.mm,300.mm,1075.mm], [1180.mm,300.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem shelf board (deployed)"] || model.materials.add("Chem shelf board (deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Lip end
  grp = ents.add_group
  grp.name = "Lip end"
  face = grp.entities.add_face([1180.mm,0.mm,1075.mm], [1186.mm,0.mm,1075.mm], [1186.mm,300.mm,1075.mm], [1180.mm,300.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem shelf board (deployed)"] || model.materials.add("Chem shelf board (deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Lip end
  grp = ents.add_group
  grp.name = "Lip end"
  face = grp.entities.add_face([1774.mm,0.mm,1075.mm], [1780.mm,0.mm,1075.mm], [1780.mm,300.mm,1075.mm], [1774.mm,300.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem shelf board (deployed)"] || model.materials.add("Chem shelf board (deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Piano hinge (back edge)
  grp = ents.add_group
  grp.name = "Piano hinge (back edge)"
  ge = grp.entities
  circle = ge.add_circle([1180.mm,0.mm,1069.mm], [1,0,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(600.mm)
  mat = model.materials["Piano hinge (back edge)"] || model.materials.add("Piano hinge (back edge)")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Stay X1205
  grp = ents.add_group
  grp.name = "Stay X1205"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 290.mm, -230.mm)
  circle = ge.add_circle([1205.mm,0.mm,1305.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Piano hinge (back edge)"] || model.materials.add("Piano hinge (back edge)")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Stay wall anchor
  grp = ents.add_group
  grp.name = "Stay wall anchor"
  face = grp.entities.add_face([1193.mm,0.mm,1293.mm], [1217.mm,0.mm,1293.mm], [1217.mm,8.mm,1293.mm], [1193.mm,8.mm,1293.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge (back edge)"] || model.materials.add("Piano hinge (back edge)")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Stay X1755
  grp = ents.add_group
  grp.name = "Stay X1755"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 290.mm, -230.mm)
  circle = ge.add_circle([1755.mm,0.mm,1305.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Piano hinge (back edge)"] || model.materials.add("Piano hinge (back edge)")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Stay wall anchor
  grp = ents.add_group
  grp.name = "Stay wall anchor"
  face = grp.entities.add_face([1743.mm,0.mm,1293.mm], [1767.mm,0.mm,1293.mm], [1767.mm,8.mm,1293.mm], [1743.mm,8.mm,1293.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge (back edge)"] || model.materials.add("Piano hinge (back edge)")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Chem Shelf (deployed)"
  inst.layer = model.layers["Shelf Deployed"]

  # ═══ Chem Shelf (stowed) ═══
  defn = model.definitions.add("Chem Shelf (stowed)")
  ents = defn.entities
  # Chem shelf board (stowed/transport)
  grp = ents.add_group
  grp.name = "Chem shelf board (stowed/transport)"
  face = grp.entities.add_face([1180.mm,0.mm,1075.mm], [1780.mm,0.mm,1075.mm], [1780.mm,25.mm,1075.mm], [1180.mm,25.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(300.mm)
  mat = model.materials["Chem shelf board (stowed/transport)"] || model.materials.add("Chem shelf board (stowed/transport)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 0.35
  grp.material = mat

  # Transport latch
  grp = ents.add_group
  grp.name = "Transport latch"
  face = grp.entities.add_face([1450.mm,0.mm,1345.mm], [1510.mm,0.mm,1345.mm], [1510.mm,18.mm,1345.mm], [1450.mm,18.mm,1345.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Transport latch"] || model.materials.add("Transport latch")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 0.6
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Chem Shelf (stowed)"
  inst.layer = model.layers["Shelf Stowed"]

  # ═══ Evap cooler (ghost) ═══
  defn = model.definitions.add("Evap cooler (ghost)")
  ents = defn.entities
  # Evap cooler (stow, top Z950)
  grp = ents.add_group
  grp.name = "Evap cooler (stow, top Z950)"
  face = grp.entities.add_face([1450.mm,0.mm,150.mm], [2050.mm,0.mm,150.mm], [2050.mm,350.mm,150.mm], [1450.mm,350.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(800.mm)
  mat = model.materials["Evap cooler (stow, top Z950)"] || model.materials.add("Evap cooler (stow, top Z950)")
  mat.color = Sketchup::Color.new(154, 176, 192)
  mat.alpha = 0.3
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Evap cooler (ghost)"
  inst.layer = model.layers["Evap"]

  # ═══ TAP-01 (relocated) ═══
  defn = model.definitions.add("TAP-01 (relocated)")
  ents = defn.entities
  # Tap branch riser (3/4 HDPE)
  grp = ents.add_group
  grp.name = "Tap branch riser (3/4 HDPE)"
  ge = grp.entities
  circle = ge.add_circle([1130.mm,18.mm,850.mm], [0,0,1], 12.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(525.mm)
  mat = model.materials["Tap branch riser (3/4 HDPE)"] || model.materials.add("Tap branch riser (3/4 HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-06 (blue isolation)
  grp = ents.add_group
  grp.name = "BV-06 (blue isolation)"
  face = grp.entities.add_face([1112.mm,4.mm,1010.mm], [1148.mm,4.mm,1010.mm], [1148.mm,40.mm,1010.mm], [1112.mm,40.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Piano hinge (back edge)"] || model.materials.add("Piano hinge (back edge)")
  mat.color = Sketchup::Color.new(112, 120, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Tap spout (out)
  grp = ents.add_group
  grp.name = "Tap spout (out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 92.mm, 0.mm)
  circle = ge.add_circle([1130.mm,18.mm,1375.mm], vec, 10.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Tap branch riser (3/4 HDPE)"] || model.materials.add("Tap branch riser (3/4 HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tap spout (down)
  grp = ents.add_group
  grp.name = "Tap spout (down)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -225.mm)
  circle = ge.add_circle([1130.mm,110.mm,1375.mm], vec, 10.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Tap branch riser (3/4 HDPE)"] || model.materials.add("Tap branch riser (3/4 HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "TAP-01 (relocated)"
  inst.layer = model.layers["Tap"]


anc = Geom::Point3d.new(1480.mm, 300.mm, 1075.mm)
txt = entities.add_text("CHEM SHELF — fold-down
(deployed, Z1075 = 945 above deck)", anc, Geom::Vector3d.new(-150.mm, 650.mm, 500.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1180.mm, 0.mm, 1075.mm)
txt = entities.add_text("PIANO HINGE on pinhole wall
(back edge, Z1075)", anc, Geom::Vector3d.new(-350.mm, -250.mm, 350.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1755.mm, 290.mm, 1075.mm)
txt = entities.add_text("STAY (carries the load)
folds flat when stowed", anc, Geom::Vector3d.new(250.mm, 450.mm, 350.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1480.mm, 25.mm, 1375.mm)
txt = entities.add_text("FOLDS UP for transport
(vertical, Z1075-1375)", anc, Geom::Vector3d.new(200.mm, -350.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1810.mm, 0.mm, 650.mm)
txt = entities.add_text("Battery bank
(shelf sits LEFT of it)", anc, Geom::Vector3d.new(350.mm, -350.mm, 350.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1750.mm, 350.mm, 950.mm)
txt = entities.add_text("Evap slides UNDER
(top Z950 < shelf Z1050)", anc, Geom::Vector3d.new(0.mm, 600.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1130.mm, 110.mm, 1375.mm)
txt = entities.add_text("TAP-01 RELOCATED
left of the shelf (X~1130)
top aligned w/ stowed shelf (Z1375)", anc, Geom::Vector3d.new(-350.mm, 350.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Context", "Equipment", "Shelf Deployed", "Shelf Stowed", "Evap", "Tap", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l| model.layers.remove(l, true) rescue nil unless l == default_layer || keep_tags.include?(l.name) }

model.layers.each { |l| l.visible = (l.name != "Labels") }
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(0.55, -0.74, 0.4); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
[["Combined", ["Context", "Equipment", "Shelf Deployed", "Shelf Stowed", "Evap", "Tap"]], ["Deployed (in use)", ["Context", "Equipment", "Shelf Deployed", "Evap", "Tap"]], ["Stowed (transport)", ["Context", "Equipment", "Shelf Stowed", "Evap", "Tap"]], ["Labeled", ["Context", "Equipment", "Shelf Deployed", "Shelf Stowed", "Evap", "Tap", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  page = model.pages.add(name); page.use_camera = true
}
model.layers.each { |l| l.visible = true }
model.commit_operation
{ success: true, model: "Fold-down Chem Shelf Study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   scenes: model.pages.count }.to_json
