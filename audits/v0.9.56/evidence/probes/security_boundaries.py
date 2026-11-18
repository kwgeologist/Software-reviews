from pathlib import Path
import os,sys,json,tempfile
from unittest.mock import patch
from datetime import datetime,timedelta,timezone
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56';sys.path[:0]=[str(R),str(R/'tests')]
from ogcore import licensing,userdata
from license_manager import issuer
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
out={}
with tempfile.TemporaryDirectory() as td:
 td=Path(td);old=os.getcwd();os.chdir(td)
 try:
  with patch.dict(os.environ,{'LOCALAPPDATA':'.','APPDATA':'.'},clear=False):
   out['relative_appdata']={'preferences':str(userdata.preference_file('.audit-prefs').resolve()),'licensing_state':str(licensing.state_path().resolve()),'owner_home':str(issuer.home().resolve()),'write_succeeded':userdata.write_preference('.audit-prefs','audit only'),'current_project_folder':str(td),'files_created':[str(p.relative_to(td)) for p in td.rglob('*')if p.is_file()]}
 finally:os.chdir(old)
 key=Ed25519PrivateKey.generate();keyid='audit-not-shipped';keys={keyid:issuer.public_key_text(key)};now=datetime(2026,11,1,tzinfo=timezone.utc);req=issuer.LicenseRequest('Audit only','Synthetic', 'evaluation',tuple(licensing.MODULES),issued_at=now,expires_at=now+timedelta(days=10));data=issuer.sign(issuer.payload_for(req,keyid),key,keyid);clock=licensing.ClockState(td/'clock.bin',licensing.PlainProtector());results=[]
 for t in [now+timedelta(days=5),now+timedelta(days=20),now+timedelta(days=5)]:
  verified=licensing.verify_bytes(data,now=t,keys=keys);r=licensing.check('geo',now=t,license_result=verified,clock=clock);results.append({'simulated_clock':str(t),'status':r.status.value,'watermark':str(clock.latest())})
 out['expired_then_clock_restored']={'results':results,'signature_required':True,'explicit_test_key_injection_only':True,'state_deleted_or_modified':False,'host_clock_changed':False,'scope':'pure source algorithm; no test key added to shipped trust'}
(B/'security-boundaries-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
