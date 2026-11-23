from pathlib import Path
import os,json,time,subprocess
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';R=B/'full-serial';R.mkdir(exist_ok=True);P='/workspace/audit-v0.9.56-windows/tooling/bin/python';T=Path('/workspace/audit-v0.9.70-tk-segfault');e=os.environ.copy();e.update(DISPLAY=':241',PYTHONPATH=str(T/'tk86-extension')+':/workspace/audit-v0.9.68-full/deps',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',MPLCONFIGDIR=str(R/'mpl'),XDG_CACHE_HOME=str(R/'cache'),LD_LIBRARY_PATH=str(T/'native/root/usr/lib/x86_64-linux-gnu'))
x=subprocess.Popen(['/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb',e['DISPLAY'],'-screen','0','1600x1000x24','-nolisten','tcp'],stdout=(R/'xvfb.log').open('w'),stderr=subprocess.STDOUT);time.sleep(.3)
cmd=[str(T/'native/root/usr/bin/gdb'),'--batch','-ex','set pagination off','-ex','set debuginfod enabled off','-ex','set print thread-events off','-ex','run','-ex','thread apply all bt 60','-ex','info sharedlibrary','--args',P,'-X','faulthandler','-m','pytest','-v','-p','no:cacheprovider','tests','--tb=short','-rs',f'--junitxml={R}/results.xml']
r={'command':cmd,'cwd':str(C),'start':time.time(),'environment':{k:e[k]for k in ['DISPLAY','PYTHONPATH','PYTHONDONTWRITEBYTECODE','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MPLCONFIGDIR','XDG_CACHE_HOME']},'native_debugger':True,'peak_inferior_RSS_KiB':0};(R/'command.json').write_text(json.dumps(r,indent=2));p=subprocess.Popen(cmd,cwd=C,env=e,stdout=(R/'pytest-native.log').open('w'),stderr=subprocess.STDOUT)
try:
 while p.poll()is None:
  children=[]
  try:
   ids=Path(f'/proc/{p.pid}/task/{p.pid}/children').read_text().split()
   for pid in ids:
    lines=Path(f'/proc/{pid}/status').read_text().splitlines();rss=next((int(l.split()[1])for l in lines if l.startswith('VmRSS:')),0);r['peak_inferior_RSS_KiB']=max(r['peak_inferior_RSS_KiB'],rss);children.append({'pid':int(pid),'rss_KiB':rss})
  except (FileNotFoundError,PermissionError):pass
  r.update(elapsed_seconds=time.time()-r['start'],inferior=children,gdb_pid=p.pid);(R/'status.json').write_text(json.dumps(r,indent=2));time.sleep(5)
 r.update(gdb_exit_code=p.returncode,seconds=time.time()-r['start'],finished=True);(R/'status.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
finally:x.terminate();x.wait()
