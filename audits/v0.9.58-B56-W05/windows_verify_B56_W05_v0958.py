"""Read-only B56-W05 verification. Runs simulated dates; never changes the OS clock.
Tests compiled package extensions, NOT the frozen customer executable.
Save outside Workbench. Output and isolated state also stay outside the source/package.
"""
from pathlib import Path
import argparse,sys,os,json,hashlib,subprocess,tempfile,time,traceback
from contextlib import contextmanager
from datetime import datetime,timedelta,timezone
EXPECTED={}  # v0.9.58 hashes recorded locally; customer ZIP transfer pending independent inspection
SOURCE_HASHES={'ogcore/licensing.py': 'e8b1abebfae454d0154b3fb3753cd4e8ddd79b7eaa3a39003cb8952472ee0f28', 'ogcore/license_runtime.py': 'b9191829b6d795b00d48b2087b27c1846db4bacc2177853bc21860028e0ff79c', 'ogcore/licensing_keys.py': '7a932568e4425096e7daeffa631080f285c03ac84544d93b02627b4bd15e045c', 'ogcore/__init__.py': '19819cda2e8a3a3609c021729d469a5597e1e3d61a50871daa693248497757f4', 'ogcore/safeio.py': '3cd313c10bba613815d0ad1496d95a6c5658210503cb69eb88cebf8ecbd6230d', 'ogcore/userdata.py': 'bb773050349d1e16f7a436be9b8cde1f980a396ad5153166af49cc9ca3537949', 'tests/test_licensing.py': '4065e7a59ee0eeaebe0e6a8d4306417e981742cd11b470c4f59a062c6664f4e5', 'tests/test_v0957_fixes.py': '35d8d849fe58513dc4f7a21cb4678329d7567ea56f6591013b61bf3639ed669f', 'tests/test_v0958_fixes.py': '7ff101d09caa5d79bdbc322f54f5e3e94ac0ddfd9d9bfc61cbdc0b9cbb5c4ea3'}
if not __debug__:raise SystemExit('Run without Python optimization (-O/PYTHONOPTIMIZE).')
BEFORE=datetime(2027,2,1,tzinfo=timezone.utc);AFTER=datetime(2027,3,15,tzinfo=timezone.utc)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bootstrap(checkout,package,out):
 for name,digest in SOURCE_HASHES.items():
  actual=hashlib.sha256((checkout/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
  if actual!=digest:raise RuntimeError('Source differs from verified 104bf4f: '+name)
 sys.path.insert(0,str(checkout));import ogcore
 ogcore.__path__.insert(0,str(package/'_internal/ogcore'))
 from ogcore import licensing,license_runtime
 from importlib.machinery import ExtensionFileLoader
 origins={}
 for stem,m in [('licensing',licensing),('license_runtime',license_runtime)]:
  p=Path(m.__file__).resolve()
  assert isinstance(m.__loader__,ExtensionFileLoader),f'Source fallback refused: {p}'
  assert p.parent==(package/'_internal/ogcore').resolve(),f'Wrong extension: {p}'
  assert sha(p)==EXPECTED[stem],f'Unexpected package hash: {p}'
  origins[stem]={'path':str(p),'sha256':sha(p),'loader':type(m.__loader__).__name__}
 (out/f'origins-{os.getpid()}.json').write_text(json.dumps({'pid':os.getpid(),'python':sys.version,'modules':origins},indent=2))
 return licensing,license_runtime
p=argparse.ArgumentParser();p.add_argument('--checkout',required=True);p.add_argument('--package',required=True);p.add_argument('--out',required=True);p.add_argument('--role',default='parent',choices=['parent','check','remember','hold']);p.add_argument('--state');p.add_argument('--license');p.add_argument('--keys');p.add_argument('--ready');p.add_argument('--release');p.add_argument('--index',type=int,default=0);p.add_argument('--skip-pytest',action='store_true');a=p.parse_args()
C=Path(a.checkout).resolve();D=Path(a.package).resolve();O=Path(a.out).resolve()
if O.is_relative_to(C) or O.is_relative_to(D):raise SystemExit('Output must be outside the checkout and package.')
O.mkdir(parents=True,exist_ok=True)
if sys.platform!='win32':raise SystemExit('Native Windows required; this helper will not claim a Linux/emulation pass.')
if sys.version_info[:2]!=(3,12):raise SystemExit('Use py -3.12: the pinned package extensions are cp312-win_amd64.')
EXPECTED={stem:sha(D/'_internal/ogcore'/f'{stem}.cp312-win_amd64.pyd') for stem in ['licensing','license_runtime']}
L,LR=bootstrap(C,D,O)
assert L.STATE_LOCK_TIMEOUT==10.0 and hasattr(L,'LicenseStateBusy'),'Missing v0.9.58 lock fix'
(O/'package-licensing-hashes.json').write_text(json.dumps({'independently_pinned_to_uploaded_zip':False,'recorded_on_windows_host':EXPECTED},indent=2))
def clock(path):return L.ClockState(path,L.DpapiProtector())
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
result={'classification':'Windows compiled-extension tests; customer EXE not executed; extension hashes recorded locally, uploaded ZIP not independently inspected','package':str(D),'checkout':str(C),'host_clock_changed':False,'source_or_package_modified':False,'cases':{}}
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
  assert b'"expired"'not in state.read_bytes()
  result['cases']['DPAPI_restart_reimport_renewal_original_denied']='passed'
  state=T/'concurrent.bin';assert check(state,data,keys,BEFORE).ok;workers=[child('remember',state,'--index',str(i))for i in range(4)];e=check(state,data,keys,AFTER)
  for w in workers:
   stdout,stderr=w.communicate(timeout=120);assert w.returncode==0,stderr
  assert e.status==L.Status.EXPIRED and check(state,data,keys,BEFORE).status==L.Status.EXPIRED
  result['cases']['DPAPI_concurrent_processes']='passed'
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
  result['cases']['DPAPI_real_lock_timeout']=case
  assert e.status==L.Status.EXPIRED and wait>=10 and present and after_holder,case
  assert restart_status==replay.status.value==reimport.status.value==old_after_renewal=='expired',case
  assert renewal_install.ok and renewed_status=='valid',case
  if not a.skip_pytest:
   # Preload the exact package PYDs in pytest and its restarted/concurrent Python children.
   boot=T/'bootstrap';boot.mkdir();site="""import os,sys,json,hashlib\nfrom pathlib import Path\ntry:\n C=Path(os.environ['B56_AUDIT_CHECKOUT']);D=Path(os.environ['B56_AUDIT_PACKAGE']);O=Path(os.environ['B56_AUDIT_OUTPUT'])\n sys.path.insert(0,str(C))\n import ogcore\n ogcore.__path__.insert(0,str(D/'_internal/ogcore'))\n from ogcore import licensing,license_runtime\n from importlib.machinery import ExtensionFileLoader\n expected=json.loads(os.environ['B56_AUDIT_HASHES']);origins={}\n for name,module in [('licensing',licensing),('license_runtime',license_runtime)]:\n  path=Path(module.__file__).resolve()\n  assert isinstance(module.__loader__,ExtensionFileLoader) and path.parent==(D/'_internal/ogcore').resolve(),str(path)\n  digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==expected[name],str(path)\n  origins[name]={'path':str(path),'sha256':digest}\n (O/('pytest-origins-'+str(os.getpid())+'.json')).write_text(json.dumps(origins,indent=2))\nexcept BaseException:\n import traceback\n traceback.print_exc();os._exit(91)\n"""
   (boot/'sitecustomize.py').write_text(site);env=os.environ.copy();env.update(PYTHONPATH=str(boot),B56_AUDIT_CHECKOUT=str(C),B56_AUDIT_PACKAGE=str(D),B56_AUDIT_OUTPUT=str(O),B56_AUDIT_HASHES=json.dumps(EXPECTED))
   command=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(C/'tests/test_licensing.py'),str(C/'tests/test_v0957_fixes.py'),str(C/'tests/test_v0958_fixes.py'),'-k','not test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository','--junitxml='+str(O/'windows-compiled-results.xml')]
   with (O/'windows-compiled-tests.log').open('w')as log:done=subprocess.run(command,cwd=C,env=env,stdout=log,stderr=subprocess.STDOUT)
   result['pytest_command']=command;result['pytest_exit_code']=done.returncode
   lines=(O/'windows-compiled-tests.log').read_text(errors='replace').splitlines()
   result['pytest_summary']=[line for line in lines if ' passed' in line and ' in ' in line][-1:] 
  result['verdict_for_timeout_probe']='still reproducible'if result['cases']['DPAPI_real_lock_timeout']['reproduced']else'held-lock regression passed'
except BaseException as exc:
 result['error']=repr(exc);result['traceback']=traceback.format_exc()
finally:
 (O/'windows-B56-W05-summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
raise SystemExit(1 if result.get('error')or result.get('pytest_exit_code',0)!=0 or result.get('cases',{}).get('DPAPI_real_lock_timeout',{}).get('reproduced')else 0)
