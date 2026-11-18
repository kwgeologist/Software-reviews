from pathlib import Path
import sys,tempfile,json,threading,time
from contextlib import contextmanager
from unittest.mock import patch
from datetime import datetime,timedelta,timezone
B=Path('/workspace/verify-v0.9.57-B56-W05');C=B/'checkout';sys.path.insert(0,str(C))
from ogcore import licensing,safeio
from license_manager import issuer
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
before=datetime(2027,2,1,tzinfo=timezone.utc);after=datetime(2027,3,15,tzinfo=timezone.utc);key=Ed25519PrivateKey.generate();keys={'probe':issuer.public_key_text(key)};data=issuer.sign(issuer.payload_for(issuer.LicenseRequest('Audit','Synthetic','evaluation',issued_at=datetime(2027,1,1,tzinfo=timezone.utc),expires_at=datetime(2027,3,1,tzinfo=timezone.utc)),'probe'),key,'probe')
with tempfile.TemporaryDirectory()as td:
 state=Path(td)/'state.bin';clock=lambda:licensing.ClockState(state,licensing.PlainProtector());result=licensing.verify_bytes(data,now=before,keys=keys);licensing.check('geo',now=before,clock=clock(),license_result=result);ready=threading.Event();release=threading.Event();errors=[];real=safeio.atomic_write
 @contextmanager
 def delayed(path,*args,**kw):
  if threading.current_thread().name=='held-state-writer' and Path(path)==state:
   ready.set()
   if not release.wait(30):raise TimeoutError('audit scheduler timed out')
  with real(path,*args,**kw)as h:yield h
 def writer():
  try:clock().remember(before+timedelta(minutes=1))
  except Exception as e:errors.append(repr(e))
 with patch.object(safeio,'atomic_write',delayed):
  t=threading.Thread(target=writer,name='held-state-writer');t.start();assert ready.wait(10);started=time.monotonic();expired=licensing.check('geo',now=after,clock=clock(),license_result=licensing.verify_bytes(data,now=after,keys=keys));seconds=time.monotonic()-started;seen_before_release=clock().expired_on(expired.identity)is not None;release.set();t.join(10)
 replay=licensing.check('geo',now=before,clock=clock(),license_result=licensing.verify_bytes(data,now=before,keys=keys));out={'checkout_commit':'ed117d8bbf66d7be9e67827831fb33dae2cb7a23','runtime':'Linux Python source, PlainProtector','licensing_origin':licensing.__file__,'expired_check_status':expired.status.value,'expired_write_wait_seconds':seconds,'expiry_record_present_before_old_writer_finishes':seen_before_release,'expiry_record_present_after_old_writer_finishes':clock().expired_on(expired.identity)is not None,'rollback_status':replay.status.value,'writer_errors':errors,'state_or_license_tampered':False,'host_clock_changed':False,'ordering_hook':'paused one writer after reading state while holding its lock; production lock timeout unchanged'}
(B/'lock-timeout-replay-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
