from pathlib import Path
import sys,tempfile,json,time,resource,subprocess,os
from unittest import mock
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')]
import conftest
from database import ProjectDatabase
from ogmap.datastore import MapDataStore
from seismicworkbench.wells import load_wells
out={};x=subprocess.Popen(['/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb',':205','-screen','0','1600x1000x24','-nolisten','tcp'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);os.environ['DISPLAY']=':205';time.sleep(.2)
try:
 with tempfile.TemporaryDirectory(prefix='v0970-scale-')as td:
  root=Path(td);db=ProjectDatabase(root/'synthetic.ogwdb');db.set_project_value('coordinate_system','EPSG:2278');n=112000;t=time.perf_counter()
  with db.atomic()as con:
   con.executemany('insert into wells(well_name,api_uwi,well_uid,created_at,updated_at)values(?,?,?,?,?)',((f'Synthetic {k:06}',f'42{k:012}',f'synthetic-{k}','2026-11-22','2026-11-22')for k in range(n)))
   con.execute('insert into locations(well_id,surface_x,surface_y) select id,3320000+(id%1000),490000+(id/1000) from wells')
  out['seed_seconds']=time.perf_counter()-t
  t=time.perf_counter();store=MapDataStore().load(db);out['map_store_load_seconds']=time.perf_counter()-t;assert len(store.ids)==n
  db.update_well(1,{'well_name':'Changed one'});t=time.perf_counter();changed=store.refresh(db);out['map_one_well_refresh_seconds']=time.perf_counter()-t;out['map_refresh_changed_ids']=sorted(changed);assert changed=={1}
  t=time.perf_counter();wells=load_wells(db);out['seismic_wells_load_seconds']=time.perf_counter()-t;assert len(wells)==n
  db.close();del wells,store
  from geoworkbench.main_window import WellDataManagerApp
  with mock.patch('pathlib.Path.home',return_value=root):
   a=WellDataManagerApp();a.withdraw();t=time.perf_counter();a.load_project(root/'synthetic.ogwdb');out['geo_load_project_including_list_seconds']=time.perf_counter()-t
   t=time.perf_counter();a.refresh_wells();out['geo_full_list_refresh_seconds']=time.perf_counter()-t;out['geo_displayed_rows']=len(a.well_tree.get_children());assert out['geo_displayed_rows']==n
   a.on_close()
 out.update(wells=n,synthetic_only=True,no_LAS_or_raster_assets_in_scale_fixture=True,max_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,processes_competing_with_test_suite=True)
 (B/'scale-probe.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:x.terminate();x.wait()
