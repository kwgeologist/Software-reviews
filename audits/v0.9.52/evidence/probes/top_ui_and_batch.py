from pathlib import Path
import sys,tempfile,json,tkinter as tk
from unittest.mock import patch
B=Path('/workspace/audit-v0.9.52');R=B/'OandG_Workbench_v0.9.52';sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from geoworkbench.interpretation_dialogs import TopDefinitionsDialog
from ogmap import sources
out={}
with tempfile.TemporaryDirectory() as td:
 path=Path(td)/'p.ogwdb';db=ProjectDatabase(path);db.set_project_value('coordinate_system','EPSG:2231');w=db.add_well('W','05-123-00001');db.execute('INSERT INTO locations(well_id,surface_x,surface_y) VALUES(?,?,?)',(w,3000000,4800000));db.set_formation_top(w,'A',100,source='X');db.set_formation_top(w,'B',1000,source='X');a=db.top_definition('A')[0];b=db.top_definition('B')[0];db.add_top_alias(b,'B old')
 def values():return sources.collect(db,{'kind':'top','formation':'B old','measure':'MD'},unit='ft').value.tolist()
 root=tk.Tk();root.withdraw();root.db=db;root.refresh_tabs=lambda:None;dlg=TopDefinitionsDialog(root);dlg.tree.selection_set(str(a));root.update();before=values()
 with patch('geoworkbench.interpretation_dialogs.simpledialog.askstring',return_value='B old'),patch('geoworkbench.interpretation_dialogs.messagebox.askyesno',return_value=False) as confirm:
  dlg.rename()
 out['normal_global_manager_rename']={'map_MD_before':before,'map_MD_after':values(),'merge_confirmation_calls':confirm.call_count,'definitions':db.formation_names(),'alias_owner':db.canonical_top_name('B old')}
 dlg.destroy();db.top_definition('Corr-only');db.set_project_value('correlation:tops',json.dumps([{'name':'Corr-only','added':True,'shown':True}]));dlg=TopDefinitionsDialog(root);identifier=db.top_definition('Corr-only')[0];dlg.tree.selection_set(str(identifier))
 with patch('geoworkbench.interpretation_dialogs.messagebox.askyesno',return_value=True):dlg.delete()
 out['normal_manager_delete']={'before_close':db.formation_names()};dlg.destroy();root.destroy();db.close();db=ProjectDatabase(path);out['normal_manager_delete']['after_reopen']=db.formation_names();db.close()
from test_batch_zones import Project
from ogcore import batch_zones as bz,batch_ui
with tempfile.TemporaryDirectory() as td:
 p=Project(Path(td));d=p.definition();bz.save_definition(p.db,d);wid=p.wells['A-1'];root=tk.Tk();root.withdraw();dialog=batch_ui.BatchCalculationsDialog(root,p.db,current_well_id=wid,tab=1);dialog.zones.show_definition(d)
 def calculate(definition):
  try:return {'values':bz.calculate_well(p.db,definition,wid,p.db.formation_tops_for([wid])[wid],'XON',bz.aliases(p.db))[0]}
  except Exception as e:return {'error':type(e).__name__+': '+str(e)}
 out['batch_before']=calculate(dialog.zones.read_definition());definition_id=p.db.top_definition('Haynesville')[0];p.db.rename_top_definition(definition_id,'Haynesville New');root.update();held=dialog.zones.read_definition();out['batch_after_rename']={'live_top_var':dialog.zones.top_var.get(),'alias_resolution':p.db.canonical_top_name('Haynesville'),'current_saved_top':bz.definitions(p.db)[d.name].top_formation,'live_result':calculate(held),'reloaded_result':calculate(bz.definitions(p.db)[d.name])}
 dialog.destroy();root.destroy();p.db.close()
(B/'top-ui-batch-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
