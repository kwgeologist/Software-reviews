import os,sys,json,tempfile,tkinter as tk
from pathlib import Path
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path.insert(0,str(R))
from ogcore import symbol_catalog as C
from ogmap.view import MapView
from ogmap.symbols import marker_paths
from matplotlib.colors import to_hex
C.install(C.builtin());root=tk.Tk();root.geometry('900x700');v=MapView(root);v.pack(fill='both',expand=True);root.update();wells=[{'id':1,'x':0.,'y':0.,'code':'OIL','label':''}];v.set_wells(wells);root.update()
def cols():
 return sorted({to_hex(c)for a in v._symbol_artists for c in list(a.get_facecolors())+list(a.get_edgecolors())if c[3]>0})
before=cols();cat=C.builtin();cat.entry('OIL').color='#123456';C.install(cat);root.update();v.refresh_wells();root.update();after=cols();v.set_wells(wells);root.update();rebuilt=cols();root.destroy();C.install(C.builtin());out={'before':before,'after_catalog_install_and_refresh':after,'new_marker_definition':'#123456','after_set_wells_rebuild':rebuilt};(R.parent/'map-style-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
