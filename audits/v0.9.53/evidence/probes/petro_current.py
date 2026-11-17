import sys,json,time
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path.insert(0,str(R))
from petroworkbench.app import PetroWorkbench
from petroworkbench.well_data import WellData
A=PetroWorkbench();A.withdraw();results={}
try:
 w=WellData.synthetic();w.name='Standalone API well';w.api='42401123450000';state=A._default_workspace(w);A.well_workspaces={'standalone':{'well':w,'state':state}};A.active_well_key='standalone';A.well=w;A._refresh_project_tree();A.update()
 results['standalone_before']={'well_api':w.api,'stored_api':state.get('api'),'tree_rows':A.project_tree_well_rows,'labels':[A.project_tree.item(i,'text') for i in A.project_tree.get_children('wells_node')]}
 A._api_search_focus_in();A.api_search_var.set('4240112345');A.update();results['standalone_search_count']=len(A.project_tree.get_children('wells_node'))
 A.api_search_var.set('');A.update()
 A.well_workspaces={f'w{k}':{'well':None,'state':{'geo_api_uwi':f'42-{k%500:03d}-{k:05d}','well_name':f'W{k}'}} for k in range(5000)}
 A.well_workspaces['tie1']={'well':None,'state':{'geo_api_uwi':'42-001-00001','well_name':'TIE1'}};A.well_workspaces['missing']={'well':None,'state':{'geo_api_uwi':'','well_name':'MISSING'}};A.active_well_key='w0';A._refresh_project_tree();A.update();calls=[];A.switch_well=lambda key:calls.append(key)
 before=dict(A.project_tree_well_keys);start=time.perf_counter();A.api_search_var.set('42-001');A.update();shown=list(A.project_tree.get_children('wells_node'));A.api_search_var.set('');A.update();results['large_filter']={'wells':len(A.well_workspaces),'seconds':time.perf_counter()-start,'matches':len(shown),'restored':len(A.project_tree.get_children('wells_node')),'stable_rows':before==A.project_tree_well_keys,'switched':calls.copy(),'active':A.active_well_key}
 rows=[i for i,k in before.items() if k in ['w1','tie1']];picked=[]
 for i in rows:A.project_tree.selection_set(i);A.update();picked.append({'iid':i,'expected':before[i],'actual':calls[-1]})
 results['duplicate_api_identity']=picked
finally:A.destroy()
Path('/workspace/audit-v0.9.53/petro-independent-evidence.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
