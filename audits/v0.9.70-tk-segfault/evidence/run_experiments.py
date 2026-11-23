from pathlib import Path
import os,sys,subprocess,time,json,resource
B=Path('/workspace/audit-v0.9.70-tk-segfault');C=Path('/workspace/audit-v0.9.70-integrity/checkout');P='/workspace/audit-v0.9.56-windows/tooling/bin/python';X='/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb';G=str(B/'native/root/usr/bin/gdb')
def env(version,display,root):
 e=os.environ.copy();e.update(DISPLAY=f':{display}',PYTHONPATH=(':'.join(([str(B/'tk86-extension')]if version=='86'else[])+['/workspace/audit-v0.9.68-full/deps',str(B/'probes')])),PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MPLCONFIGDIR=str(root/'mpl'),XDG_CACHE_HOME=str(root/'cache'),TK_AUDIT_OBSERVATIONS=str(root/'observations.jsonl'),TK_AUDIT_THREAD_PROFILE='1');return e

def run(name,version,targets,display,observer=True,native=False,timeout=900):
 r=B/'runs'/name;r.mkdir(exist_ok=True);e=env(version,display,r);x=subprocess.Popen([X,e['DISPLAY'],'-screen','0','1600x1000x24','-nolisten','tcp'],stdout=(r/'xvfb.log').open('w'),stderr=subprocess.STDOUT);time.sleep(.2)
 cmd=[P,'-X','faulthandler','-m','pytest','-q','-p','no:cacheprovider']+(['-p','tk_observer']if observer else[])+targets+['--tb=short','-rs',f'--junitxml={r}/results.xml']
 if native:
  e['LD_LIBRARY_PATH']=str(B/'native/root/usr/lib/x86_64-linux-gnu')
  cmd=[G,'--batch','-ex','set pagination off','-ex','set debuginfod enabled off','-ex','set print thread-events off','-ex','run','-ex','thread apply all bt 35','-ex','info sharedlibrary','--args']+cmd
 out={'name':name,'Tk_requested':version,'command':cmd,'observer':observer,'native':native,'start':time.time()};(r/'command.json').write_text(json.dumps(out,indent=2))
 try:
  with (r/'run.log').open('w')as h:
   p=subprocess.Popen(cmd,cwd=C,env=e,stdout=h,stderr=subprocess.STDOUT);maxrss=0
   while p.poll()is None:
    try:
     text=Path(f'/proc/{p.pid}/status').read_text();rss=[line for line in text.splitlines()if line.startswith('VmRSS:')];maxrss=max(maxrss,int(rss[0].split()[1]))if rss else maxrss
    except (FileNotFoundError,PermissionError):pass
    if time.time()-out['start']>timeout:p.terminate();out['timed_out']=True;break
    time.sleep(.2)
   try:code=p.wait(timeout=8)
   except subprocess.TimeoutExpired:p.kill();code=p.wait()
  out.update(exit_code=code,seconds=time.time()-out['start'],parent_peak_RSS_KiB=maxrss)
 finally:x.terminate();x.wait()
 (r/'status.json').write_text(json.dumps(out,indent=2));print(name,code,flush=True);return out
if __name__=='__main__':
 import concurrent.futures
 def branch(v,disp):
  runs=[]
  # A: three fresh whole Cross Section files, first uninstrumented, then observed.
  for k in range(3):runs.append(run(f'A-{v}-{k+1}',v,['tests/test_xsection.py'],disp,observer=k>0))
  # D: same target test after distinct GUI modules in ONE process.
  target=['tests/test_xsection.py::PunchListWindowTests::test_settings_hold_from_one_session_to_the_next','tests/test_xsection.py::GeoCrossSectionTests::test_wells_chosen_on_the_map_open_a_section']
  for prefix,files in [('first',[]),('after-seismic',['tests/test_seismic_app.py']),('after-map',['tests/test_map_drawing_objects.py','tests/test_scrolling_map.py']),('after-correlation',['tests/test_correlation.py'])]:
   runs.append(run(f'D-{v}-{prefix}',v,files+target,disp))
  # C: long ordered GUI sequence, ending with a complete Cross Section module.
  seq=['tests/test_geo_tabs.py','tests/test_map_drawing_objects.py','tests/test_petro_integration.py','tests/test_digitize_ui.py','tests/test_geosteering_project.py','tests/test_seismic_app.py','tests/test_correlation.py','tests/test_xsection.py']
  runs.append(run(f'C-{v}-serial-GUI',v,seq,disp,timeout=1800))
  return runs
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
  out=list(pool.map(lambda args:branch(*args),[('86',221),('9',222)]))
 (B/'experiment-summary.json').write_text(json.dumps(out,indent=2))
