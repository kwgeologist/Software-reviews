from pathlib import Path
import sys,json,tempfile,ast,copy
from types import SimpleNamespace as NS
from unittest.mock import patch
B=Path('/workspace/audit-v0.9.63-stale-tops');C=B/'checkout';sys.path.insert(0,str(C))
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from database import ProjectDatabase
from xsection import model,dialogs,render
from xsection.window import CrossSectionWindow as Window
from xsection.store import Store
from xsection.layout import SectionLayout
from geoworkbench.interpretation_dialogs import TopDefinitionsDialog
GHOST=['ASTN','605ASTN','ASTNB','605ASTNB','CRCSL','602CRCSL','BUDA','602BUDA','GRGN','602GRGN','FRWR','602FRWR']
# Execute the exact constructor's non-widget state assembly, not a rewritten equivalent.
tree=ast.parse((C/'xsection/dialogs.py').read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef)and n.name=='TopsDialog');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef)and n.name=='__init__');body=[];active=False
for n in init.body:
 if isinstance(n,ast.Assign)and any(isinstance(a,ast.Attribute)and a.attr=='section'for a in n.targets):active=True
 if isinstance(n,ast.Assign)and any(isinstance(a,ast.Name)and a.id=='b'for a in n.targets):break
 if active:body.append(copy.deepcopy(n))
f=copy.deepcopy(init);f.name='assemble';f.body=body;module=ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[]));env=dict(vars(dialogs));exec(compile(module,str(C/'xsection/dialogs.py'),'exec'),env);assemble=env['assemble']
class Var:
 def __init__(self,v):self.v=v
 def get(self):return self.v
 def set(self,v):self.v=v
class Box:
 def configure(self,**kw):self.values=kw.get('values',[])
class Tree:
 def insert(self,*args,**kw):pass

def manager(section,store):
 rows=[];w=NS(tree=Tree(),section=section,store=store,layout=None,_group_row=lambda *a:None,_item=lambda *a:rows.append(a))
 Window._list_manager(w,set());return [r[1][4:]for r in rows if r[0]=='tops']
def draw(section,store):
 layout=SectionLayout(store,section,section.display);fig=Figure();ax=fig.add_subplot(111);engine=render.Engine(ax,None,layout,vertical_scale=section.vertical_scale,styles={t.name.casefold():t for t in section.tops})
 for place in layout.places:engine._well_markers(place,place.left,place.right)
 engine.draw_interpretation();return sorted({t['name']for t in engine.drawn.top_marks})
with tempfile.TemporaryDirectory(prefix='stale-tops-audit-')as td:
 path=Path(td)/'synthetic.ogwdb';db=ProjectDatabase(path);db.set_project_value('coordinate_system','EPSG:2231');db.set_active_source('LO')
 wells=[db.add_well('Synthetic '+str(i),'seller-'+str(i))for i in range(2)]
 for i,w in enumerate(wells):
  db.update_well(w,{'total_depth_md':3000,'kb_elevation':500})
  db.execute('INSERT INTO locations(well_id,surface_x,surface_y)VALUES(?,?,?)',(w,3000000+i*1000,1200000))
  for k,name in enumerate(GHOST):db.set_formation_top(w,name,1000+k*10,'OLD')
  db.set_formation_top(w,'Surviving LO',1300,'LO');db.set_formation_top(w,'Surviving BMB',1400,'BMB')
 first=db.top_definition('ASTN',create=False)[0];db.add_top_alias(first,'Old ASTN alias')
 section=model.Section('Audit',[model.SectionWell(w)for w in wells]);store=Store(db);Window._add_top_styles(NS(store=store),section);store.save_section(section)
 before=draw(section,store)
 # Invoke the actual Global Manager delete method; only its confirmation/UI refresh are stubbed.
 definitions={str(d['id']):d for d in db.top_definitions()if d['name']in GHOST}
 ui=NS(db=db,chosen=lambda:list(definitions),definitions=definitions,changed=lambda message:None)
 with patch('geoworkbench.interpretation_dialogs.messagebox.askyesno',return_value=True):TopDefinitionsDialog.delete(ui)
 canonical=db.formation_names();sources=db.interpretation_sources('tops');assert sources==['BMB','LO'],sources
 assert not set(GHOST)&set(canonical);assert db.top_aliases()==[];assert len(db.rows("SELECT * FROM formation_tops WHERE source='OLD'"))==0
 stale_render=draw(section,store)
 store.refresh_picks();Window._add_top_styles(NS(store=store),section);fresh_render=draw(section,store)
 state=NS();assemble(state,None,section,canonical,db=db);state.source=lambda:'';all_list=[t.name for t in state.styles if dialogs.TopsDialog.listed(state,t)]
 state.source=lambda:'LO';lo_list=[t.name for t in state.styles if dialogs.TopsDialog.listed(state,t)]
 # A cached explicit source style also bypasses absence of any current source picks.
 stale=next(t for t in state.styles if t.name=='ASTN');stale.source='LO';state.__dict__.pop('_source_tops',None);lo_explicit=dialogs.TopsDialog.listed(state,stale)
 state.destroy=lambda:None;state.show_source=Var(False);state.label_place=Var('Inside track');dialogs.TopsDialog._ok(state)
 store.save_section(section);manager_list=manager(section,store)
 # Toolbar draft names are separate from the canonical list and the style list.
 draft=NS(db=db,_new_tops=['ASTN'],section=section,target_box=Box(),datum_box=Box(),pick_target=Var('ASTN'));Window._fill_targets(draft)
 db.close();db=ProjectDatabase(path);reopened=Store(db);loaded=reopened.sections()['Audit'];after_reopen_canonical=db.formation_names()
 again=NS();assemble(again,None,loaded,after_reopen_canonical,db=db)
 result={'baseline_commit':'42d8e330cc6013c73cedd1ca4f2cf4bae1cadc01','project_kind':'temporary synthetic; no client database supplied','global_manager_delete_method_executed':True,'deleted_names':GHOST,'canonical_after_delete':canonical,'current_sources_after_delete':sources,'aliases_after_delete':[],'deleted_source_pick_count':0,'render_before_delete':before,'render_after_delete_before_pick_refresh':stale_render,'render_after_pick_refresh':fresh_render,'tops_dialog_all_sources':[t for t in all_list if t in GHOST],'tops_dialog_LO_without_explicit_style':[t for t in lo_list if t in GHOST],'tops_dialog_explicit_LO_style_without_LO_pick':lo_explicit,'display_manager_deleted_rows':[t for t in manager_list if t in GHOST],'canonical_after_reopen':after_reopen_canonical,'saved_deleted_styles_after_reopen':[t.name for t in loaded.tops if t.name in GHOST],'dialog_deleted_rows_after_reopen':[t.name for t in again.styles if t.name in GHOST],'conditional_draft_target_survives_delete':'ASTN'in draft.target_box.values,'methodology':'Actual database/manager deletion, Store, model, renderer, _list_manager and _ok methods; no Tk display. Dialog data-assembly AST extracted unchanged before first widget access; tree collection uses UI sinks.'}
 assert len(result['tops_dialog_all_sources'])==12 and len(result['display_manager_deleted_rows'])==12
 assert not set(GHOST)&set(fresh_render)and set(GHOST)<=set(stale_render)
 assert not set(GHOST)&set(after_reopen_canonical)and len(result['dialog_deleted_rows_after_reopen'])==12
 db.close()
(B/'stale-tops-evidence.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
