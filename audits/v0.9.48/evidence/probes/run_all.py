from pathlib import Path
import subprocess,os,json,time,sys
B=Path('/workspace/audit-v0.9.48');R=B/'OandG_Workbench_v0.9.48';env=os.environ.copy();env.update(DISPLAY=':98',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR='/tmp/audit0948-mpl',APPDATA='/tmp/audit0948-settings',LOCALAPPDATA='/tmp/audit0948-settings')
start=time.perf_counter()
with (B/'full-tests.log').open('w') as h:
 r=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','--durations=25','--junitxml='+str(B/'full-results.xml')],cwd=R,env=env,stdout=h,stderr=subprocess.STDOUT)
result={'exit_code':r.returncode,'seconds':time.perf_counter()-start};(B/'full-run-status.json').write_text(json.dumps(result,indent=2));print('full',result,flush=True)
if r.returncode not in (0,1):
 O=B/'isolated-tests';O.mkdir(exist_ok=True);results=[];files=sorted((R/'tests').glob('test_*.py'))
 for i,p in enumerate(files):
  t=time.perf_counter()
  with (O/(p.stem+'.log')).open('w') as h:
   try:r=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(p),'--junitxml='+str(O/(p.stem+'.xml'))],cwd=R,env=env,stdout=h,stderr=subprocess.STDOUT,timeout=420);code=r.returncode
   except subprocess.TimeoutExpired:code='timeout'
  results.append({'file':p.name,'exit_code':code,'seconds':time.perf_counter()-t});(B/'isolated-results.json').write_text(json.dumps(results,indent=2));print(i+1,len(files),p.name,code,round(time.perf_counter()-t,2),flush=True)
