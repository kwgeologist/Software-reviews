import os,sys,json,tempfile,copy
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path.insert(0,str(R))
from ogcore import symbol_catalog as C
from geoworkbench.symbol_catalog_dialog import SymbolCatalogDialog
import well_symbols as W
out={}
with tempfile.TemporaryDirectory()as t:
 os.environ['OGW_SYMBOL_CATALOG']=str(Path(t)/'cat.json');C.install(C.builtin());root=tk.Tk();root.withdraw();d=SymbolCatalogDialog(root);root.update();before=[vars(m).copy()for m in d.work.mappings];d.load_form('OIL');d.v['code'].set('BAD CODE')
 with patch('geoworkbench.symbol_catalog_dialog.messagebox.showerror'):accepted=d.apply_form()
 after=[vars(m).copy()for m in d.work.mappings];out['rejected_rename']={'accepted':accepted,'oil_entry_restored':d.work.entry('OIL') is not None,'mapping_changes':[{'before':a,'after':b}for a,b in zip(before,after)if a!=b],'catalog_errors':d.work.validate()};d.cancel();root.destroy()
 # Save button following a live-preview field edit without Apply.
 root=tk.Tk();root.withdraw();d=SymbolCatalogDialog(root);d.load_form('GAS');old=d.work.entry('GAS').description;d.v['description'].set('Edited in form');saved=d.save();out['save_without_apply']={'saved':saved,'typed':'Edited in form','reloaded':C.load().entry('GAS').description,'before':old};root.destroy()
C.install(C.builtin());(R.parent/'editor-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
