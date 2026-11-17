from pathlib import Path
import sys,tempfile,json,tkinter as tk
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path.insert(0,str(R))
from database import ProjectDatabase
from bulk_import import BulkWorkbookImporter
from openpyxl import Workbook
from geoworkbench.interpretation_dialogs import TopDefinitionsDialog
out={}
with tempfile.TemporaryDirectory() as td:
 p=Path(td);db=ProjectDatabase(p/'p.ogwdb');w=db.add_well('W','0512300001');book=Workbook();sheet=book.active;sheet.title='Tops';sheet.append(['API','Formation','MD','Source']);sheet.append(['0512300001','A',100,'Acme Energy']);sheet.append(['0512300001','B',1000,'Acme  Energy']);f=p/'tops.xlsx';book.save(f);book.close();report=BulkWorkbookImporter(db,f).import_all()
 out['import_errors']=report.errors;out['stored_sources']=[dict(r) for r in db.rows('SELECT formation,source FROM formation_tops')];out['enumerated_sources']=db.top_pick_sources();out['rename_displayed_source_count']=db.rename_top_pick_source('ACME ENERGY','Renamed');out['sources_after_rename']=[dict(r) for r in db.rows('SELECT formation,source FROM formation_tops')]
 # Recreate the normalized-name collision through the same supported source rename.
 db.rename_top_pick_source('RENAMED','ACME ENERGY');root=tk.Tk();root.withdraw();root.db=db;root.refresh_tabs=lambda:None;manager=TopDefinitionsDialog(root)
 try:dialog=manager.manage_sources();out['manager_open_error']=None;dialog.destroy()
 except Exception as e:out['manager_open_error']=type(e).__name__+': '+str(e)
 manager.destroy();root.destroy();db.close()
(B/'source-spacing-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
