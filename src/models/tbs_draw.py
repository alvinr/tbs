#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_draw.py — Neutral drawing + material primitives for the TBS-001 SketchUp models.

The generic Ruby-emitting helpers (mm, ruby_box/cylinder/prism/pipe/pipe_run/..., component,
material + mute/ghost machinery, vector math) shared by EVERY model generator. Extracted from
generate_sketchup_model.py (Phase 0 of the model-aggregation plan) so no model imports the
"overview" module just to draw — overview becomes a pure aggregator.

Holds the SHARED mutable build state (_MAT_BY_COLOR material registry, the muted()/_CTX_* ghost
context). Import this module (e.g. `import tbs_draw as draw`) so every reader sees the one live
state; do NOT `from tbs_draw import _CTX_FORCE` (that copies a stale binding).
"""
import math
import contextlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))

def mm(val):
    """Render a millimeter value as a Ruby literal carrying the `.mm` suffix.

    SketchUp's geometry database is always inches internally, but the Ruby API
    converts on input: `2362.mm` yields the correct inch value. Emitting `.mm`
    keeps the generated Ruby readable in the project's native millimeters and
    lets SketchUp do the conversion, rather than baking in pre-divided floats.
    """
    # Drop a trailing ".0" so whole numbers read as 2362.mm, not 2362.0.mm.
    if isinstance(val, float) and val.is_integer():
        val = int(val)
    return f"{val}.mm"
_CANON_RGB = {
    # tight greys / near-blacks (Δ≤6)
    (32, 32, 32): (26, 26, 26),
    (34, 34, 40): (26, 26, 26), (34, 34, 34): (26, 26, 26),
    (43, 43, 48): (42, 42, 42), (44, 44, 44): (42, 42, 42),
    (58, 58, 58): (51, 52, 58), (58, 58, 66): (51, 52, 58),
    (80, 80, 88): (80, 80, 90),
    (96, 96, 104): (88, 96, 112),
    (122, 128, 136): (128, 128, 138),
    (126, 126, 118): (119, 119, 119), (128, 128, 128): (119, 119, 119),
    (154, 160, 160): (154, 160, 166), (154, 160, 168): (154, 160, 166),
    (192, 192, 200): (184, 188, 196),
    (200, 176, 106): (200, 176, 112),
    (216, 207, 188): (216, 208, 188),
    # same-hue color pairs (Δ≤10) — blue / yellow, imperceptible
    (41, 128, 185): (41, 121, 184),
    (245, 197, 24): (241, 196, 15),
}
def hex_to_rgb(h):
    """Convert '#RRGGBB' to (r, g, b), collapsing near-identical colors to a canonical value so
    they share a material (holds the Sketchfab material count down)."""
    h = h.lstrip("#")
    rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return _CANON_RGB.get(rgb, rgb)
MUTE_NEUTRAL = (190, 190, 195)
GHOST_HEX = "#8C929B"   # single neutral blue-gray for ALL forced-ghost context (construction prior phases)
def mute_hex(h, f, neutral=MUTE_NEUTRAL):
    """Blend a '#RRGGBB' color a fraction `f` toward `neutral` (0 = unchanged, 1 = full
    neutral).  Used to desaturate ghosted context (e.g. IBC tanks) so strong circuit
    colors don't bury the key components — matches the muted feel of overview.skp.
    Under a forced-muted (ghost) context, ALL colors collapse to the single GHOST_HEX so the
    faded prior-phase context reads as one uniform gray (easiest to read against the current
    phase's full-color additions) and shares ONE material (Sketchfab caps materials at ~100)."""
    if _CTX_FORCE:
        return GHOST_HEX
    if not f:
        return h
    r, g, b = hex_to_rgb(h)
    nr, ng, nb = neutral
    blend = lambda c, n: round(c * (1 - f) + n * f)
    return "#%02X%02X%02X" % (blend(r, nr), blend(g, ng), blend(b, nb))
_MAT_BY_COLOR = {}
def shared_mat_name(name, color, alpha):
    """Return a material name shared by every element of the same CANONICAL color + alpha.
    Under a forced-muted (ghost) context the name is namespaced ('ghost ' prefix) and keyed
    separately, so a ghosted static copy never collides on the same material as its full-color
    live twin (same group name, different color/alpha). Outside a forced context this is
    byte-identical to before (the key gains a constant False prefix; the returned name is unchanged)."""
    key = (_CTX_FORCE, hex_to_rgb(color), alpha if alpha is not None else 1.0)
    return _MAT_BY_COLOR.setdefault(key, ("ghost " + name) if _CTX_FORCE else name)
_CTX_MUTE, _CTX_ALPHA, _CTX_FORCE = 0.0, None, False
@contextlib.contextmanager
def muted(mute, alpha, force=False):
    """Within this block, drawing helpers build muted CONTEXT/backdrop geometry at source.
    force=True makes the context's mute/alpha WIN over whatever the caller passes — so builders
    that hardcode their own alpha/mute (e.g. ibc_stack(alpha=0.85)) are still fully ghosted."""
    global _CTX_MUTE, _CTX_ALPHA, _CTX_FORCE
    prev = (_CTX_MUTE, _CTX_ALPHA, _CTX_FORCE)
    _CTX_MUTE, _CTX_ALPHA, _CTX_FORCE = mute, alpha, force
    try:
        yield
    finally:
        _CTX_MUTE, _CTX_ALPHA, _CTX_FORCE = prev
def _mute_ctx(mute, alpha):
    """Resolve a helper's mute/alpha against the current muted() context (idempotent).
    Under force, the context values override the caller's; otherwise the caller's explicit
    (non-None) values win, so outside a muted() block this is byte-identical to passing them through."""
    if _CTX_FORCE:
        return (_CTX_MUTE, _CTX_ALPHA if _CTX_ALPHA is not None else alpha)
    return (_CTX_MUTE if mute is None else mute, _CTX_ALPHA if alpha is None else alpha)
def ruby_box(name, x, y, z, w, d, h, color=None, alpha=None, both_sides=False, mute=None,
             holes=None, hole_axis=None):
    """Generate Ruby to create a named box group inside the `ents` context.

    Parameters are in mm. x, y, z: origin corner (min X, min Yd, min Z).
    w, d, h: width (X), depth (Yd), height (Z). Boxes are added to `ents`,
    the entities collection of the enclosing component definition.
    `both_sides` paints the back faces too (so interior + exterior read the
    same — used for the container shell).

    `holes` cuts real drilled clearance holes THROUGH the panel (a void, not a
    part — so a pipe/cable reads as passing through a hole, not fused into the
    slab; see check_interference.py --pipes).  Each hole is `(a, b, r)` in mm
    world coords of the two in-plane axes, radius r, cut along `hole_axis`
    ("x"/"y"/"z" — the panel's thin axis): x→(yd,z), y→(x,z), z→(x,yd).  The
    cutter is oversized ±2mm so it cleanly penetrates both faces via
    Group#subtract; material is applied to the resulting solid.
    """
    mute, alpha = _mute_ctx(mute, alpha)
    # Sum in millimeters first, then render each corner with the `.mm` suffix.
    x0, y0, z0 = mm(x), mm(y), mm(z)
    x1, y1 = mm(x + w), mm(y + d)
    h_mm = mm(h)

    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face('
        f'[{x0},{y0},{z0}], [{x1},{y0},{z0}], '
        f'[{x1},{y1},{z0}], [{x0},{y1},{z0}])',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({h_mm})',
    ]

    if holes:
        # Cut real drilled clearance holes by drawing each circle COPLANAR on the panel's NEAR face and
        # pushpulling it through the thickness.  (Group#subtract does NOT chain in this SketchUp — the 2nd
        # boolean silently collapses the solid to garbage; coplanar-face pushpull is robust and adds one
        # clean 24-segment hole each, staying manifold.)  Keep each hole a safe MARGIN inside the panel
        # on both in-plane axes so a near-edge razor sliver can't form.
        span = {"x": (x, x + w, w), "y": (y, y + d, d), "z": (z, z + h, h)}[hole_axis]
        inplane = {"x": ((y, y + d), (z, z + h)),
                   "y": ((x, x + w), (z, z + h)),
                   "z": ((x, x + w), (y, y + d))}[hole_axis]
        normal = {"x": "[1,0,0]", "y": "[0,1,0]", "z": "[0,0,1]"}[hole_axis]
        near, thick = span[0], span[2]
        MARGIN = 5.0

        def _clamp(v, lo, hi, r):
            return min(max(v, lo + r + MARGIN), hi - r - MARGIN)
        for a, b, r in holes:
            a = _clamp(a, inplane[0][0], inplane[0][1], r)
            b = _clamp(b, inplane[1][0], inplane[1][1], r)
            if hole_axis == "x":
                cc = f'[{mm(near)},{mm(a)},{mm(b)}]'
            elif hole_axis == "y":
                cc = f'[{mm(a)},{mm(near)},{mm(b)}]'
            else:
                cc = f'[{mm(a)},{mm(b)},{mm(near)}]'
            lines += [
                f'  hcirc = grp.entities.add_circle({cc}, {normal}, {mm(r)}, 24)',
                f'  hdisk = hcirc.map {{ |e| e.faces }}.flatten.uniq.min_by {{ |ff| ff.area }}',
                f'  hdisk.reverse! if hdisk.normal.{hole_axis} < 0',   # normal into the solid
                f'  hdisk.pushpull({mm(thick)})',                       # through to the far face → hole
            ]

    if color:
        color = mute_hex(color, mute)
        r, g, b = hex_to_rgb(color)
        # Reuse the material if it already exists so re-sends don't pile up
        # "Container Ceiling2", "Container Ceiling3", … duplicates.
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        # Always set alpha (default opaque) so a reused material can't keep a
        # stale translucency from an earlier run.
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
        if both_sides:
            lines.append(f'  grp.entities.grep(Sketchup::Face).each '
                         f'{{ |f| f.material = mat; f.back_material = mat }}')

    lines.append('')
    return '\n'.join(lines)
def ruby_prism(name, pts, z, h, color=None, alpha=None, mute=None, holes=None):
    """A vertical prism from an arbitrary polygon (list of (x, y) mm points) at height z,
    pushpulled up by h. Same material handling as ruby_box. Used for NOTCHED grates so the deck
    is ONE continuous piece (a bite cut out of one edge), not separate sections needing support.

    `holes` cuts real drilled clearance cutouts THROUGH the slab (along its Z thickness) so a pipe
    reads as passing through a hole/slot, not fused into the deck (see check_interference.py --pipes).
    Each entry is either a ROUND hole `(cx, cy, r)` or a rectangular SLOT `(x0, y0, x1, y1)`, in mm
    XY world coords; each must sit strictly INSIDE the polygon (coplanar-face pushpull, same robust
    drill as ruby_box — Group#subtract chaining is unreliable in this SketchUp)."""
    mute, alpha = _mute_ctx(mute, alpha)
    z0, h_mm = mm(z), mm(h)
    face_pts = ", ".join(f"[{mm(px)},{mm(py)},{z0}]" for px, py in pts)
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face({face_pts})',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({h_mm})',
    ]
    for hole in (holes or []):
        if len(hole) == 3:                                   # round hole (cx, cy, r)
            cx, cy, r = hole
            lines.append(f'  hc = grp.entities.add_circle([{mm(cx)},{mm(cy)},{z0}], [0,0,1], {mm(r)}, 24)')
            lines.append('  hf = hc.map { |e| e.faces }.flatten.uniq.min_by { |ff| ff.area }')
        else:                                                # rectangular slot (x0, y0, x1, y1)
            x0, y0, x1, y1 = hole
            lines.append(f'  hf = grp.entities.add_face('
                         f'[{mm(x0)},{mm(y0)},{z0}], [{mm(x1)},{mm(y0)},{z0}], '
                         f'[{mm(x1)},{mm(y1)},{z0}], [{mm(x0)},{mm(y1)},{z0}])')
        lines.append('  if hf; hf.reverse! if hf.normal.z < 0; hf.pushpull(%s); end' % h_mm)   # through to the far face → cutout
    if color:
        color = mute_hex(color, mute)
        r, g, b = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)
