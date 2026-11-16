from pathlib import Path
import json,subprocess,os
B=Path('/workspace/audit-v0.9.48');D=B/'customer-build/OandG_Workbench';out=[]
for name in ['OandG_Workbench','PetroWorkbench','SeismicWorkbench','GeosteeringWorkbench','CorrelationWorkbench']:
 for mode,folder in [('unlicensed','/tmp/audit0948-frozen-empty'),('owner_trust_rejected','/tmp/audit0948-owner-resolved-workflow/local')]:
  env=os.environ.copy();env.update(DISPLAY=':100',APPDATA=folder,LOCALAPPDATA=folder,MPLCONFIGDIR='/tmp/audit0948-frozen-mpl',LD_LIBRARY_PATH='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib');log=B/(name+'-frozen-'+mode+'.log')
  with log.open('w') as h:r=subprocess.run([str(D/name),'--self-test'],env=env,stdout=h,stderr=subprocess.STDOUT,timeout=90)
  out.append({'name':name,'mode':mode,'exit_code':r.returncode});(B/'frozen-launch-evidence.json').write_text(json.dumps(out,indent=2));print(out[-1],flush=True)
