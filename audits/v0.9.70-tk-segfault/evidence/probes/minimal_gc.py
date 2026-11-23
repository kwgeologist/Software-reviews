"""Controlled native-finalization experiment, not a claim of the original SIGSEGV trigger."""
import tkinter as tk,threading,gc,sys,json,faulthandler,resource,_tkinter
faulthandler.enable(all_threads=True)
gc.disable();r=tk.Tk();r.withdraw();r.cycle=r;metadata={'python':sys.version,'extension':_tkinter.__file__,'Tcl_patch':r.tk.call('info','patchlevel'),'Tk_patch':r.tk.call('package','provide','Tk')};r.destroy();metadata['pending_after_destroy']=list(r.tk.call('after','info'));del r;objects=gc.get_objects();metadata.update(roots_in_gc=sum(isinstance(o,tk.Tk)for o in objects),figures_in_gc=sum(type(o).__module__=='matplotlib.figure'and type(o).__name__=='Figure'for o in objects),rss_max_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,gc_count=gc.get_count());del objects
print(json.dumps({'tk':tk.TkVersion,'mode':sys.argv[1],'controlled_cycle':True,'automatic_gc_disabled':True,**metadata}),flush=True)
if sys.argv[1]=='auto-worker':
 def allocate():
  gc.enable()
  junk=[[]for _ in range(5000)]
 t=threading.Thread(target=allocate,name='controlled-automatic-worker-gc');t.start();t.join()
elif sys.argv[1]=='worker':
 t=threading.Thread(target=lambda:gc.collect(),name='controlled-worker-gc');t.start();t.join()
else:gc.collect()
print('completed',flush=True)
