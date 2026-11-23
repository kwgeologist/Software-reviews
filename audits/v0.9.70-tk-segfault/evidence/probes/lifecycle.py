from pathlib import Path
import os,sys,json,gc,weakref,resource,time,threading,faulthandler
B=Path('/workspace/audit-v0.9.70-tk-segfault');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')]
import conftest
import tkinter as tk,_tkinter
from test_xsection import WindowTests
from xsection.window import CrossSectionWindow
from matplotlib.figure import Figure
faulthandler.enable(all_threads=True)
mode=sys.argv[1];iterations=int(sys.argv[2]);out=Path(sys.argv[3]);out.parent.mkdir(exist_ok=True,parents=True);log=out.open('w',buffering=1);refs=[];errors=[];case=WindowTests();case.setUp();case.root.report_callback_exception=lambda *e:errors.append(str(e))
def emit(k,root=None):
 objs=gc.get_objects();r={'iteration':k,'mode':mode,'roots_in_gc':sum(isinstance(o,tk.Tk)for o in objs),'widgets_in_gc':sum(isinstance(o,tk.Misc)for o in objs),'figures_in_gc':sum(isinstance(o,Figure)for o in objs),'retained_closed_sections':sum(w()is not None for w in refs),'after':list(case.root.tk.call('after','info')),'commands':len(case.root.tk.splitlist(case.root.tk.call('info','commands'))),'gc':gc.get_count(),'rss_max_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'callback_errors':list(errors)};del objs;log.write(json.dumps(r,default=str)+'\n');log.flush()
log.write(json.dumps({'runtime':sys.version,'tk':case.root.tk.call('info','patchlevel'),'tk_pkg':case.root.tk.call('package','provide','Tk'),'extension':_tkinter.__file__,'mode':mode})+'\n');emit(0)
try:
 for k in range(iterations):
  w=case.window();refs.append(weakref.ref(w))
  if mode=='normal':w.close()
  else:w.destroy()
  del w
  case.root.update()
  if k%20==19:emit(k+1)
 # Measure natural retention first; controlled GC is separate evidence, after the requested cycles.
 emit(iterations);collected=gc.collect();case.root.update();emit('after_main_thread_gc')
 log.write(json.dumps({'collected_after_cycles':collected,'complete':True})+'\n')
finally:case.tearDown();log.close()