def component(defn_name, tag, body):
    """Wrap a body of ruby_box calls into a ComponentDefinition + instance.

    The body builds geometry into `ents`; we then place one instance and put
    it on `tag`.
    """
    return f'''  # ═══ {defn_name} ═══
  defn = model.definitions.add("{defn_name}")
  ents = defn.entities
{body}
  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "{defn_name}"
  inst.layer = model.layers["{tag}"]
'''
def ruby_cone_wire(name, apex, base, tag):
    """Generate Ruby for a wireframe pyramid (edges only) in `ents`.

    apex: (x, y, z). base: 4 (x, y, z) corners. The edges are assigned to
    `tag`, whose line style is set to dashed in the main script — so the cone
    reads as dashed guidance geometry rather than a solid system.
    """
    a = f'[{mm(apex[0])},{mm(apex[1])},{mm(apex[2])}]'
    b = [f'[{mm(p[0])},{mm(p[1])},{mm(p[2])}]' for p in base]
    return '\n'.join([
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  apex = {a}',
        f'  b0 = {b[0]}; b1 = {b[1]}; b2 = {b[2]}; b3 = {b[3]}',
        f'  edges = []',
        f'  edges.concat(ge.add_edges(b0, b1, b2, b3, b0))',
        f'  edges << ge.add_line(apex, b0)',
        f'  edges << ge.add_line(apex, b1)',
        f'  edges << ge.add_line(apex, b2)',
        f'  edges << ge.add_line(apex, b3)',
        f'  lyr = model.layers["{tag}"]',
        f'  edges.each {{ |e| e.layer = lyr if e.is_a?(Sketchup::Edge) }}',
        '',
    ])
