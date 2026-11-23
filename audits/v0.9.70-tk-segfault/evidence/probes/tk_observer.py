"""External read-only pytest observer. Does not replace cleanup, force GC, or suppress errors."""
import os,sys,json,time,gc,threading,weakref,resource,faulthandler
from pathlib import Path
import tkinter as tk
import _tkinter
OUT=Path(os.environ['TK_AUDIT_OBSERVATIONS']);ROOTS={};COUNTS={'made':0,'destroy':0,'gc':0,'cross_thread_tk_calls':0};MAIN=threading.get_ident()
F=OUT.open('a',buffering=1)
def emit(o):F.write(json.dumps(o,default=str)+'\n');F.flush()
def snapshot(label):
 rows=[]
 for key,ref in list(ROOTS.items()):
  root=ref()
  if root is None:continue
  r={'id':key}
  try:
   r['exists']=bool(root.winfo_exists());jobs=root.tk.call('after','info');r['pending']=list(jobs);r['commands']=len(root.tk.splitlist(root.tk.call('info','commands')))
   if jobs:r['pending_scripts']=[str(root.tk.call('after','info',j))[:250]for j in jobs[:8]]
  except Exception as e:r['query_error']=str(e)
  rows.append(r)
 mpl=sys.modules.get('matplotlib._pylab_helpers');managers=len(mpl.Gcf.get_all_fig_managers())if mpl else 0
 # Query GC objects without retaining the list between snapshots.
 objects=gc.get_objects();figures=sum(type(o).__module__=='matplotlib.figure'and type(o).__name__=='Figure'for o in objects);widgets=sum(isinstance(o,tk.Misc)for o in objects);del objects
 emit({'event':label,'time':time.time(),'roots':rows,'counts':dict(COUNTS),'GC':gc.get_count(),'gc_enabled':gc.isenabled(),'mpl_managers':managers,'retained_figures':figures,'retained_tk_widgets':widgets,'rss_max_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'threads':[t.name for t in threading.enumerate()]})
orig_init,orig_destroy=tk.Tk.__init__,tk.Tk.destroy
def init(self,*a,**k):
 orig_init(self,*a,**k);COUNTS['made']+=1;ROOTS[id(self)]=weakref.ref(self)
def destroy(self,*a,**k):
 COUNTS['destroy']+=1;return orig_destroy(self,*a,**k)
tk.Tk.__init__,tk.Tk.destroy=init,destroy
# Tk bridge methods call tkapp.call, so profile their Python entry without touching native calls.
def profile(frame,event,arg):
 if event=='call'and threading.get_ident()!=MAIN and frame.f_code.co_filename.endswith('/tkinter/__init__.py'):
  COUNTS['cross_thread_tk_calls']+=1
  if COUNTS['cross_thread_tk_calls']<20:emit({'event':'cross_thread_tk_python_entry','function':frame.f_code.co_name,'thread':threading.current_thread().name})
 return profile
if os.environ.get('TK_AUDIT_THREAD_PROFILE')=='1':threading.setprofile(profile)
def gc_event(phase,info):
 if phase=='start':COUNTS['gc']+=1
 if threading.get_ident()!=MAIN:emit({'event':'gc_on_worker','phase':phase,'thread':threading.current_thread().name,'info':info})
gc.callbacks.append(gc_event)
faulthandler.enable(all_threads=True)
emit({'event':'runtime','python':sys.version,'tk_extension':_tkinter.__file__,'TkVersion':tk.TkVersion,'TclVersion':tk.TclVersion,'pid':os.getpid(),'observer':True})
def pytest_runtest_logstart(nodeid,location):snapshot('start '+nodeid)
def pytest_runtest_logfinish(nodeid,location):snapshot('finish '+nodeid)
def pytest_sessionfinish(session,exitstatus):snapshot('sessionfinish '+str(exitstatus))
