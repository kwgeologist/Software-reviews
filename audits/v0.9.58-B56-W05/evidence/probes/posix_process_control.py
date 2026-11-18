"""Read-only B56-W05 verification. Runs simulated dates; never changes the OS clock.
Tests compiled package extensions, NOT the frozen customer executable.
Save outside Workbench. Output and isolated state also stay outside the source/package.
"""
from pathlib import Path
import argparse,sys,os,json,hashlib,subprocess,tempfile,time,traceback
from contextlib import contextmanager
from datetime import datetime,timedelta,timezone
EXPECTED={'licensing':'0df011b565ec4be36f9beefc56044be6214896443850a06a1c7d587c872d2bc6','license_runtime':'d89050dca5aab2379e5e44bbdc6ab1d752bdf6e481f8553a6f01fd5944ad1e20'}
BEFORE=datetime(2027,2,1,tzinfo=timezone.utc);AFTER=datetime(2027,3,15,tzinfo=timezone.utc)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bootstrap(checkout,package,out):
 sys.path.insert(0,str(checkout))
 from ogcore import licensing,license_runtime
 (out/f'origins-{os.getpid()}.json').write_text(json.dumps({'licensing':licensing.__file__,'license_runtime':license_runtime.__file__},indent=2))
 return licensing,license_runtime
p=argparse.ArgumentParser();p.add_argument('--checkout',required=True);p.add_argument('--package',required=True);p.add_argument('--out',required=True);p.add_argument('--role',default='parent',choices=['parent','check','remember','hold']);p.add_argument('--state');p.add_argument('--license');p.add_argument('--keys');p.add_argument('--ready');p.add_argument('--release');p.add_argument('--index',type=int,default=0);p.add_argument('--skip-pytest',action='store_true');a=p.parse_args()
C=Path(a.checkout).resolve();D=Path(a.package).resolve();O=Path(a.out).resolve()
if O.is_relative_to(C) or O.is_relative_to(D):raise SystemExit('Output must be outside the checkout and package.')
O.mkdir(parents=True,exist_ok=True)
if sys.platform!='linux':raise SystemExit('Linux source-only control')
if sys.version_info[:2]!=(3,12):raise SystemExit('Use py -3.12: the pinned package extensions are cp312-win_amd64.')
L,LR=bootstrap(C,D,O)
def clock(path):return L.ClockState(path,L.PlainProtector())
def check(path,data,keys,when):return L.check('geo',now=when,clock=clock(path),license_result=L.verify_bytes(data,now=when,keys=keys))
if a.role!='parent':
 state=Path(a.state)
 if a.role=='check':print(json.dumps({'status':check(state,Path(a.license).read_bytes(),json.loads(Path(a.keys).read_text()),BEFORE).status.value}));raise SystemExit(0)
 if a.role=='remember':
  for k in range(40):clock(state).remember(BEFORE+timedelta(seconds=a.index*40+k))
  raise SystemExit(0)
 from ogcore import safeio
 original=safeio.atomic_write
 @contextmanager
 def held(path,*args,**kw):
  if Path(path)==state:
   Path(a.ready).write_text('state read; lock held')
   deadline=time.monotonic()+45
   while not Path(a.release).exists():
    if time.monotonic()>deadline:raise TimeoutError('Scheduling release not received')
    time.sleep(.02)
  with original(path,*args,**kw)as h:yield h
 safeio.atomic_write=held
 clock(state).remember(BEFORE+timedelta(minutes=1));raise SystemExit(0)
