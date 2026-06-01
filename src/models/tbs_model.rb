model = Sketchup.active_model
model.start_operation("TBS-001 Phase 1", true)
entities = model.active_entities

  # Container Floor
  grp = entities.add_group
  grp.name = "Container Floor"
  face = grp.entities.add_face([0.0,0.0,-1.5748031496062993], [232.00787401574806,0.0,-1.5748031496062993], [232.00787401574806,92.99212598425197,-1.5748031496062993], [0.0,92.99212598425197,-1.5748031496062993])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.5748031496062993)
  mat = model.materials.add("Container Floor")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Container Ceiling
  grp = entities.add_group
  grp.name = "Container Ceiling"
  face = grp.entities.add_face([0.0,0.0,94.01574803149607], [232.00787401574806,0.0,94.01574803149607], [232.00787401574806,92.99212598425197,94.01574803149607], [0.0,92.99212598425197,94.01574803149607])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.5748031496062993)
  mat = model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Pinhole Wall (Yd=0)
  grp = entities.add_group
  grp.name = "Pinhole Wall (Yd=0)"
  face = grp.entities.add_face([0.0,-1.5748031496062993,0.0], [232.00787401574806,-1.5748031496062993,0.0], [232.00787401574806,0.0,0.0], [0.0,0.0,0.0])
  face.reverse! if face.normal.z < 0
  face.pushpull(94.01574803149607)
  mat = model.materials.add("Pinhole Wall (Yd=0)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Film Plane Wall (Yd=max)
  grp = entities.add_group
  grp.name = "Film Plane Wall (Yd=max)"
  face = grp.entities.add_face([0.0,92.99212598425197,0.0], [232.00787401574806,92.99212598425197,0.0], [232.00787401574806,94.56692913385827,0.0], [0.0,94.56692913385827,0.0])
  face.reverse! if face.normal.z < 0
  face.pushpull(94.01574803149607)
  mat = model.materials.add("Film Plane Wall (Yd=max)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Far End Wall (IBC end)
  grp = entities.add_group
  grp.name = "Far End Wall (IBC end)"
  face = grp.entities.add_face([232.00787401574806,0.0,0.0], [233.58267716535437,0.0,0.0], [233.58267716535437,92.99212598425197,0.0], [232.00787401574806,92.99212598425197,0.0])
  face.reverse! if face.normal.z < 0
  face.pushpull(94.01574803149607)
  mat = model.materials.add("Far End Wall (IBC end)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Processing Tray Floor
  grp = entities.add_group
  grp.name = "Processing Tray Floor"
  face = grp.entities.add_face([6.692913385826772,3.1496062992125986,0.0], [182.244094488189,3.1496062992125986,0.0], [182.244094488189,89.76377952755905,0.0], [6.692913385826772,89.76377952755905,0.0])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.07874015748031496)
  mat = model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(232, 245, 233)
  mat.alpha = 0.5
  grp.material = mat

  # Tray Rim Near
  grp = entities.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([6.692913385826772,3.1496062992125986,0.07874015748031496], [182.244094488189,3.1496062992125986,0.07874015748031496], [182.244094488189,3.2283464566929134,0.07874015748031496], [6.692913385826772,3.2283464566929134,0.07874015748031496])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.8897637795275593)
  mat = model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Far
  grp = entities.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([6.692913385826772,89.68503937007874,0.07874015748031496], [182.244094488189,89.68503937007874,0.07874015748031496], [182.244094488189,89.76377952755905,0.07874015748031496], [6.692913385826772,89.76377952755905,0.07874015748031496])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.8897637795275593)
  mat = model.materials.add("Tray Rim Far")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Left
  grp = entities.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([6.692913385826772,3.1496062992125986,0.07874015748031496], [6.771653543307087,3.1496062992125986,0.07874015748031496], [6.771653543307087,89.76377952755905,0.07874015748031496], [6.692913385826772,89.76377952755905,0.07874015748031496])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.8897637795275593)
  mat = model.materials.add("Tray Rim Left")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Right
  grp = entities.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([182.16535433070868,3.1496062992125986,0.07874015748031496], [182.244094488189,3.1496062992125986,0.07874015748031496], [182.244094488189,89.76377952755905,0.07874015748031496], [182.16535433070868,89.76377952755905,0.07874015748031496])
  face.reverse! if face.normal.z < 0
  face.pushpull(1.8897637795275593)
  mat = model.materials.add("Tray Rim Right")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Walkway Near (left section)
  grp = entities.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([18.50393700787402,0.0,2.952755905511811], [45.472440944881896,0.0,2.952755905511811], [45.472440944881896,11.811023622047244,2.952755905511811], [18.50393700787402,11.811023622047244,2.952755905511811])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.984251968503937)
  mat = model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Near (widened)
  grp = entities.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([45.47244094488189,0.0,2.952755905511811], [103.50393700787401,0.0,2.952755905511811], [103.50393700787401,19.68503937007874,2.952755905511811], [45.47244094488189,19.68503937007874,2.952755905511811])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.984251968503937)
  mat = model.materials.add("Walkway Near (widened)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Near (right section)
  grp = entities.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([103.50393700787401,0.0,2.952755905511811], [170.43307086614175,0.0,2.952755905511811], [170.43307086614175,11.811023622047244,2.952755905511811], [103.50393700787401,11.811023622047244,2.952755905511811])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.984251968503937)
  mat = model.materials.add("Walkway Near (right section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Far
  grp = entities.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([18.50393700787402,81.18110236220473,2.952755905511811], [170.43307086614175,81.18110236220473,2.952755905511811], [170.43307086614175,92.99212598425197,2.952755905511811], [18.50393700787402,92.99212598425197,2.952755905511811])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.984251968503937)
  mat = model.materials.add("Walkway Far")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Right (IBC end)
  grp = entities.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([170.43307086614175,0.0,2.952755905511811], [182.24409448818898,0.0,2.952755905511811], [182.24409448818898,92.99212598425197,2.952755905511811], [170.43307086614175,92.99212598425197,2.952755905511811])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.984251968503937)
  mat = model.materials.add("Walkway Right (IBC end)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Left (cargo door)
  grp = entities.add_group
  grp.name = "Walkway Left (cargo door)"
  face = grp.entities.add_face([6.692913385826772,0.0,2.952755905511811], [18.503937007874015,0.0,2.952755905511811], [18.503937007874015,92.99212598425197,2.952755905511811], [6.692913385826772,92.99212598425197,2.952755905511811])
  face.reverse! if face.normal.z < 0
  face.pushpull(0.984251968503937)
  mat = model.materials.add("Walkway Left (cargo door)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat


model.commit_operation
Sketchup.active_model.active_view.zoom_extents
{ success: true, phase: "Phase 1 — Container + Walkways + Tray" }.to_json
