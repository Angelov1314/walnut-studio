import bpy, math, random, os, sys
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from geometry import *
random.seed(42)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'reference/base_scene.blend'))
s=bpy.context.scene

def delete_prefix(*prefixes):
 for o in list(bpy.data.objects):
  if any(o.name.startswith(p) for p in prefixes):bpy.data.objects.remove(o,do_unlink=True)
def assign(o,m):o.data.materials.clear();o.data.materials.append(m)
def color(name,c,rough=None):
 m=bpy.data.materials[name];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);m.diffuse_color=(*c,1)
 if rough is not None:p.inputs['Roughness'].default_value=rough
 return m
# Reference palette, quieter microtexture rather than coarse bump.
olive=color('Forest sage woven upholstery',(.145,.17,.067),.81)
throw=color('Sage cotton throw',(.205,.235,.113),.91)
cream=color('Warm ivory pillowcase',(.80,.735,.61),.87)
color('Dove grey cotton duvet',(.78,.73,.63),.93)
color('Petrol blue curtain linen',(.075,.13,.12),.86)
color('Warm ivory | mineral plaster',(.68,.64,.55),.87)
for m in bpy.data.materials:
 if m.use_nodes:
  for n in m.node_tree.nodes:
   if n.type=='BUMP':
    n.inputs['Distance'].default_value=min(n.inputs['Distance'].default_value,.0025)
    n.inputs['Strength'].default_value=min(n.inputs['Strength'].default_value,.23)
# Walnut has directional fine grain and a subdued satin finish.
walnut=wood('WALNUT | horizontal grain',(.20,.085,.034))
for n in walnut.node_tree.nodes:
 if n.type=='BUMP':n.inputs['Distance'].default_value=.002
walnut_x=walnut.copy();walnut_x.name='WALNUT | long table grain'
for n in walnut_x.node_tree.nodes:
 if n.type=='VECT_MATH':n.inputs[1].default_value=(.28,5,7)
white=bpy.data.materials['Chalk white enamel']
linen=bpy.data.materials['Unbleached linen weave']
bronze=mat('Brushed aged brass',(.29,.19,.085),.28,.78)
black=mat('Espresso metal',(.024,.021,.016),.31,.55)
ceramic=mat('Chalk ceramic glaze',(.65,.56,.42),.29,noise=.08,scale=160)
terracotta=mat('Warm clay planter',(.23,.115,.064),.83,noise=.12,scale=95)
soil=mat('Dark potting soil',(.022,.015,.008),.95,noise=.3,scale=85)
leafmats=[mat('Botanical leaf %d'%i,(.026+i*.016,.073+i*.020,.014+i*.006),.39) for i in range(4)]
for m in leafmats:
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.075
vein=mat('Leaf central vein',(.085,.12,.026),.65)
for o in bpy.data.objects:
 if o.type=='MESH' and any(o.name.startswith(x) for x in ['Sofa timber','Sofa oak','Oak bed','Oak headboard','Dining tabletop','Island oak']):assign(o,walnut)
# Open up the tailored sofa; use real seat and back cushions.
delete_prefix('Sage loose sofa throw','Padded headboard')
# Walnut headboard face and restrained rail moulding.
cube('Walnut headboard center panel',(-1.866,5.22,1.01),(.032,1.52,.65),walnut,.009)
for z in [.64,1.39]:cube('Walnut headboard horizontal rail',(-1.85,5.22,z),(.057,1.70,.065),walnut,.009)
for y in [4.405,6.035]:cube('Walnut headboard stile',(-1.85,y,1.005),(.057,.065,.73),walnut,.009)
cube('Walnut bed foot rail',(.345,5.22,.32),(.075,1.63,.36),walnut,.018)
for y in [4.395,6.045]:cube('Walnut side rail',(-.78,y,.30),(2.27,.065,.24),walnut_x,.009)
# Tidy cotton with irregular low-amplitude wrinkles, avoiding repeated accordion folds.
def duvet_height(u,v):
 z=.687+.005*sin(u*13+v*9)*sin(pi*v)+.003*sin(v*27+u*14)+.007*math.exp(-((u-.75)*10)**2)*sin(v*19+u*3)
 return z-max(0,(abs(v-.5)-.425)/.075)*.28-max(0,u-.91)/.09*.24
