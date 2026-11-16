import os,subprocess,json,time
from pathlib import Path
B=Path('/workspace/audit-v0.9.48');R=B/'compiled-worktree';out=[]
for script in ['app.py','petro_app.py','seismic_app.py','geosteer_app.py','correlation_app.py']:
 env=os.environ.copy();d=Path('/tmp/audit0948-owner-resolved-workflow/local');d.mkdir(parents=True,exist_ok=True);env.update(DISPLAY=':100',PYTHONDONTWRITEBYTECODE='1',APPDATA=str(d),LOCALAPPDATA=str(d),MPLCONFIGDIR=str(d/'mpl'),XDG_CACHE_HOME=str(d/'cache'))
 t=time.perf_counter()
 with (B/(script[:-3]+'-compiled-licensed-self-test.log')).open('w') as log:
  try:r=subprocess.run(['/workspace/audit-tooling-v048/bin/python',script,'--self-test'],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 out.append({'script':script,'exit_code':code,'seconds':time.perf_counter()-t});(B/'compiled-licensed-self-tests.json').write_text(json.dumps(out,indent=2));print(out[-1],flush=True)