def ruby_cylinder(name, cx, cy, cz, radius, height, color=None, alpha=None,
                  n=24, axis="z", mute=None):
    """Generate Ruby for a cylinder in `ents`, axis along +x/+y/+z.

    (cx, cy, cz): center of the base circle. radius/height in mm. Used for
    round bodies (filters, drum, ducts, pipe stubs, fans).
    """
    mute, alpha = _mute_ctx(mute, alpha)
    normal = {"z": "[0,0,1]", "y": "[0,1,0]", "x": "[1,0,0]"}[axis]
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  circle = ge.add_circle([{mm(cx)},{mm(cy)},{mm(cz)}], '
        f'{normal}, {mm(radius)}, {n})',
        f'  cface = ge.add_face(circle)',
        f'  cface.reverse! if cface.normal.{axis} < 0',
        f'  cface.pushpull({mm(height)})',
    ]
    if color:
        color = mute_hex(color, mute)
        r, g, b = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r}, {g}, {b})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)
def ruby_bolt(name, x, y, z, length, radius=6.0, axis="z", color=None, head="base", nut="far", mute=None):
    """A fastener: an Ø(2·radius) shank from (x,y,z) along +`axis` by `length`, PLUS a hex HEAD and/or hex
    NUT drawn as 6-sided prisms so it reads as a real bolt, not a plain rod.  `head`/`nut` name the end each
    sits on: "base" = the (x,y,z) end, "far" = the (base+length) end, or None (omit — e.g. a nut-less anchor
    or self-drilling screw).  Hex circumradius ≈ 1.65·radius, thickness ≈ 1.35·radius (real hex proportions).
    The head/nut protrude just proud of the shank ends (against the clamped faces)."""
    hex_r, hex_h = radius * 1.65, radius * 1.35
    ai = {"x": 0, "y": 1, "z": 2}[axis]
    out = [ruby_cylinder(name, x, y, z, radius, length, color=color, axis=axis, mute=mute)]
    for kind, end in (("head", head), ("nut", nut)):
        if not end:
            continue
        b = [x, y, z]
        b[ai] += length if end == "far" else -hex_h            # protrude outward past that shank end
        out.append(ruby_cylinder(f"{name} {kind}", b[0], b[1], b[2], hex_r, hex_h,
                                 color=color, axis=axis, n=6, mute=mute))
    return "\n".join(out)
