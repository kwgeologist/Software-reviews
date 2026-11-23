from pathlib import Path
import os,subprocess,time,json,concurrent.futures
B=Path('/workspace/audit-v0.9.70-tk-segfault');P='/workspace/audit-v0.9.56-windows/tooling/bin/python';X='/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb'
def run(v,display):
 out=[];root=B/'runs'/f'B-{v}';root.mkdir(exist_ok=True);e=os.environ.copy();e.update(DISPLAY=f':{display}',PYTHONPATH=(':'.join(([str(B/'tk86-extension')]if v=='86'else[])+['/workspace/audit-v0.9.68-full/deps'])),PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1');x=subprocess.Popen([X,e['DISPLAY'],'-screen','0','1600x1000x24','-nolisten','tcp'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.2)
 try:
  for mode in ['normal','destroy']:
   cmd=[P,'-X','faulthandler',str(B/'probes/lifecycle.py'),mode,'200',str(root/(mode+'.jsonl'))];start=time.time()
   with (root/(mode+'.log')).open('w')as f:r=subprocess.run(cmd,env=e,stdout=f,stderr=subprocess.STDOUT,timeout=600)
   out.append({'mode':mode,'command':cmd,'exit_code':r.returncode,'seconds':time.time()-start});(root/'status.json').write_text(json.dumps(out,indent=2))
 finally:x.terminate();x.wait()
 return out
with concurrent.futures.ThreadPoolExecutor(2)as pool:results=list(pool.map(lambda args:run(*args),[('86',223),('9',224)]))
(B/'lifecycle-summary.json').write_text(json.dumps(results,indent=2))