for j in range(75):
 for i in range(73):
  u=i/72;v=j/74;bpy.data.objects['Soft folded bed duvet'].data.vertices[j*73+i].co=(-1.24+u*1.71,4.37+v*1.70,duvet_height(u,v))
for j in range(53):
 for i in range(49):
  x=-.07+i/48*.45;y=4.38+j/52*1.68;u=(x+1.24)/1.71;v=(y-4.37)/1.70
  bpy.data.objects['Folded cotton bed runner'].data.vertices[j*49+i].co=(x,y,duvet_height(u,v)+.022)

# White-base walnut coffee table, with a lower slatted shelf.
delete_prefix('Handmade tile','Tile diamond motif','Coffee table frame','Coffee table leg')
cube('Walnut coffee tabletop',(-.38,2.64,.48),(.86,1.43,.055),walnut,.014)
for x in [-.72,-.04]:
 for y in [2.07,3.21]:cube('Ivory coffee table leg',(x,y,.25),(.062,.062,.45),white,.012)
for x in [-.72,-.04]:cube('Ivory lower shelf side rail',(x,2.64,.155),(.055,1.2,.05),white,.007)
for j in range(9):cube('Ivory lower shelf slat',(-.38,2.09+j*.136,.165),(.70,.064,.028),white,.005)
# A warm woven rug subtly zones the lounge.
rug=mat('Natural oatmeal flatweave',(.35,.29,.20),.99,noise=.2,scale=380)
for n in rug.node_tree.nodes:
 if n.type=='BUMP':n.inputs['Distance'].default_value=.001
cube('Flatweave living rug',(-.43,2.62,.039),(1.65,2.23,.018),rug,.045)
# Recessed bedside cabinet in the clear gap between sofa and bed.
cube('Bedside ivory cabinet',(-1.68,4.025,.35),(.54,.51,.64),white,.016)
cube('Bedside open cubby',(-1.399,4.025,.26),(.006,.39,.19),black,.006)
cube('Bedside walnut top',(-1.68,4.025,.695),(.57,.54,.038),walnut,.009)
cube('Bedside drawer reveal',(-1.398,4.025,.515),(.009,.45,.003),black)
beam('Bedside brass pull',(-1.385,3.985,.57),(-1.385,4.065,.57),.006,bronze)
# Plants use curved leaf meshes, branches, central veins, soil and tapered pots.
def pot(name,loc,r,h,material):
 x,y,z=loc;vs=[];fs=[];profile=[(r*.76,0),(r,.93*h),(r,h),(r*.88,h),(r*.87,.92*h)]
 for radius,zz in profile:
  for k in range(48):a=2*pi*k/48;vs.append((x+radius*cos(a),y+radius*sin(a),z+zz))
 for j in range(len(profile)-1):
  for k in range(48):a=j*48+k;b=j*48+(k+1)%48;fs.append((a,b,b+48,a+48))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);assign(o,material)
 for p in me.polygons:p.use_smooth=True
 cyl(name+' soil',(x,y,z+h*.94),r*.86,.016,soil)
 return Vector((x,y,z+h))
