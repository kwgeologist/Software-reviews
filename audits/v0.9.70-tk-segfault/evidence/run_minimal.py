import sys,os,json,subprocess,time
from pathlib import Path
B=Path('/workspace/audit-v0.9.70-tk-segfault');sys.path.insert(0,str(B));from run_experiments import env,P,X,G
root=B/'runs/minimal';root.mkdir(exist_ok=True);x=subprocess.Popen([X,':226','-screen','0','1600x1000x24','-nolisten','tcp'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.2);out=[]
try:
 for v in ['86','9']:
  e=env(v,226,root)
  for mode in ['main','worker']:
   cmd=[P,'-X','faulthandler',str(B/'probes/minimal_gc.py'),mode]
   with (root/f'gc-{v}-{mode}.log').open('w')as h:r=subprocess.run(cmd,env=e,stdout=h,stderr=subprocess.STDOUT)
   out.append({'version':v,'experiment':'controlled_gc','mode':mode,'exit_code':r.returncode,'command':cmd})
  for mode in ['tk-only','mpl']:
   cmd=[P,'-X','faulthandler',str(B/'probes/minimal_canvas.py'),mode,'200',str(root/f'canvas-{v}-{mode}.jsonl')]
   with (root/f'canvas-{v}-{mode}.log').open('w')as h:r=subprocess.run(cmd,env=e,stdout=h,stderr=subprocess.STDOUT,timeout=300)
   out.append({'version':v,'experiment':'canvas','mode':mode,'exit_code':r.returncode,'command':cmd})
  e['LD_LIBRARY_PATH']=str(B/'native/root/usr/lib/x86_64-linux-gnu');cmd=[G,'--batch','-ex','set pagination off','-ex','set debuginfod enabled off','-ex','run','-ex','thread apply all bt 35','-ex','info sharedlibrary','--args',P,'-X','faulthandler',str(B/'probes/minimal_gc.py'),'worker']
  with (root/f'native-gc-{v}-worker.log').open('w')as h:r=subprocess.run(cmd,env=e,stdout=h,stderr=subprocess.STDOUT,timeout=90)
  out.append({'version':v,'experiment':'native_controlled_gc','mode':'worker','gdb_exit_code':r.returncode,'command':cmd})
  (B/'minimal-summary.json').write_text(json.dumps(out,indent=2))
finally:x.terminate();x.wait()