def ruby_tri(name, p1, p2, p3, thick, color=None, alpha=None, mute=None):
    """Triangular plate: a face through p1,p2,p3 pushpulled by `thick` along its
    normal (used for gusset plates)."""
    mute, alpha = _mute_ctx(mute, alpha)
    face = ', '.join(f'[{mm(p[0])},{mm(p[1])},{mm(p[2])}]' for p in (p1, p2, p3))
    out = [
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        '  ge = grp.entities',
        f'  f = ge.add_face({face})',
        f'  f.pushpull({mm(thick)})',
    ]
    if color:
        color = mute_hex(color, mute)
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        out.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        out.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        out.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        out.append('  grp.material = mat')
    out.append('')
    return '\n'.join(out)
def ruby_arc_wall(name, cx, cy, r, wall_t, height, gap_center_deg, gap_deg,
                  color=None, alpha=None, n=48, z0=0, mute=0.0):
    """Hollow curved wall (annular sector, extruded in +Z) with a gap.

    The gap (an opening of `gap_deg` centerd on `gap_center_deg`) reads as a
    doorway/entry slot in the cylinder. Built as a closed band polygon (outer
    arc forward + inner arc back) at base height `z0` then pushpulled `height`.
    """
    ri = r - wall_t
    a0 = math.radians(gap_center_deg + gap_deg / 2.0)
    a1 = math.radians(gap_center_deg + 360.0 - gap_deg / 2.0)
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(n, -1, -1):
        a = a0 + (a1 - a0) * i / n
        pts.append((cx + ri * math.cos(a), cy + ri * math.sin(a)))
    pts_ruby = ', '.join(f'[{mm(round(x, 2))},{mm(round(y, 2))},{mm(z0)}]' for x, y in pts)

    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  face = ge.add_face([{pts_ruby}])',
        f'  face.reverse! if face.normal.z < 0',
        f'  face.pushpull({mm(height)})',
    ]
    if color:
        color = mute_hex(color, mute)
        r_, g_, b_ = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({r_}, {g_}, {b_})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)
