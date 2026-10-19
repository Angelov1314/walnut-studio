import bpy, math, random
from mathutils import Vector
from math import sin, cos, pi

def mat(name, color, rough=0.5, metal=0, noise=0, scale=100):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    p = n.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if noise:
        tex = n.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value = scale
        tex.inputs['Detail'].default_value = 2
        bump = n.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = noise
        bump.inputs['Distance'].default_value = 0.025
        l.new(tex.outputs['Fac'], bump.inputs['Height'])
        l.new(bump.outputs['Normal'], p.inputs['Normal'])
    return m

def wood(name, base):
    m = mat(name, base, 0.39)
    n = m.node_tree.nodes
    l = m.node_tree.links
    p = n.get('Principled BSDF')
    tc = n.new('ShaderNodeTexCoord')
    mp = n.new('ShaderNodeVectorMath')
    mp.operation = 'MULTIPLY'
    mp.inputs[1].default_value = (5, 0.28, 7)
    l.new(tc.outputs['Generated'], mp.inputs[0])
    no = n.new('ShaderNodeTexNoise')
    no.inputs['Scale'].default_value = 5
    no.inputs['Detail'].default_value = 3
    no.inputs['Roughness'].default_value = 0.7
    l.new(mp.outputs['Vector'], no.inputs['Vector'])
    ra = n.new('ShaderNodeValToRGB')
    ra.color_ramp.elements[0].position = 0.18
    ra.color_ramp.elements[0].color = (*(v * 0.64 for v in base), 1)
    ra.color_ramp.elements[1].position = 0.83
    ra.color_ramp.elements[1].color = (*(min(v * 1.25, 1) for v in base), 1)
    l.new(no.outputs['Fac'], ra.inputs[0])
    l.new(ra.outputs[0], p.inputs['Base Color'])
    bu = n.new('ShaderNodeBump')
    bu.inputs['Strength'].default_value = 0.16
    bu.inputs['Distance'].default_value = 0.009
    l.new(no.outputs['Fac'], bu.inputs['Height'])
    l.new(bu.outputs[0], p.inputs['Normal'])
    return m

def cube(name, loc, dim, ma, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dim
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if ma:
        o.data.materials.append(ma)
    if bevel:
        mod = o.modifiers.new('Soft manufactured edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        mod = o.modifiers.new('Weighted corner normals', 'WEIGHTED_NORMAL')
    return o

def uv(name, loc, scale, ma, seg=32, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(ma)
    for p in o.data.polygons:
        p.use_smooth = True
    return o

def cyl(name, loc, r, depth, ma, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(ma)
    b = o.modifiers.new('Edge softness', 'BEVEL')
    b.width = 0.009
    b.segments = 3
    o.modifiers.new('Normals', 'WEIGHTED_NORMAL')
    return o

def line(name, coords, r, ma):
    c = bpy.data.curves.new(name, 'CURVE')
    c.dimensions = '3D'
    c.resolution_u = 20
    c.bevel_depth = r
    c.bevel_resolution = 3
    s = c.splines.new('POLY')
    s.points.add(len(coords) - 1)
    for p, co in zip(s.points, coords):
        p.co = (*co, 1)
    o = bpy.data.objects.new(name, c)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(ma)
    return o

def beam(name, a, b, r, ma):
    return line(name, [a, b], r, ma)

def fabric_mesh(name, nx, ny, fn, ma, solid=0.008):
    vs = [fn(i / nx, j / ny) for j in range(ny + 1) for i in range(nx + 1)]
    fs = []
    for j in range(ny):
        for i in range(nx):
            k = j * (nx + 1) + i
            fs.append((k, k + 1, k + nx + 2, k + nx + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(vs, [], fs)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(ma)
    for p in me.polygons:
        p.use_smooth = True
    sub = o.modifiers.new('Fabric smoothing', 'SUBSURF')
    sub.levels = 1
    if solid:
        so = o.modifiers.new('Hem thickness', 'SOLIDIFY')
        so.thickness = solid
    return o

def cushion(name, loc, dim, ma, rot=(0, 0, 0)):
    o = cube(name, loc, dim, ma, min(dim) * 0.34)
    o.rotation_euler = rot
    return o

def area(name, loc, target, power, color, size, size_y=None):
    d = bpy.data.lights.new(name, 'AREA')
    d.energy = power
    d.color = color
    d.shape = 'RECTANGLE'
    d.size = size
    d.size_y = size_y or size
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - o.location).to_track_quat('-Z', 'Y').to_euler()
    return o