import os,subprocess,json,time
from pathlib import Path
B=Path('/workspace/audit-v0.9.39');R=B/'OandG_Workbench_v0.9.39';out=[]
for script in ['app.py','petro_app.py','seismic_app.py','geosteer_app.py','correlation_app.py']:
 env=os.environ.copy();d=Path('/tmp/audit0939-selftests')/script[:-3];d.mkdir(parents=True,exist_ok=True);env.update(DISPLAY=':99',PYTHONDONTWRITEBYTECODE='1',APPDATA=str(d),LOCALAPPDATA=str(d),MPLCONFIGDIR=str(d/'mpl'),XDG_CACHE_HOME=str(d/'cache'))
 t=time.perf_counter()
 with (B/(script[:-3]+'-self-test.log')).open('w') as log:
  try:r=subprocess.run(['/tmp/audit0939-venv/bin/python',script,'--self-test'],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 out.append({'script':script,'exit_code':code,'seconds':time.perf_counter()-t});(B/'self-tests.json').write_text(json.dumps(out,indent=2));print(out[-1],flush=True)
