import bpy, os, sys, time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=bpy.context.scene
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
mode=args[0] if args else 'checks'
if mode=='checks':
 s.render.engine='BLENDER_EEVEE';s.render.resolution_percentage=50;s.eevee.taa_render_samples=24
 for f in [1,144,145,240,241,360]:
  s.frame_set(f);s.render.filepath=os.path.join(ROOT,'renders',f'qa/check_{f:03}.png');bpy.ops.render.render(write_still=True);print('DONE',f,flush=True)
elif mode=='film':
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=64;s.eevee.use_raytracing=True;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
 os.makedirs(os.path.join(ROOT,'renders','frames'),exist_ok=True)
 for f in range(int(args[1]) if len(args)>1 else 1, (int(args[2]) if len(args)>2 else 360)+1):
  path=os.path.join(ROOT,'renders','frames',f'{f:04}.png')
  if os.path.exists(path):continue
  s.frame_set(f);s.render.filepath=path;bpy.ops.render.render(write_still=True);print('FILM_FRAME',f,flush=True)
elif mode=='stills':
 s.render.engine='BLENDER_EEVEE';s.eevee.use_raytracing=True;s.eevee.taa_render_samples=256;s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
 for f,name in [(1,'01_overview'),(195,'02_living_detail'),(300,'03_window_dining')]:
  s.frame_set(f);s.render.filepath=os.path.join(ROOT,'renders',name+'.png');bpy.ops.render.render(write_still=True);print('STILL',name,flush=True)
