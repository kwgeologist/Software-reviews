"""Standalone multiple-root/canvas event-finalization stress; no Workbench imports."""
import sys,gc,json,resource,faulthandler
import tkinter as tk
from tkinter import ttk,font
faulthandler.enable(all_threads=True)
mode=sys.argv[1];count=int(sys.argv[2]);out=open(sys.argv[3],'w',buffering=1)
if mode!='tk-only':
 from matplotlib.figure import Figure
 from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
for k in range(count):
 r=tk.Tk();r.withdraw();top=tk.Toplevel(r);f=font.Font(root=r,family='sans',size=10);ttk.Label(top,text='synthetic',font=f).pack()
 if mode!='tk-only':
  fig=Figure(figsize=(2,1));a=fig.add_subplot();a.plot([0,1],[1,0]);canvas=FigureCanvasTkAgg(fig,master=top);canvas.get_tk_widget().pack();canvas.draw_idle()
 r.after_idle(gc.collect);r.update();pending=list(r.tk.call('after','info'));top.destroy();r.destroy()
 if mode!='tk-only':del canvas,fig,a
 del top,r,f
 if k%10==0:gc.collect()
 if k%20==0:out.write(json.dumps({'iteration':k+1,'mode':mode,'pending_before_close':pending,'rss_max_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'gc':gc.get_count()})+'\n')
out.write(json.dumps({'complete':True,'cycles':count,'mode':mode})+'\n');out.close()
