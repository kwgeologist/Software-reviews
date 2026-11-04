import os,sys,tempfile,json,time,sqlite3
from pathlib import Path
from collections import Counter
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path.insert(0,str(R))
from database import ProjectDatabase
from ogcore import ihs298 as I,symbol_catalog as C
import well_symbols as W
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);os.environ['OGW_SYMBOL_CATALOG']=str(p/'catalog.json');C.install(C.builtin());db=ProjectDatabase(p/'p.ogwdb');entities=[]
 for n,suffix in enumerate(['00','01','02']):entities.append(I.Entity(str(n),1,uwis=['424011234500'+suffix],lease_name='Synthetic Lease '+suffix,operator='Synthetic Operator',field_name='Synthetic Field',months={'2025-01':{'oil':100.+n,'gas':200.+n,'water':0.}}))
 parsed=I.Parsed(p/'synthetic.98c',entities=entities,issues=I.Issues());plan=I.plan(db,parsed);done=I.apply(db,plan);before=[dict(r)for r in db.rows('SELECT w.id,w.api14,p.id AS production_id,p.month,p.oil,p.gas FROM wells w JOIN production_monthly p ON p.well_id=w.id ORDER BY w.api14')];again=I.plan(db,parsed);out['completion_identity']={'rows':before,'reimport_counts':dict(again.counts),'create_again':len(again.create)};I.apply(db,again);db.close();db=ProjectDatabase(p/'p.ogwdb');after=[dict(r)for r in db.rows('SELECT w.id,w.api14,p.id AS production_id,p.month,p.oil,p.gas FROM wells w JOIN production_monthly p ON p.well_id=w.id ORDER BY w.api14')];out['completion_identity']['same_ids_and_values_after_reopen']=before==after
 db.execute('UPDATE production_monthly SET oil=999 WHERE well_id=?',(before[1]['id'],));q=I.plan(db,parsed);out['one_completion_conflict']={'conflicts':q.counts['conflict'],'identical':q.counts['identical']};db.close()
 # Validates adding the provenance columns to an otherwise schema-29 project, twice.
 db=ProjectDatabase(p/'old.ogwdb');wid=db.add_well('Legacy','42401111110000');db.update_well(wid,{'well_symbol_code':'DRYSO','well_symbol_id':58});db.close();con=sqlite3.connect(p/'old.ogwdb');con.execute('ALTER TABLE seismic_horizons DROP COLUMN provenance');con.execute('ALTER TABLE seismic_faults DROP COLUMN provenance');con.commit();con.close();states=[]
 for _ in range(2):
  db=ProjectDatabase(p/'old.ogwdb');states.append({'well':dict(db.row('SELECT id,api14,well_symbol_code,well_symbol_id FROM wells WHERE id=?',(wid,))),'horizon_provenance_column':any(r[1]=='provenance'for r in db.rows('PRAGMA table_info(seismic_horizons)')),'fault_provenance_column':any(r[1]=='provenance'for r in db.rows('PRAGMA table_info(seismic_faults)'))});db.close()
 out['migration_idempotence']=states
 # 298 all-or-nothing write rollback across new wells and monthly rows.
 db=ProjectDatabase(p/'cancel.ogwdb');plan=I.plan(db,parsed)
 class Task:
  cancelled=False
  def __call__(self,*args):self.cancelled=True
 try:I.apply(db,plan,task=Task())
 except Exception as e:out['cancel_rollback']={'exception':type(e).__name__,'wells':db.row('SELECT COUNT(*) FROM wells')[0],'months':db.row('SELECT COUNT(*) FROM production_monthly')[0]}
 db.close()
 out['active_codes']=C.builtin().active_codes();out['shared_primitives']={a+'='+b:W.glyph_primitives(W.symbol_for_code(a))==W.glyph_primitives(W.symbol_for_code(b))for a,b in [('PLUGOIL','PAOW'),('DRILWELL','DERRICK'),('DRL','DERRICK')]}
(R.parent/'identity-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
