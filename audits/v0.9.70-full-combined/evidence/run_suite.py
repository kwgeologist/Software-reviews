from pathlib import Path
import os,json,sys,subprocess,time,xml.etree.ElementTree as ET,collections
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');P='/workspace/audit-v0.9.56-windows/tooling/bin/python';X='/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb'
weights=collections.defaultdict(float)
for case in ET.parse('/workspace/audit-v0.9.68-full/full-results.xml').iter('testcase'):
 n=case.get('classname','').split('.')
 if len(n)>1:weights[n[1]]+=float(case.get('time','0'))
files=sorted(C.joinpath('tests').rglob('test_*.py'));groups=[[]for _ in range(4)];loads=[0.]*4
for p in sorted(files,key=lambda p:weights.get(p.stem,5.),reverse=True):
 idx=min(range(4),key=loads.__getitem__);groups[idx].append(str(p.relative_to(C)));loads[idx]+=weights.get(p.stem,5.)
assert sorted(sum(groups,[]))==sorted(str(p.relative_to(C))for p in files)
(B/'suite-plan.json').write_text(json.dumps({'baseline':'1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa','module_count':len(files),'groups':groups,'estimated_seconds':loads,'note':'All shipped test_*.py modules, four independent processes/displays; not a serial-run qualification.'},indent=2))
xs=[];ps=[];handles=[];runs=[]
try:
 for idx,group in enumerate(groups):
  root=B/f'group-{idx+1}';root.mkdir(exist_ok=True);env=os.environ.copy();env.update(DISPLAY=f':{201+idx}',PYTHONPATH='/workspace/audit-v0.9.68-full/deps',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',XDG_CACHE_HOME=str(root/'xdg-cache'),MPLCONFIGDIR=str(root/'mpl'))
  h=(root/'xvfb.log').open('w');handles.append(h);xs.append(subprocess.Popen([X,env['DISPLAY'],'-screen','0','1600x1000x24','-nolisten','tcp'],stdout=h,stderr=subprocess.STDOUT))
  time.sleep(.2)
  cmd=[P,'-X','faulthandler','-m','pytest','-q','-p','no:cacheprovider',*group,'--tb=short','-rs',f'--junitxml={root}/results.xml']
  h=(root/'pytest.log').open('w');handles.append(h);ps.append(subprocess.Popen(cmd,cwd=C,env=env,stdout=h,stderr=subprocess.STDOUT));runs.append({'group':idx+1,'pid':ps[-1].pid,'command':cmd,'start':time.time(),'display':env['DISPLAY']})
 (B/'suite-commands.json').write_text(json.dumps(runs,indent=2));print(json.dumps({'started':4,'modules':len(files),'prior_weight_seconds':loads}),flush=True)
 while any(p.poll()is None for p in ps):
  for r,p in zip(runs,ps):r['exit_code']=p.poll()
  (B/'suite-status.json').write_text(json.dumps(runs,indent=2));time.sleep(5)
 for r,p in zip(runs,ps):r['exit_code']=p.wait();r['end']=time.time()
 (B/'suite-status.json').write_text(json.dumps(runs,indent=2));print(json.dumps({'exit_codes':[p.returncode for p in ps]}),flush=True)
finally:
 for p in xs:p.terminate()
 for p in xs:p.wait()
 for h in handles:h.close()