def leaf(name,base,direction,length,width,ma):
 a=Vector(base);d=Vector(direction).normalized();side=d.cross(Vector((0,0,1)))
 if side.length<.01:side=Vector((1,0,0))
 side.normalize();up=side.cross(d).normalized();vs=[];fs=[]
 for i in range(13):
  u=i/12;mid=a+d*length*u+up*(sin(u*pi)*length*.095-u*u*length*.065)
  for j in range(5):
   v=j/2-1;pt=mid+side*(sin(pi*u)**.8*width*.5*v)+up*(abs(v)**1.6*sin(pi*u)*width*.15);vs.append(tuple(pt))
 for i in range(12):
  for j in range(4):k=i*5+j;fs.append((k,k+1,k+6,k+5))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);assign(o,ma)
 for p in me.polygons:p.use_smooth=True
 line(name+' midrib',[tuple(a+d*length*u+up*(sin(u*pi)*length*.095-u*u*length*.065+.0007)) for u in [i/12 for i in range(13)]],.0007,vein)
 return o
def plant(name,loc,r=.12,h=.22,height=.42):
 base=pot(name+' planter',loc,r,h,ceramic if r<.15 else terracotta)
 for b in range(7):
  ang=b*2.399;end=base+Vector((cos(ang)*height*.22,sin(ang)*height*.22,height*(.6+random.random()*.4)))
  line(name+' branch',[tuple(base),tuple(base.lerp(end,.55)+Vector((.02,0,0))),tuple(end)],.0025 if r<.15 else .006,vein)
  for j in range(5):
   t=.25+j*.16;start=base.lerp(end,t)
   aa=ang+j*2.4;leaf(name+' leaf',start,(cos(aa),sin(aa),.38),height*.32,height*.15,random.choice(leafmats))
  leaf(name+' tip',end,(cos(ang),sin(ang),.8),height*.25,height*.12,leafmats[2])
plant('Bedside olive plant',(-1.7,4.02,.718),.077,.12,.24)
plant('Floor ficus',(1.68,2.96,.041),.21,.38,1.14)
# Bed far corner: small greenery, no tall foliage obstructing the balcony.
plant('Window fern',(-1.53,6.22,.30),.11,.21,.48)
# Replace toy-like daisies with olive twigs in the existing stoneware vase.
delete_prefix('Flower stem','Flower center','Golden flower petal')
base=Vector((-.39,2.93,.75))
for i in range(4):
 a=i*2.2;end=base+Vector((.11*cos(a),.11*sin(a),.24+random.random()*.13))
 beam('Olive twig',base,end,.002,vein)
 for j in range(7):
  t=.24+j*.10;ang=a+j*pi
  leaf('Olive sprig leaf',base.lerp(end,t),(cos(ang),sin(ang),.3),.075,.025,leafmats[2])
# Candle, stacked books and a ceramic bowl on the coffee table.
candlewax=mat('Ivory candle wax',(.71,.56,.35),.5)
cyl('Coffee table candle vessel',(-.14,2.70,.569),.059,.126,ceramic)
cyl('Candle wax surface',(-.14,2.70,.635),.049,.009,candlewax)
flame=mat('Candle warm flame',(1,.31,.035),.4);p=flame.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.28,.025,1);p.inputs['Emission Strength'].default_value=4
uv('Candle flame',(-.14,2.70,.663),(.008,.008,.024),flame,16,10)
beam('Candle wick',(-.14,2.70,.639),(-.14,2.70,.652),.002,black)
# Abstract botanical relief art, native geometry instead of external textures.
artpaper=mat('Art warm cotton paper',(.56,.49,.36),.96)
artink=mat('Art olive ink',(.075,.092,.038),.94)
artochre=mat('Art ochre ink',(.30,.16,.064),.95)
for y,phase in [(2.07,.2),(2.93,1.1)]:
 cube('Walnut botanical frame',(-2.004,y,1.98),(.038,.65,.80),walnut,.007)
 cube('Botanical paper',(-1.980,y,1.98),(.005,.595,.744),artpaper)
 for b in range(3):
  coords=[]
  for j in range(18):
   t=j/17;coords.append((-1.974,y-.16+b*.13+.035*sin(t*3+phase+b),1.69+t*(.39+.07*b)))
  line('Botanical print stem',coords,.0028,artink)
  for j in range(5):
   k=3+j*3;pos=Vector(coords[k]);o=uv('Botanical print leaf',pos+Vector((.001,(-1 if j%2 else 1)*.039,.018)),(.002,.049,.021),artink if b!=1 else artochre,20,10);o.rotation_euler[0]=(-.5 if j%2 else .5)