result={'classification':'Linux Python source only, POSIX locking and PlainProtector; no Windows package execution','package':str(D),'checkout':str(C),'host_clock_changed':False,'source_or_package_modified':False,'cases':{}}
try:
 with tempfile.TemporaryDirectory(prefix='B56-W05-')as td:
  T=Path(td);os.environ.update(PYTHONDONTWRITEBYTECODE='1',LOCALAPPDATA=str(T/'Local'),APPDATA=str(T/'Roaming'))
  os.environ.pop('OGW_LICENSE_FILE',None);os.environ.pop('OGW_LICENSE_MANAGER_HOME',None)
  from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
  from license_manager import issuer
  key=Ed25519PrivateKey.generate();keys={'audit-only':issuer.public_key_text(key)}
  def make(expires=datetime(2027,3,1,tzinfo=timezone.utc),license_id=''):
   req=issuer.LicenseRequest('Isolated audit','Synthetic','evaluation',issued_at=datetime(2027,1,1,tzinfo=timezone.utc),expires_at=expires,license_id=license_id)
   return issuer.sign(issuer.payload_for(req,'audit-only'),key,'audit-only')
  data=make();licensefile=T/'test.ogwlic';licensefile.write_bytes(data);keyfile=T/'public-keys.json';keyfile.write_text(json.dumps(keys))
  base=[sys.executable,str(Path(__file__).resolve()),'--checkout',str(C),'--package',str(D),'--out',str(O)]
  def child(role,state,*extra):return subprocess.Popen(base+['--role',role,'--state',str(state),'--license',str(licensefile),'--keys',str(keyfile),*extra],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  state=T/'sequential.bin';v=check(state,data,keys,BEFORE);e=check(state,data,keys,AFTER);assert v.ok and e.status==L.Status.EXPIRED
  restarted=child('check',state);stdout,stderr=restarted.communicate(timeout=120);assert restarted.returncode==0,stderr;assert json.loads(stdout)['status']=='expired'
  imported=L.install_license(data,target=T/'target.ogwlic',now=BEFORE,keys=keys,clock=clock(state));assert imported.status==L.Status.EXPIRED
  renewed=make(datetime(2028,3,1,tzinfo=timezone.utc),e.license_id);installed=L.install_license(renewed,target=T/'target.ogwlic',now=BEFORE,keys=keys,clock=clock(state));assert installed.ok
  assert check(state,data,keys,BEFORE).status==L.Status.EXPIRED;assert check(state,renewed,keys,BEFORE).ok
  assert json.loads(state.read_bytes())['expired']
  result['cases']['POSIX_plain_restart_reimport_renewal_original_denied']='passed'
  state=T/'concurrent.bin';assert check(state,data,keys,BEFORE).ok;workers=[child('remember',state,'--index',str(i))for i in range(4)];e=check(state,data,keys,AFTER)
  for w in workers:
   stdout,stderr=w.communicate(timeout=120);assert w.returncode==0,stderr
  assert e.status==L.Status.EXPIRED and check(state,data,keys,BEFORE).status==L.Status.EXPIRED
  result['cases']['POSIX_plain_concurrent_processes']='passed'
  state=T/'timeout.bin';assert check(state,data,keys,BEFORE).ok;ready=T/'ready';release=T/'release';holder=child('hold',state,'--ready',str(ready),'--release',str(release));deadline=time.monotonic()+20
  while not ready.exists():
   if holder.poll()is not None:raise RuntimeError(holder.communicate()[1])
   if time.monotonic()>deadline:raise TimeoutError('Holder did not become ready')
   time.sleep(.02)
  try:
   started=time.monotonic();e=check(state,data,keys,AFTER);wait=time.monotonic()-started;present=clock(state).expired_on(e.identity)is not None
  finally:release.write_text('continue')
  stdout,stderr=holder.communicate(timeout=120);assert holder.returncode==0,stderr
  after_holder=clock(state).expired_on(e.identity)is not None
  restarted=child('check',state);stdout,stderr=restarted.communicate(timeout=120);assert restarted.returncode==0,stderr
  restart_status=json.loads(stdout)['status']
  replay=check(state,data,keys,BEFORE)
  target=T/'timeout-installed.ogwlic'
  reimport=L.install_license(data,target=target,now=BEFORE,keys=keys,clock=clock(state))
  renewal=make(datetime(2028,3,1,tzinfo=timezone.utc),e.license_id)
  renewal_install=L.install_license(renewal,target=target,now=BEFORE,keys=keys,clock=clock(state))
  old_after_renewal=check(state,data,keys,BEFORE).status.value
  renewed_status=check(state,renewal,keys,BEFORE).status.value
  case={'expired_status':e.status.value,'detail':e.detail,'wait_seconds':wait,'record_present_before_holder_release':present,'record_present_after_holder_release':after_holder,'restart_status':restart_status,'rollback_status':replay.status.value,'reimport_status':reimport.status.value,'renewal_status':renewal_install.status.value,'original_after_renewal':old_after_renewal,'renewal_check_status':renewed_status,'pending_files_after_merge':len(list(state.parent.glob(state.name+'.expired-*'))),'reproduced':replay.status==L.Status.VALID}
  result['cases']['POSIX_plain_real_lock_timeout']=case
  assert e.status==L.Status.EXPIRED and wait>=10 and present and after_holder,case
  assert restart_status==replay.status.value==reimport.status.value==old_after_renewal=='expired',case
  assert renewal_install.ok and renewed_status=='valid',case
  result['verdict_for_timeout_probe']='still reproducible'if result['cases']['POSIX_plain_real_lock_timeout']['reproduced']else'held-lock regression passed'
except BaseException as exc:
 result['error']=repr(exc);result['traceback']=traceback.format_exc()
finally:
 (O/'posix-process-replay.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
raise SystemExit(1 if result.get('error')or result.get('pytest_exit_code',0)!=0 or result.get('cases',{}).get('POSIX_plain_real_lock_timeout',{}).get('reproduced')else 0)
