import os,sys,subprocess,time,json
from pathlib import Path
B=Path('/workspace/audit-v0.9.39');R=B/'OandG_Workbench_v0.9.39';O=B/'isolated-tests';O.mkdir(exist_ok=True)
env=os.environ.copy();env.update(DISPLAY=':98',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR='/tmp/audit0939-mpl',APPDATA='/tmp/audit0939-settings',LOCALAPPDATA='/tmp/audit0939-settings')
results=[];files=sorted((R/'tests').glob('test_*.py'));start=time.perf_counter()
for i,p in enumerate(files):
 t=time.perf_counter()
 with (O/(p.stem+'.log')).open('w') as h:
  try:r=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(p),'--junitxml='+str(O/(p.stem+'.xml'))],cwd=R,env=env,stdout=h,stderr=subprocess.STDOUT,timeout=300);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 results.append({'file':p.name,'exit_code':code,'seconds':time.perf_counter()-t});(B/'isolated-results.json').write_text(json.dumps(results,indent=2))
 print(i+1,len(files),p.name,code,round(time.perf_counter()-t,2),flush=True)
print('total seconds',time.perf_counter()-start)