# Reveal the walnut dining top; add a narrow linen runner and styled shelf.
delete_prefix('Sage dining tablecloth')
cube('Dining oatmeal runner',(1.55,4.55,.811),(.40,1.34,.01),linen,.004)
cube('Floating walnut display shelf',(1.87,4.55,2.02),(.26,1.48,.055),walnut,.008)
for y in [4.02,5.08]:beam('Shelf concealed brass bracket',(2.02,y,1.87),(1.81,y,2.0),.009,bronze)
plant('Shelf trailing pothos',(1.84,4.10,2.052),.074,.12,.19)
for k in range(3):
 coords=[]
 for j in range(16):t=j/15;coords.append((1.70-.035*sin(t*pi),4.09+.05*k+.028*sin(t*5+k),2.09-t*(.33+.07*k)))
 line('Pothos trailing vine',coords,.002,vein)
 for j in range(2,16,2):leaf('Pothos heart leaf',coords[j],(-.15,(-1)**j,.12),.072,.049,random.choice(leafmats))
for j in range(5):
 m=[olive,linen,ceramic,walnut,artochre][j];cube('Shelf art book',(1.885,4.52+j*.047,2.19),(.17,.035,.275+random.random()*.06),m,.003)
uv('Shelf ceramic sculptural vessel',(1.86,5.04,2.16),(.069,.085,.11),ceramic)
cyl('Shelf vessel mouth',(1.86,5.04,2.27),.03,.05,ceramic)
# Replace the oversized original floor-lamp head with a smaller luminous petal lamp.
delete_prefix('Lamp heavy base','Arched floor lamp','Lamp crook','Lamp opal core','Layered shade petal')
cyl('Walnut edition lamp base',(-1.965,3.93,.073),.11,.09,bronze)
line('Walnut edition arched stem',[(-1.965,3.93,.10),(-1.965,3.93,1.76)]+[(-1.965+.54*(1-cos(t*pi/2)),3.93,1.76+.20*sin(t*pi)) for t in [j/40 for j in range(41)]],.010,bronze)
shade=mat('Warm parchment lamp petals',(.66,.48,.25),.59)
p=shade.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.52,.19,1);p.inputs['Emission Strength'].default_value=.7
for ring in range(4):
 for k in range(10):
  a=k*2*pi/10+(ring%2)*.3;r=.103+.017*sin(ring*pi/3)
  o=uv('Walnut lamp petal',(-1.425+r*cos(a),3.93+r*sin(a),1.52+ring*.055),(.048,.028,.060),shade,20,12);o.rotation_euler=(0,.32,a)
uv('Lamp luminous core',(-1.425,3.93,1.61),(.09,.09,.12),flame)
# Lighting: warm practical pools against a cooler dusk window.
for o in list(bpy.data.objects):
 if o.type=='LIGHT':bpy.data.objects.remove(o,do_unlink=True)
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.32,.43,.58,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.12
area('Dusk window softbox',(0,6.43,2.01),(-.6,2.2,.8),110,(.56,.70,1),2.9,2)
area('Camera soft warm bounce',(.6,.0,2.30),(-.7,3.7,.8),24,(1,.79,.53),2.6,1.8)
area('Quiet ceiling bounce',(.2,3.1,2.76),(0,3.5,0),9,(1,.83,.63),2.7,2.4)
area('Reading lamp warm wall pool',(-1.43,3.94,1.66),(-2.04,4.08,1.42),34,(1,.55,.24),.30,.3)
area('Reading lamp downward pool',(-1.43,3.94,1.51),(-1.65,4.03,.70),20,(1,.63,.32),.22,.22)
area('Bed headboard warm wash',(-2.015,5.18,1.60),(-2.04,5.18,1.95),7,(1,.53,.22),1.1,.06)
area('Bed floating toe light',(.39,5.22,.15),(.9,5.22,.02),8,(1,.55,.25),1.2,.06)
area('Botanical gallery soft graze',(-1.84,2.51,2.58),(-2,2.5,1.90),26,(1,.69,.39),1.15,.20)
area('Dining wall light pool',(1.77,4.6,1.75),(2.04,4.60,1.38),22,(1,.59,.28),.2,.22)
area('Dining shelf underlight',(1.91,4.55,1.98),(1.65,4.55,.78),13,(1,.69,.41),1.13,.035)
# Shade emission gets its own material so the room's white paint stays neutral.
sm=mat('Dining linen shade glow',(.72,.56,.31),.63);p=sm.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.62,.30,1);p.inputs['Emission Strength'].default_value=.5
assign(bpy.data.objects['Wall lamp shade'],sm)
for name,power,c in [('Soft blue exterior',.75,(.36,.51,.68)),('Distant warm concrete',.28,(.37,.43,.51)),('Distant muted glazing',.24,(.26,.35,.45))]:
 p=bpy.data.materials[name].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=power
