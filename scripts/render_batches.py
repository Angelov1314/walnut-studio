"""Render in fresh Blender processes; safely resume from existing frames."""
from pathlib import Path
import subprocess, sys
import os
ROOT=Path(__file__).resolve().parent.parent
BLENDER=os.environ.get('BLENDER_BIN','blender')
start=int(sys.argv[1]) if len(sys.argv)>1 else 1
for a in range(start,361,60):
 b=min(a+59,360)
 with (ROOT/'renders'/f'film_{a}.log').open('w') as log:
  result=subprocess.run([BLENDER,'-b',str(ROOT/'Walnut_Studio.blend'),'-t','6','--python',str(ROOT/'scripts'/'render.py'),'--','film',str(a),str(b)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
 if result.returncode:raise SystemExit(f'Blender batch {a}-{b} failed ({result.returncode}); resume from {a}.')
 print(f'BATCH_COMPLETE {a}-{b}',flush=True)
