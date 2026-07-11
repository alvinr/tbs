# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-002 Mini-TBS (ghosted boxes + clickable flaps)", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Sketchfab metadata — fill-only-if-blank; never overwrites existing values ──
model.name = "TBS-002" if model.name.to_s.strip.empty?
model.description = "A classroom-ready design for teaching pinhole photography \u2014 its process and its craft \u2014 to students from elementary school through college." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-002") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "A classroom-ready design for teaching pinhole photography \u2014 its process and its craft \u2014 to students from elementary school through college.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "4dc2aa302f884cb192da7c57725d4bf2") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

  model.layers.add("Boxes") unless model.layers["Boxes"]
  model.layers.add("Pinhole") unless model.layers["Pinhole"]
  model.layers.add("Shutter") unless model.layers["Shutter"]
  model.layers.add("Film Panel") unless model.layers["Film Panel"]
  model.layers.add("Prep Top Flaps") unless model.layers["Prep Top Flaps"]
  model.layers.add("Light Cone") unless model.layers["Light Cone"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Cardboard boxes (ghost) ═══
  defn = model.definitions.add("Cardboard boxes (ghost)")
  ents = defn.entities
  # Floor
  grp = ents.add_group
  grp.name = "Floor"
  face = grp.entities.add_face([0.mm,0.mm,-4.mm], [914.mm,0.mm,-4.mm], [914.mm,457.mm,-4.mm], [0.mm,457.mm,-4.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.16
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Side wall (near)
  grp = ents.add_group
  grp.name = "Side wall (near)"
  face = grp.entities.add_face([0.mm,-4.mm,0.mm], [914.mm,-4.mm,0.mm], [914.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(406.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.16
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Side wall (far)
  grp = ents.add_group
  grp.name = "Side wall (far)"
  face = grp.entities.add_face([0.mm,457.mm,0.mm], [914.mm,457.mm,0.mm], [914.mm,461.mm,0.mm], [0.mm,461.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(406.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.16
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Pinhole wall
  grp = ents.add_group
  grp.name = "Pinhole wall"
  face = grp.entities.add_face([-4.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,457.mm,0.mm], [-4.mm,457.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(406.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.16
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Duct-tape drip liner (optional)
  grp = ents.add_group
  grp.name = "Duct-tape drip liner (optional)"
  face = grp.entities.add_face([461.mm,60.mm,0.mm], [850.mm,60.mm,0.mm], [850.mm,397.mm,0.mm], [461.mm,397.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.mm)
  mat = model.materials["Duct-tape drip liner (optional)"] || model.materials.add("Duct-tape drip liner (optional)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 0.55
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Cardboard boxes (ghost)"
  inst.layer = model.layers["Boxes"]

  # ═══ Camera-box top (taped shut) ═══
  defn = model.definitions.add("Camera-box top (taped shut)")
  ents = defn.entities
  # Camera top flap (near)
  grp = ents.add_group
  grp.name = "Camera top flap (near)"
  face = grp.entities.add_face([0.mm,0.mm,403.mm], [457.mm,0.mm,403.mm], [457.mm,228.5.mm,403.mm], [0.mm,228.5.mm,403.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Camera top flap (near)"] || model.materials.add("Camera top flap (near)")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.14400000000000002
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Camera top flap (far)
  grp = ents.add_group
  grp.name = "Camera top flap (far)"
  face = grp.entities.add_face([0.mm,228.5.mm,403.mm], [457.mm,228.5.mm,403.mm], [457.mm,457.mm,403.mm], [0.mm,457.mm,403.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Camera top flap (near)"] || model.materials.add("Camera top flap (near)")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.14400000000000002
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Camera top tape (seam)
  grp = ents.add_group
  grp.name = "Camera top tape (seam)"
  face = grp.entities.add_face([0.mm,203.5.mm,406.mm], [457.mm,203.5.mm,406.mm], [457.mm,253.5.mm,406.mm], [0.mm,253.5.mm,406.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.5.mm)
  mat = model.materials["Camera top tape (seam)"] || model.materials.add("Camera top tape (seam)")
  mat.color = Sketchup::Color.new(138, 138, 138)
  mat.alpha = 0.85
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Camera-box top (taped shut)"
  inst.layer = model.layers["Boxes"]

  # ═══ End wall + arm sleeves ═══
  defn = model.definitions.add("End wall + arm sleeves")
  ents = defn.entities
  # End wall (arm-sleeve wall)
  grp = ents.add_group
  grp.name = "End wall (arm-sleeve wall)"
  face = grp.entities.add_face([910.mm,0.mm,0.mm], [914.mm,0.mm,0.mm], [914.mm,457.mm,0.mm], [910.mm,457.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(406.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 0.16
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Arm sleeve
  grp = ents.add_group
  grp.name = "Arm sleeve"
  ge = grp.entities
  circle = ge.add_circle([914.mm,113.5.mm,203.mm], [1,0,0], 51.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(130.mm)
  mat = model.materials["Arm sleeve"] || model.materials.add("Arm sleeve")
  mat.color = Sketchup::Color.new(72, 64, 96)
  mat.alpha = 0.9
  grp.material = mat

  # Arm sleeve
  grp = ents.add_group
  grp.name = "Arm sleeve"
  ge = grp.entities
  circle = ge.add_circle([914.mm,343.5.mm,203.mm], [1,0,0], 51.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(130.mm)
  mat = model.materials["Arm sleeve"] || model.materials.add("Arm sleeve")
  mat.color = Sketchup::Color.new(72, 64, 96)
  mat.alpha = 0.9
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "End wall + arm sleeves"
  inst.layer = model.layers["Boxes"]

  # ═══ Box-join tape ═══
  defn = model.definitions.add("Box-join tape")
  ents = defn.entities
  # Join tape (floor)
  grp = ents.add_group
  grp.name = "Join tape (floor)"
  face = grp.entities.add_face([432.mm,0.mm,-5.5.mm], [482.mm,0.mm,-5.5.mm], [482.mm,457.mm,-5.5.mm], [432.mm,457.mm,-5.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.5.mm)
  mat = model.materials["Join tape (floor)"] || model.materials.add("Join tape (floor)")
  mat.color = Sketchup::Color.new(138, 138, 138)
  mat.alpha = 0.9
  grp.material = mat

  # Join tape (top)
  grp = ents.add_group
  grp.name = "Join tape (top)"
  face = grp.entities.add_face([432.mm,0.mm,406.mm], [482.mm,0.mm,406.mm], [482.mm,457.mm,406.mm], [432.mm,457.mm,406.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.5.mm)
  mat = model.materials["Join tape (floor)"] || model.materials.add("Join tape (floor)")
  mat.color = Sketchup::Color.new(138, 138, 138)
  mat.alpha = 0.9
  grp.material = mat

  # Join tape (near)
  grp = ents.add_group
  grp.name = "Join tape (near)"
  face = grp.entities.add_face([432.mm,-5.5.mm,0.mm], [482.mm,-5.5.mm,0.mm], [482.mm,-4.mm,0.mm], [432.mm,-4.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(406.mm)
  mat = model.materials["Join tape (floor)"] || model.materials.add("Join tape (floor)")
  mat.color = Sketchup::Color.new(138, 138, 138)
  mat.alpha = 0.9
  grp.material = mat

  # Join tape (far)
  grp = ents.add_group
  grp.name = "Join tape (far)"
  face = grp.entities.add_face([432.mm,461.mm,0.mm], [482.mm,461.mm,0.mm], [482.mm,462.5.mm,0.mm], [432.mm,462.5.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(406.mm)
  mat = model.materials["Join tape (floor)"] || model.materials.add("Join tape (floor)")
  mat.color = Sketchup::Color.new(138, 138, 138)
  mat.alpha = 0.9
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Box-join tape"
  inst.layer = model.layers["Boxes"]

  # ═══ Pinhole ═══
  defn = model.definitions.add("Pinhole")
  ents = defn.entities
  # Pinhole plate (aluminum)
  grp = ents.add_group
  grp.name = "Pinhole plate (aluminum)"
  face = grp.entities.add_face([0.mm,203.5.mm,178.mm], [2.mm,203.5.mm,178.mm], [2.mm,253.5.mm,178.mm], [0.mm,253.5.mm,178.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole plate (aluminum)"] || model.materials.add("Pinhole plate (aluminum)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole Ø0.794mm
  grp = ents.add_group
  grp.name = "Pinhole Ø0.794mm"
  ge = grp.entities
  circle = ge.add_circle([-2.mm,228.5.mm,203.mm], [1,0,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(6.mm)
  mat = model.materials["Pinhole Ø0.794mm"] || model.materials.add("Pinhole Ø0.794mm")
  mat.color = Sketchup::Color.new(204, 102, 0)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole"
  inst.layer = model.layers["Pinhole"]


# ── Clickable dynamic components ──

# ═══ Shutter — DYNAMIC COMPONENT (click to move) ═══
sh_defn = model.definitions.add("Shutter")
ents = sh_defn.entities
  # Shutter flap
  grp = ents.add_group
  grp.name = "Shutter flap"
  face = grp.entities.add_face([0.mm,-45.mm,-90.mm], [2.mm,-45.mm,-90.mm], [2.mm,45.mm,-90.mm], [0.mm,45.mm,-90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Shutter flap"] || model.materials.add("Shutter flap")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

sh_inst = entities.add_instance(sh_defn, Geom::Transformation.translation([-6.mm, 228.5.mm, 248.mm]))
sh_inst.name = "Shutter"
sh_inst.layer = model.layers["Shutter"]
da = "dynamic_attributes"
[sh_defn, sh_inst].each do |e|
  e.set_attribute(da, "_name", "Shutter")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "lift", 1.0)
  e.set_attribute(da, "roty", 0.0)
end
sh_inst.set_attribute(da, "_lift_access", "VIEW")
sh_inst.set_attribute(da, "_lift_label", "Lift (0 closed / 1 open)")
sh_inst.set_attribute(da, "_roty_formula", "110*lift")
sh_inst.set_attribute(da, "onclick", 'ANIMATE("lift", 0, 1)')
sh_inst.set_attribute(da, "_onclick_access", "NONE")


# ═══ Film-plane panel — DYNAMIC COMPONENT (click to move) ═══
fp_defn = model.definitions.add("Film-plane panel")
ents = fp_defn.entities
  # Panel board
  grp = ents.add_group
  grp.name = "Panel board"
  face = grp.entities.add_face([-4.mm,-203.mm,0.mm], [0.mm,-203.mm,0.mm], [0.mm,203.mm,0.mm], [-4.mm,203.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(279.mm)
  mat = model.materials["Panel board"] || model.materials.add("Panel board")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 1.0
  grp.material = mat

  # Coated paper
  grp = ents.add_group
  grp.name = "Coated paper"
  face = grp.entities.add_face([-5.mm,-178.mm,12.5.mm], [-4.mm,-178.mm,12.5.mm], [-4.mm,178.mm,12.5.mm], [-5.mm,178.mm,12.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(254.mm)
  mat = model.materials["Coated paper"] || model.materials.add("Coated paper")
  mat.color = Sketchup::Color.new(250, 246, 232)
  mat.alpha = 1.0
  grp.material = mat

fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([457.mm, 228.5.mm, 63.5.mm]))
fp_inst.name = "Film-plane panel"
fp_inst.layer = model.layers["Film Panel"]
da = "dynamic_attributes"
[fp_defn, fp_inst].each do |e|
  e.set_attribute(da, "_name", "FilmPanel")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "fold", 0.0)
  e.set_attribute(da, "roty", 0.0)
end
fp_inst.set_attribute(da, "_fold_access", "VIEW")
fp_inst.set_attribute(da, "_fold_label", "Fold (0 exposure up / 1 coating down)")
fp_inst.set_attribute(da, "_roty_formula", "90*fold")
fp_inst.set_attribute(da, "onclick", 'ANIMATE("fold", 0, 1)')
fp_inst.set_attribute(da, "_onclick_access", "NONE")


# ═══ Prep-box top flaps — DYNAMIC COMPONENT (click: open the top to extract the print) ═══
pt_defn = model.definitions.add("Prep top flaps")
ents = pt_defn.entities
ptn_defn = model.definitions.add("Prep top flap (near)")
ents = ptn_defn.entities
  # Prep top flap (near)
  grp = ents.add_group
  grp.name = "Prep top flap (near)"
  face = grp.entities.add_face([0.mm,0.mm,-3.mm], [457.mm,0.mm,-3.mm], [457.mm,228.5.mm,-3.mm], [0.mm,228.5.mm,-3.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Panel board"] || model.materials.add("Panel board")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 1.0
  grp.material = mat

ptn_inst = pt_defn.entities.add_instance(ptn_defn, Geom::Transformation.new)
ptn_inst.name = "Prep top flap (near)"
ptf_defn = model.definitions.add("Prep top flap (far)")
ents = ptf_defn.entities
  # Prep top flap (far)
  grp = ents.add_group
  grp.name = "Prep top flap (far)"
  face = grp.entities.add_face([0.mm,-228.5.mm,-3.mm], [457.mm,-228.5.mm,-3.mm], [457.mm,0.mm,-3.mm], [0.mm,0.mm,-3.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Panel board"] || model.materials.add("Panel board")
  mat.color = Sketchup::Color.new(210, 180, 140)
  mat.alpha = 1.0
  grp.material = mat

ptf_inst = pt_defn.entities.add_instance(ptf_defn, Geom::Transformation.translation([0.mm, 457.mm, 0.mm]))
ptf_inst.name = "Prep top flap (far)"
pt_inst = entities.add_instance(pt_defn, Geom::Transformation.translation([457.mm, 0.mm, 406.mm]))
pt_inst.name = "Prep top flaps"
pt_inst.layer = model.layers["Prep Top Flaps"]
da = "dynamic_attributes"
[pt_defn, pt_inst].each do |e|
  e.set_attribute(da, "_name", "PrepTopFlaps")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "open", 0.0)
end
pt_inst.set_attribute(da, "_open_access", "VIEW")
pt_inst.set_attribute(da, "_open_label", "Open (0 closed / 1 open)")
pt_inst.set_attribute(da, "onclick", 'ANIMATE("open", 0, 1)')
pt_inst.set_attribute(da, "_onclick_access", "NONE")
[ptn_defn, ptn_inst].each do |e|
  e.set_attribute(da, "_name", "PrepTopFlapNear")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "rotx", 0.0)
end
ptn_inst.set_attribute(da, "_rotx_formula", "95*PrepTopFlaps!open")
[ptf_defn, ptf_inst].each do |e|
  e.set_attribute(da, "_name", "PrepTopFlapFar")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "rotx", 0.0)
end
ptf_inst.set_attribute(da, "_rotx_formula", "-95*PrepTopFlaps!open")


# ── Light cone (translucent teaching aid) ──

# ── Light cone (pinhole → paper) — translucent teaching aid, own tag ──
lc = entities.add_group
lc.name = "Light cone"
lc.layer = model.layers["Light Cone"]
lge = lc.entities
apx = Geom::Point3d.new(0.mm, 228.5.mm, 203.mm)
p0 = Geom::Point3d.new(452.mm, 50.5.mm, 76.mm); p1 = Geom::Point3d.new(452.mm, 406.5.mm, 76.mm); p2 = Geom::Point3d.new(452.mm, 406.5.mm, 330.mm); p3 = Geom::Point3d.new(452.mm, 50.5.mm, 330.mm)
lge.add_face(apx, p0, p1)
lge.add_face(apx, p1, p2)
lge.add_face(apx, p2, p3)
lge.add_face(apx, p3, p0)
lge.add_face(p0, p1, p2, p3)
lcm = model.materials["Light cone"] || model.materials.add("Light cone")
lcm.color = Sketchup::Color.new(74, 144, 217)
lcm.alpha = 0.18
lge.grep(Sketchup::Face).each { |f| f.material = lcm; f.back_material = lcm }


# ── Component callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Pinhole" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PINHOLE  Ø0.794mm  (f/576)", anc, Geom::Vector3d.new(-200.mm, -300.mm, 250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Shutter" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("SHUTTER
(click: lift to expose)", anc, Geom::Vector3d.new(-300.mm, -350.mm, 350.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Film-plane panel" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("FILM-PLANE PANEL
(click: fold down to coat / up to expose)", anc, Geom::Vector3d.new(120.mm, -450.mm, 450.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Prep top flaps" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PREP-BOX TOP FLAPS
(boxes built flaps-up; click: open
to remove the print in daylight)", anc, Geom::Vector3d.new(250.mm, -300.mm, 500.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Cardboard boxes (ghost)" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("TWO CARDBOARD BOXES
(joined with grey tape — ghosted)", anc, Geom::Vector3d.new(-120.mm, 520.mm, 560.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(1044.mm, 113.5.mm, 203.mm)
txt = entities.add_text("ARM SLEEVES (end wall)
(reach in to mix + coat in the dark)", anc, Geom::Vector3d.new(300.mm, -200.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(228.5.mm, 228.5.mm, 203.mm)
txt = entities.add_text("LIGHT CONE
(pinhole → paper)", anc, Geom::Vector3d.new(-150.mm, -420.mm, 300.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(457.mm, 228.5.mm, -4.mm)
txt = entities.add_text("GREY TAPE
(joins the two boxes)", anc, Geom::Vector3d.new(-100.mm, 400.mm, -250.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Boxes", "Pinhole", "Shutter", "Film Panel", "Prep Top Flaps", "Light Cone", "Labels"]; dl = model.layers[0]
model.layers.to_a.each { |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }

model.layers.each { |l| l.visible = true }
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(-0.4, -0.8, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["Assembled", ["Boxes", "Pinhole", "Shutter", "Film Panel", "Prep Top Flaps", "Light Cone"], nil, 0], ["No light cone", ["Boxes", "Pinhole", "Shutter", "Film Panel", "Prep Top Flaps"], nil, 0], ["Labeled", ["Boxes", "Pinhole", "Shutter", "Film Panel", "Prep Top Flaps", "Light Cone", "Labels"], nil, 0]].each { |name, tags, tgt, so|
  model.layers.each { |l| l.visible = (l == dl || tags.include?(l.name)) }
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.zoom_extents
  page = model.pages.add(name); page.use_camera = true
}
model.layers.each { |l| l.visible = true }
model.layers["Labels"].visible = false

model.commit_operation

# Register the DCs AFTER committing (redraw_with_undo opens its own operation).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  [sh_inst, fp_inst, pt_inst].each { |di| cls.redraw_with_undo(di) rescue nil } if cls
end

{ success: true, model: "mini-tbs", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   focal_mm: 457, f_number: 576 }.to_json