cityglow=mat('Distant apartment warm windows',(.58,.33,.12),.6);p=cityglow.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.58,.24,1);p.inputs['Emission Strength'].default_value=.58
for o in bpy.data.objects:
 if o.name.startswith('Distant window') and random.random()<.17:assign(o,cityglow)
# A quiet built-in frame integrates the existing refrigerator into the walnut palette.
greige=mat('Warm greige appliance enamel',(.38,.36,.31),.38)
for o in bpy.data.objects:
 if o.name.startswith(('Tall refrigerator','Refrigerator door')):assign(o,greige)
cube('Walnut refrigerator side panel',(1.116,5.94,1.08),(.047,.77,2.15),walnut,.008)
cube('Walnut refrigerator top surround',(1.54,5.94,2.145),(.90,.77,.05),walnut,.009)

# Edit the shots to show walnut surfaces, décor, and light with slow parallax.
shots=[('01 | Entrance slow dolly',1,144,(.95,.22,1.54),(.69,1.02,1.50),(-.36,4.25,1.14),(-.41,4.47,1.11),21.5,23,5.6),('02 | Living textures slider',145,240,(.94,1.97,1.25),(.87,2.62,1.24),(-.58,2.81,.89),(-.80,3.07,1.04),35,37,3.2),('03 | Window and dining reveal',241,360,(.30,2.19,1.55),(.43,2.73,1.53),(-.13,5.0,1.13),(-.1,5.18,1.17),25,26,5.6)]
for name,f1,f2,a,b,ta,tb,la,lb,fstop in shots:
 o=bpy.data.objects[name];focus=bpy.data.objects[name+' focus'];o.animation_data_clear();o.data.animation_data_clear();focus.animation_data_clear();o.data.dof.aperture_fstop=fstop
 for f,pos,tgt,lens in [(f1,a,ta,la),(f2,b,tb,lb)]:
  o.location=pos;o.rotation_euler=(Vector(tgt)-Vector(pos)).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;focus.location=tgt
  o.keyframe_insert('location',frame=f);o.keyframe_insert('rotation_euler',frame=f);o.data.keyframe_insert('lens',frame=f);focus.keyframe_insert('location',frame=f)
s.render.engine='BLENDER_EEVEE';s.eevee.use_raytracing=True;s.eevee.taa_render_samples=64
s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.20
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=360;s.render.image_settings.file_format='PNG';s.render.filepath='//renders/frames/'
s.frame_set(72)
from organize_scene import organize
organize()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Walnut_Studio.blend'))
s.render.resolution_percentage=65;s.eevee.taa_render_samples=48
for f in [72,195,300]:
 s.frame_set(f);s.render.filepath=str(ROOT/'renders/qa'/f'preview_{f}.png');bpy.ops.render.render(write_still=True);print('PREVIEW_READY',f,flush=True)
