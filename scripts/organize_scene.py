import bpy

def organize():
 bpy.context.scene.unit_settings.system='METRIC'
 bpy.context.scene.unit_settings.length_unit='METERS'
 groups={name:bpy.data.collections.get(name) or bpy.data.collections.new(name) for name in ['01 Architecture','02 Walnut Furniture','03 Textiles','04 Plants and Styling','05 Lighting','06 Cameras','07 Exterior','08 Kitchen and Accessories']}
 for c in groups.values():
  if c.name not in bpy.context.scene.collection.children:bpy.context.scene.collection.children.link(c)
 for o in list(bpy.context.scene.objects):
  n=o.name.lower()
  if o.type=='CAMERA' or n.startswith(('01 |','02 |','03 |')):key='06 Cameras'
  elif o.type=='LIGHT' or any(x in n for x in ['lamp','light pool','luminous','candle flame']):key='05 Lighting'
  elif n.startswith(('distant','sky background')):key='07 Exterior'
  elif any(x in n for x in ['planter','plant','leaf','midrib','pothos','fern','ficus','olive twig','olive sprig','botanical','shelf art book','shelf ceramic','shelf vessel','vase','candle']):key='04 Plants and Styling'
  elif any(x in n for x in ['pillow','duvet','runner','rug','curtain','cushion','upholstered']):key='03 Textiles'
  elif any(x in n for x in ['sofa','bed','coffee table','coffee tabletop','lower shelf','dining','chair','refrigerator','display shelf','shelf concealed']):key='02 Walnut Furniture'
  elif any(x in n for x in ['floor','oak plank','starter plank','wall','ceiling','window','glazing','balcony','skirting','cornice']):key='01 Architecture'
  else:key='08 Kitchen and Accessories'
  target=groups[key]
  for c in list(o.users_collection):c.objects.unlink(o)
  target.objects.link(o)

if __name__=='__main__':
 organize();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