def tilted_slab(name, x, y_near, z_base, w, length, t, tilt_deg, color, alpha=None, mute=0.0):
    """Flat slab tilted up from its near-bottom edge, rising in +Z and -Y (faces
    away from the container, toward the sun). length runs up the tilt."""
    th = math.radians(tilt_deg)
    dy, dz = -length * math.cos(th), length * math.sin(th)
    corners = [(x, y_near, z_base), (x + w, y_near, z_base),
               (x + w, y_near + dy, z_base + dz), (x, y_near + dy, z_base + dz)]
    pts = ', '.join(f'[{mm(px)},{mm(py)},{mm(pz)}]' for px, py, pz in corners)
    color = mute_hex(color, mute)
    r, g, b = hex_to_rgb(color)
    mat_nm = shared_mat_name(name, color, alpha)
    return '\n'.join([
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  face = grp.entities.add_face({pts})',
        f'  face.pushpull({mm(t)})',
        f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")',
        f'  mat.color = Sketchup::Color.new({r}, {g}, {b})',
        f'  mat.alpha = {alpha if alpha is not None else 1.0}',
        '  grp.material = mat', ''])
def ruby_pipe(name, p1, p2, r, color=None, alpha=None, n=16, mute=0.0):
    """Straight cylindrical pipe between two arbitrary points p1, p2 (mm)."""
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    lines = [
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  vec = Geom::Vector3d.new({mm(x2 - x1)}, {mm(y2 - y1)}, {mm(z2 - z1)})',
        f'  circle = ge.add_circle([{mm(x1)},{mm(y1)},{mm(z1)}], vec, {mm(r)}, {n})',
        f'  pf = ge.add_face(circle)',
        f'  pf.reverse! if pf.normal.dot(vec) < 0',
        f'  pf.pushpull(vec.length)',
    ]
    if color:
        color = mute_hex(color, mute)
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        lines.append(f'  mat = model.materials["{mat_nm}"] || '
                     f'model.materials.add("{mat_nm}")')
        lines.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        lines.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        lines.append(f'  grp.material = mat')
    lines.append('')
    return '\n'.join(lines)
