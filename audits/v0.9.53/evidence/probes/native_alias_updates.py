import sys,json,tempfile
from pathlib import Path
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import ihs297,petra_ppf
from test_petra_ppf import write_ppf,FIRST,READABLE
out={}
with tempfile.TemporaryDirectory() as td:
 t=Path(td);db=ProjectDatabase(t/'ihs.ogwdb');parsed=ihs297.parse(R/'tests/data/native/ihs/wells_297.97f');w=parsed.wells[0];parsed.wells=[w]
 ihs297.apply(db,ihs297.plan(db,parsed,'overwrite','EPSG:4326',blank_only=False));wid=db.row('SELECT id FROM wells WHERE api_uwi=?',(w.uwi,))[0];top=ihs297.tops(w)[0];did=db.top_definition(top['formation'])[0];db.rename_top_definition(did,'Canonical renamed IHS')
 before=[dict(r) for r in db.rows('SELECT formation,measured_depth,source FROM formation_tops WHERE well_id=? AND definition_id=?',(wid,did))];code,md,q=w.tops[0];w.tops[0]=(code,md+25,q)
 plan=ihs297.plan(db,parsed,'overwrite','EPSG:4326',blank_only=False);counts=ihs297.apply(db,plan);after=[dict(r) for r in db.rows('SELECT formation,measured_depth,source FROM formation_tops WHERE well_id=? AND definition_id=?',(wid,did))]
 out['ihs']={'input_corrected_MD':md+25,'before':before,'after':after,'counts':dict(counts),'diagnostics':plan.issues.rows()};db.close()
 db=ProjectDatabase(t/'ppf.ogwdb');path=write_ppf(t,FIRST);scan=petra_ppf.scan(path);petra_ppf.apply(db,petra_ppf.Plan(scan,mode='add_update',blank_only=False,datum='EPSG:4326',logs=False));wid=db.row('SELECT id FROM wells WHERE api_uwi=?',(READABLE,))[0];did=db.top_definition('DAKOTA')[0];db.rename_top_definition(did,'Canonical renamed PPF');before=[dict(r) for r in db.rows('SELECT formation,measured_depth,source FROM formation_tops WHERE well_id=? AND definition_id=?',(wid,did))];path.write_text(path.read_text().replace('7607.97622295704','7650.0'));plan=petra_ppf.Plan(petra_ppf.scan(path),mode='add_update',blank_only=False,datum='EPSG:4326',logs=False);counts=petra_ppf.apply(db,plan);after=[dict(r) for r in db.rows('SELECT formation,measured_depth,source FROM formation_tops WHERE well_id=? AND definition_id=?',(wid,did))]
 out['ppf']={'input_corrected_MD':7650,'before':before,'after':after,'counts':dict(counts),'diagnostics':plan.issues.rows()};db.close()
(B/'native-alias-updates-evidence.json').write_text(json.dumps(out,indent=2,default=str));print(json.dumps(out,indent=2,default=str))
