from pathlib import Path
import sys,tempfile,json
B=Path('/workspace/audit-v0.9.52');R=B/'OandG_Workbench_v0.9.52';sys.path.insert(0,str(R))
from database import ProjectDatabase
out={}
with tempfile.TemporaryDirectory() as td:
 path=Path(td)/'p.ogwdb';d=ProjectDatabase(path);w=d.add_well('Well','42401123450001');a=d.top_definition('A')[0];b=d.top_definition('B')[0];d.set_formation_top(w,'A',100,source='X');d.set_formation_top(w,'B',1000,source='X');d.add_top_alias(b,'B old')
 out['before_alias_rename']={'alias':d.canonical_top_name('B old'),'picks':[dict(r) for r in d.rows('SELECT formation,measured_depth FROM formation_tops')]}
 d.rename_top_definition(a,'B old')
 out['after_alias_rename']={'alias':d.canonical_top_name('B old'),'definitions':d.formation_names(),'picks':[dict(r) for r in d.rows('SELECT formation,measured_depth FROM formation_tops')]}
 d.close()
with tempfile.TemporaryDirectory() as td:
 path=Path(td)/'p.ogwdb';d=ProjectDatabase(path);a=d.top_definition('A')[0];b=d.top_definition('B')[0];d.add_top_alias(a,'Legacy');out['alias_before_reassignment']=d.canonical_top_name('Legacy');d.add_top_alias(b,'Legacy');out['alias_after_reassignment']=d.canonical_top_name('Legacy');d.close()
with tempfile.TemporaryDirectory() as td:
 path=Path(td)/'p.ogwdb';d=ProjectDatabase(path);a=d.top_definition('Corr-only')[0];d.set_project_value('correlation:tops',json.dumps([{'name':'Corr-only','added':True,'shown':True}]));d.delete_top_definition(a);out['after_delete']=d.formation_names();d.close();d=ProjectDatabase(path);out['after_reopen']=d.formation_names();d.close()
(B/'top-identity-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