def ruby_flex_duct(name, p1, p2, r, color=None, alpha=None, ribs=None, mute=0.0):
    """Corrugated flex duct between p1 and p2 — a run of short pipe segments with
    alternating crest/valley radii so it reads as a ribbed flexible duct."""
    L = math.sqrt(sum((p2[i] - p1[i]) ** 2 for i in range(3)))
    if ribs is None:
        ribs = max(8, int(L / (r * 0.7)))            # rib pitch ≈ 0.7·r
    out = []
    for i in range(ribs):
        t0, t1 = i / ribs, (i + 1) / ribs
        a = tuple(p1[k] + (p2[k] - p1[k]) * t0 for k in range(3))
        b = tuple(p1[k] + (p2[k] - p1[k]) * t1 for k in range(3))
        rr = r if i % 2 == 0 else r * 0.8            # crest / valley
        out.append(ruby_pipe(name, a, b, rr, color=color, alpha=alpha, n=14, mute=mute))
    return '\n'.join(out)
def ruby_coil_cord(name, waypoints, r=5.0, color=None, alpha=None,
                   coil_r=None, pitch=None, pts_per_turn=8, mute=0.0):
    """A 'soft' flexible cord — the visual opposite of the rigid `ruby_pipe_run`:
    a thin conductor that runs as a HELICAL COIL ('curly cord') along each straight
    leg, with short straight stubs at the ends / at each waypoint for termination.
    Color still encodes the circuit; the coiled geometry marks it as a flexible
    connector (the soft-connector analogue of the beaded pull-cord + corrugated
    flex-duct helpers). Tune `coil_r` (curl radius), `pitch` (axial advance per turn),
    and `r` (conductor radius — keep it thinner than the rigid conduit it replaces)."""
    coil_r = coil_r if coil_r is not None else 5.6 * r      # curl radius (~28 @ r=5, tightened 20%)
    pitch = pitch if pitch is not None else 18.0 * r        # axial advance/turn (~90 @ r=5)
    V = [tuple(float(c) for c in p) for p in waypoints]
    out = []
    for i in range(1, len(V)):
        a, b = V[i - 1], V[i]
        axis = _vsub(b, a)
        L = _vlen(axis)
        if L < 1e-3:
            continue
        d = _vscale(axis, 1.0 / L)
        stub = min(max(0.10 * L, 3.0 * r), 0.30 * L)        # straight termination ends
        coil_L = L - 2.0 * stub
        p0 = _vadd(a, _vscale(d, stub))                     # coil start (on axis)
        out.append(ruby_pipe(name, a, p0, r, color=color, alpha=alpha, n=10, mute=mute))
        if coil_L > pitch * 0.5:
            ref = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
            u = _vunit(_vcross(d, ref))                      # perpendicular frame
            w = _vcross(d, u)
            turns = coil_L / pitch
            npts = max(8, int(round(turns * pts_per_turn)))
            prev = p0
            for k in range(1, npts + 1):
                t = k / npts
                ang = 2.0 * math.pi * turns * t
                axial = _vadd(p0, _vscale(d, coil_L * t))
                pt = _vadd(axial, _vadd(_vscale(u, coil_r * math.cos(ang)),
                                        _vscale(w, coil_r * math.sin(ang))))
                out.append(ruby_pipe(name, prev, pt, r, color=color, alpha=alpha, n=6, mute=mute))
                prev = pt
            p1 = _vadd(p0, _vscale(d, coil_L))              # coil end (back on axis)
            out.append(ruby_pipe(name, prev, p1, r, color=color, alpha=alpha, n=8, mute=mute))
            out.append(ruby_pipe(name, p1, b, r, color=color, alpha=alpha, n=10, mute=mute))
        else:
            out.append(ruby_pipe(name, p0, b, r, color=color, alpha=alpha, n=10, mute=mute))
    return '\n'.join(out)
