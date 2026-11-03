import sys,json,tkinter as tk
from pathlib import Path
from tkinter import font
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from ogcore import text_style as S
r=tk.Tk();f=S.tk_font(r,S.TextStyle(font='DejaVu Serif',size=9,bold=True));out={'requested':f.configure(),'actual':f.actual(),'tk_dejavu_available':any('DejaVu Serif'==x for x in font.families(r)),'tk_family_count':len(font.families(r))};r.destroy()
r=tk.Tk();f2=S.tk_font(r,S.TextStyle(font='DejaVu Serif',size=9,bold=True));out['recreated_root_returns_old_font']=f2 is f
try:out['recreated_root_actual']=f2.actual()
except Exception as e:out['recreated_root_error']=str(e)
r.destroy();Path('/workspace/audit-v0.8.58/font-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
