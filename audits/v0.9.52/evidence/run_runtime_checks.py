from pathlib import Path
import os,subprocess,json,time,sys
B=Path('/workspace/audit-v0.9.52');R=B/'OandG_Workbench_v0.9.52';C=B/'compiled-worktree';D=B/'customer-build/OandG_Workbench';PY=sys.executable
folder=Path('/tmp/audit0952-owner-workflow');env=os.environ.copy();env.update(DISPLAY=':100',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR='/tmp/audit0952-runtime-mpl',APPDATA='/tmp/audit0952-runtime-empty',LOCALAPPDATA='/tmp/audit0952-runtime-empty')
results=[]
def run(label,args,cwd,e):
 start=time.perf_counter()
 with (B/(label+'.log')).open('w') as h:
  try:r=subprocess.run(args,cwd=cwd,env=e,stdout=h,stderr=subprocess.STDOUT,timeout=150);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 results.append({'label':label,'exit_code':code,'seconds':time.perf_counter()-start});(B/'runtime-results.json').write_text(json.dumps(results,indent=2));print(results[-1],flush=True)
run('owner-protection',[PY,str(R/'tools/release/check_protected.py'),'--owner',str(B/'owner-build/OandG_Workbench_License_Manager')],B,env)
run('customer-protection',[PY,str(R/'tools/release/check_protected.py'),str(D)],B,env)
run('owner-self-test',[str(B/'owner-build/OandG_Workbench_License_Manager'),'self-test',str(folder)],B,env)
for script,name in [('app.py','OandG_Workbench'),('petro_app.py','PetroWorkbench'),('seismic_app.py','SeismicWorkbench'),('geosteer_app.py','GeosteeringWorkbench'),('correlation_app.py','CorrelationWorkbench')]:
 for phase,root,licensed,frozen in [('source-unlicensed',R,False,False),('source-licensed',R,True,False),('compiled-licensed',C,True,False),('frozen-unlicensed',D,False,True),('frozen-owner-trust',D,True,True)]:
  e=env.copy();home=str(folder/'local') if licensed else '/tmp/audit0952-runtime-empty';e.update(APPDATA=home,LOCALAPPDATA=home)
  run(phase+'-'+name,([str(D/name),'--self-test'] if frozen else [PY,script,'--self-test']),root,e)