def _vsub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def _vadd(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def _vscale(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def _vdot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def _vcross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def _vlen(a): return math.sqrt(_vdot(a, a))
def _vunit(a):
    L = _vlen(a)
    return (a[0]/L, a[1]/L, a[2]/L) if L > 1e-9 else (0.0, 0.0, 0.0)
def ruby_elbow(name, A, O, Rc, normal, d_in, theta, r,
               color=None, alpha=None, n=16, seg=8, mute=0.0):
    """Swept-torus elbow fitting: a pipe cross-section circle (radius r) at A is
    swept along an arc (centerline radius Rc, center O, plane normal `normal`,
    sweep `theta` rad) — a real 90deg/45deg elbow body, not a butt corner."""
    xa = _vunit(_vsub(A, O))
    out = [
        f'  # {name}',
        '  grp = ents.add_group',
        f'  grp.name = "{name}"',
        '  ge = grp.entities',
        (f'  arc = ge.add_arc([{mm(O[0])},{mm(O[1])},{mm(O[2])}], '
         f'[{xa[0]:.6f},{xa[1]:.6f},{xa[2]:.6f}], '
         f'[{normal[0]:.6f},{normal[1]:.6f},{normal[2]:.6f}], '
         f'{mm(Rc)}, 0.0, {theta:.6f}, {seg})'),
        (f'  circle = ge.add_circle([{mm(A[0])},{mm(A[1])},{mm(A[2])}], '
         f'[{d_in[0]:.6f},{d_in[1]:.6f},{d_in[2]:.6f}], {mm(r)}, {n})'),
        '  f = ge.add_face(circle)',
        '  f.followme(arc)',
        # followme leaves the arc CENTERLINE behind as loose edges (no face) — they render as stray
        # dashed/"perspective" lines all over the model. Drop them (they're inside the swept tube).
        '  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }',
    ]
    if color:
        color = mute_hex(color, mute)
        rr, gg, bb = hex_to_rgb(color)
        mat_nm = shared_mat_name(name, color, alpha)
        out.append(f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")')
        out.append(f'  mat.color = Sketchup::Color.new({rr}, {gg}, {bb})')
        out.append(f'  mat.alpha = {alpha if alpha is not None else 1.0}')
        out.append('  grp.material = mat')
    out.append('')
    return '\n'.join(out)
def ruby_pipe_run(name, waypoints, r, color=None, alpha=None,
                  elbow_r=None, n=16, seg=8, mute=0.0):
    """Pipe run through axis-aligned `waypoints`: straight segments joined by a
    swept-torus elbow fitting at every interior vertex (short-radius elbow,
    centerline radius = 1x pipe diameter per skill_plumbing_drawing). Direction
    changes happen only at fittings — no diagonals, no butt corners."""
    R = elbow_r if elbow_r is not None else 2.0 * r
    V = [tuple(float(c) for c in p) for p in waypoints]
    out = []
    start = V[0]
    for i in range(1, len(V)):
        if i == len(V) - 1:
            if _vlen(_vsub(V[i], start)) > 0.5:
                out.append(ruby_pipe(name, start, V[i], r, color, alpha, n, mute=mute))
            break
        d_in = _vunit(_vsub(V[i], V[i-1]))
        d_out = _vunit(_vsub(V[i+1], V[i]))
        theta = math.acos(max(-1.0, min(1.0, _vdot(d_in, d_out))))
        if theta < 1e-3:                 # collinear — keep running straight
            continue
        T = R * math.tan(theta / 2.0)
        T = min(T, _vlen(_vsub(V[i], start)) * 0.49,
                _vlen(_vsub(V[i+1], V[i])) * 0.49)
        Rc = T / math.tan(theta / 2.0)
        A = _vadd(V[i], _vscale(d_in, -T))
        B = _vadd(V[i], _vscale(d_out, T))
        n_in = _vunit(_vsub(d_out, _vscale(d_in, _vdot(d_out, d_in))))
        O = _vadd(A, _vscale(n_in, Rc))
        normal = _vunit(_vcross(d_in, d_out))
        if _vlen(_vsub(A, start)) > 0.5:
            out.append(ruby_pipe(name, start, A, r, color, alpha, n, mute=mute))
        out.append(ruby_elbow(name + " elbow", A, O, Rc, normal, d_in, theta,
                              r, color, alpha, n, seg, mute=mute))
        start = B
    return '\n'.join(out)
def ruby_flex_run(name, waypoints, r, color=None, alpha=None,
                  elbow_r=None, n=16, seg=8, mute=0.0):
    """Like ruby_pipe_run but the straight legs are corrugated flex duct
    (ruby_flex_duct); bends use the same swept-torus elbow fitting so the run
    stays orthogonal (per skill_plumbing_drawing) — right-angle connections."""
    R = elbow_r if elbow_r is not None else 2.0 * r
    V = [tuple(float(c) for c in p) for p in waypoints]
    out = []
    start = V[0]
    for i in range(1, len(V)):
        if i == len(V) - 1:
            if _vlen(_vsub(V[i], start)) > 0.5:
                out.append(ruby_flex_duct(name, start, V[i], r, color, alpha, mute=mute))
            break
        d_in = _vunit(_vsub(V[i], V[i-1]))
        d_out = _vunit(_vsub(V[i+1], V[i]))
        theta = math.acos(max(-1.0, min(1.0, _vdot(d_in, d_out))))
        if theta < 1e-3:
            continue
        T = R * math.tan(theta / 2.0)
        T = min(T, _vlen(_vsub(V[i], start)) * 0.49,
                _vlen(_vsub(V[i+1], V[i])) * 0.49)
        Rc = T / math.tan(theta / 2.0)
        A = _vadd(V[i], _vscale(d_in, -T))
        B = _vadd(V[i], _vscale(d_out, T))
        n_in = _vunit(_vsub(d_out, _vscale(d_in, _vdot(d_out, d_in))))
        O = _vadd(A, _vscale(n_in, Rc))
        normal = _vunit(_vcross(d_in, d_out))
        if _vlen(_vsub(A, start)) > 0.5:
            out.append(ruby_flex_duct(name, start, A, r, color, alpha, mute=mute))
        out.append(ruby_elbow(name + " elbow", A, O, Rc, normal, d_in, theta,
                              r, color, alpha, n, seg, mute=mute))
        start = B
    return '\n'.join(out)
def ruby_tee(name, node, run_dir, branch_dir, r, color=None, alpha=None, n=16, mute=0.0):
    """Tee fitting body at a branch point: a fat run-through stub (along
    run_dir) plus a fat branch stub (along branch_dir), OD slightly larger than
    the pipe — a real tee, not a butt junction. The three pipe runs plug into
    its ports."""
    rt = r * 1.35
    L = r * 1.9
    ru = _vunit(run_dir)
    bu = _vunit(branch_dir)
    a = _vadd(node, _vscale(ru, -L))
    b = _vadd(node, _vscale(ru, L))
    c = _vadd(node, _vscale(bu, L))
    return '\n'.join([ruby_pipe(name, a, b, rt, color, alpha, n, mute=mute),
                      ruby_pipe(name, node, c, rt, color, alpha, n, mute=mute)])
