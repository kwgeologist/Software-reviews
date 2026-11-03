import sys,time,json,resource
from pathlib import Path
import tkinter as tk
import numpy as np
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from ogmap.view import MapView
root=tk.Tk();root.geometry('1400x900');view=MapView(root);view.pack(fill='both',expand=True);root.update()
rng=np.random.default_rng(83);xy=rng.uniform(0,100000,(112000,2));wells=[{'id':i+1,'x':float(x),'y':float(y),'code':('OIL','GAS','DRY')[i%3],'label':''}for i,(x,y)in enumerate(xy)]
t=time.perf_counter();view.set_wells(wells);root.update();load=time.perf_counter()-t
view.ax.set_xlim(0,100000);view.ax.set_ylim(0,100000);t=time.perf_counter();view.refresh_wells();root.update();basin=time.perf_counter()-t
counts=[];times=[]
for i in range(6):
 view.ax.set_xlim(i*5000,i*5000+10000);view.ax.set_ylim(0,10000);t=time.perf_counter();view.refresh_wells();root.update();times.append(time.perf_counter()-t);counts.append((len(view.ax.lines),len(view.ax.collections),len(view.ax.texts)))
out={'wells':len(wells),'set_wells_seconds':load,'basin_refresh_seconds':basin,'zoom_refresh_seconds':times,'artist_counts_over_pans':counts,'peak_process_rss_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'limitations':'Synthetic well markers only; no 200-layer composite, LIC/LAS load, production or SEG-Y stress.'};root.destroy();Path('/workspace/audit-v0.8.58/scale-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
