from pathlib import Path
import sys,json,tempfile
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from test_v0972_lic_import import _Fixture,CAL,CAL2
from ograster import lic_import as li
from ogcore import raster
out={}
f=_Fixture();f.setUp()
try:
 api='30-039-27700';src=f.lic(api,group=7);plan,report=f.run_import([src]);row=f.all_rows()[0];own=f.db.resolve_path(row['lic_path']);before=own.read_bytes()
 # Reimport this project's own LIC after a harmless custom line was added by a supported external editor.
 data=before+b'CUSTOM_PRESERVE,original-only\r\n';own.write_bytes(data)
 old=raster.parse_lic(raster.lic_text(data),own);raster.write_lic(own,old.image_file,CAL2,80,1500,old.name,old.uwi,group=7)
 own.write_bytes(own.read_bytes()+b'CUSTOM_PRESERVE,original-only\r\n');before=own.read_bytes()
 plan=li.plan_import(f.db,[own],f.options(overwrite=False),single=False);rep=li.execute(f.db,plan)
 out['own_LIC_overwrite_false']={'source':own.name,'action':plan.items[0].action,'outcome':rep.items[0].outcome,'original_changed':own.read_bytes()!=before,'marker_survived':b'CUSTOM_PRESERVE'in own.read_bytes(),'backups':len(list(own.parent.glob(own.name+'.*.bak'))),'reported_rewritten':rep.items[0].lic_rewritten,'notes':rep.items[0].notes}
finally:f.doCleanups()
f=_Fixture();f.setUp()
try:
 api='30-039-27700';p1=f.lic(api,section='GR',group=1,name='group1.LIC');p2=f.lic(api,section='GR',group=2,name='group2.LIC');_,r=f.run_import([p1,p2]);rows=f.all_rows();own=[f.db.resolve_path(r['lic_path'])for r in rows];plan=li.plan_import(f.db,own,f.options(),single=False);out['group_roundtrip']={'initial_count':len(rows),'stored_sections':[r['lic_section']for r in rows],'exported_groups':[raster.parse_lic(raster.lic_text(p.read_bytes()),p).group for p in own],'reimport_actions':[i.action for i in plan.items],'reimport_reasons':[i.reason for i in plan.items]}
finally:f.doCleanups()
(B/'lic-edge-results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
