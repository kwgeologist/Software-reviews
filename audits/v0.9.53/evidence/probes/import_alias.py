import sys,json,tempfile
from pathlib import Path
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path.insert(0,str(R))
from database import ProjectDatabase
from bulk_import import BulkWorkbookImporter
from mapped_import import MappedTableImporter
from openpyxl import Workbook
out={}
with tempfile.TemporaryDirectory() as td:
 for kind in ['bulk','mapped']:
  db=ProjectDatabase(Path(td)/(kind+'.ogwdb'));w=db.add_well('Well A','0512300001');db.set_formation_top(w,'Canonical',100,source='XON');db.add_top_alias(db.top_definition('Canonical')[0],'Legacy')
  if kind=='bulk':
   book=Workbook();sheet=book.active;sheet.title='Tops';sheet.append(['API','Formation','MD','Source']);sheet.append(['0512300001','Legacy',100,'XON']);p=Path(td)/'tops.xlsx';book.save(p);book.close();f=lambda:BulkWorkbookImporter(db,p).import_all()
  else:
   p=Path(td)/'tops.csv';p.write_text('API,Formation,MD,Source\n0512300001,Legacy,100,XON\n');f=lambda:MappedTableImporter(db,p,{'API':'API/UWI','Formation':'Formation','MD':'Formation Top MD','Source':'Formation Top Source'}).import_all()
  runs=[]
  for i in range(2):
   try:
    report=f();runs.append({'errors':report.errors,'rows':[dict(r) for r in db.rows('SELECT id,well_id,definition_id,formation,measured_depth,source FROM formation_tops')]})
   except Exception as e:runs.append({'exception':repr(e)})
  out[kind]=runs;db.close()
(B/'import-alias-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
