from pathlib import Path
import sys,tempfile,json,hashlib,subprocess
import numpy as np
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path.insert(0,str(C))
sys.path.insert(0,str(C/'tests'))
import conftest
from database import ProjectDatabase
from ogmap.datastore import MapDataStore,store_wells
from ogmap import project,sources
from seismicworkbench.wells import load_wells,map_paths
from ogcore.well_geometry import map_unit_feet,depth_unit_feet
baseline={n:hashlib.sha256((C/n).read_bytes()).hexdigest()for n in subprocess.check_output(['git','ls-files','-z'],cwd=C).decode().strip('\0').split('\0')};(B/'map-parity-source-snapshot.json').write_text(json.dumps(baseline,indent=2))
result={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=C,text=True).strip(),'synthetic_only':True,'ui_executed':False,'cases':[]}
for crs,unit in [('EPSG:32613','m'),('EPSG:2278','ft')]:
 with tempfile.TemporaryDirectory(prefix='map-anchor-audit-')as td:
  db=ProjectDatabase(Path(td)/'fixture.ogwdb');db.set_project_value('coordinate_system',crs);assert map_unit_feet(db)is not None;ids={};sl=(500000.,3200000.)
  for name,bottom,survey in [('vertical',None,False),('conflicting_BHL',(sl[0]+1000,sl[1]+1200),True),('survey_no_BHL',None,True),('typed_no_survey',(sl[0]+1000,sl[1]+1200),False),('BHL_only',(sl[0]+1000,sl[1]+1200),False),('invalid_BHL',(sl[0]+1e8,sl[1]+1e8),True)]:
   w=db.add_well(name,'audit-'+name);ids[name]=w
   db.execute('UPDATE wells SET elevation_units=?,total_depth_md=4000,well_symbol_code=? WHERE id=?',(unit,'OIL',w))
   db.execute('INSERT INTO locations(well_id,surface_x,surface_y,bottom_x,bottom_y) VALUES(?,?,?,?,?)',(w,None if name=='BHL_only'else sl[0],None if name=='BHL_only'else sl[1],None if bottom is None else bottom[0],None if bottom is None else bottom[1]))
   if survey:
    for md,ew,ns in [(0,0,0),(1000,300,400),(2000,600,800)]:db.execute('INSERT INTO deviation_points(well_id,measured_depth,tvd,east_west,north_south)VALUES(?,?,?,?,?)',(w,md,md*.8,ew,ns))
  store=MapDataStore().load(db);wells=load_wells(db);lookup={w.id:w for w in wells};shared=map_paths(wells);light={w.id:w for w in store_wells(store,np.flatnonzero(store.located))}
  for mode in ['surface','bottom hole']:
   regular_x,regular_y=store.posted_xy(mode=='bottom hole');seismic,_=project.posted_wells(wells,dict(project.DEFAULT_LABELS,symbol_at=mode),{});posted={w['id']:w for w in seismic}
   for name,w in ids.items():
    row=store.row_of(w);path=store.path(row);other=shared.get(w)
    assert (path is None)==(other is None)
    if path is not None:np.testing.assert_allclose(path,other,atol=1e-8)
    a=np.array([regular_x[row],regular_y[row]]);s=np.array([posted[w]['x'],posted[w]['y']]);same=np.allclose(a,s,atol=1e-7,rtol=0)
    assert same,(name,mode,a,s)
    case={'crs':crs,'depth_units':unit,'name':name,'mode':mode,'stick_start':None if path is None else path[0].tolist(),'stick_end':None if path is None else path[-1].tolist(),'regular_symbol':a.tolist(),'seismic_symbol':s.tolist(),'maps_agree':bool(same),'separation_map_units':float(np.linalg.norm(a-s)),'regular_bottom_post':list(sources._position(light[w],'bottom'))}
    if name=='conflicting_BHL'and mode=='bottom hole':
     np.testing.assert_allclose(s,path[-1],atol=1e-8);np.testing.assert_allclose(a,path[-1],atol=1e-8)
    result['cases'].append(case)
  conflict=ids['conflicting_BHL'];old=store.posted_xy(True);oldsymbol=[float(old[0][store.row_of(conflict)]),float(old[1][store.row_of(conflict)])]
  db.execute('UPDATE deviation_points SET east_west=east_west+50 WHERE well_id=? AND measured_depth=2000',(conflict,));changed=store.refresh(db);assert conflict in changed;fresh=store.posted_xy(True);assert oldsymbol!=[float(fresh[0][store.row_of(conflict)]),float(fresh[1][store.row_of(conflict)])]
  end=store.path(store.row_of(conflict))[-1].copy();db.close();db=ProjectDatabase(Path(td)/'fixture.ogwdb');again=MapDataStore().load(db);xy=again.posted_xy(True);np.testing.assert_allclose(again.path(again.row_of(conflict))[-1],end);np.testing.assert_allclose([float(xy[0][again.row_of(conflict)]),float(xy[1][again.row_of(conflict)])],end)
  result.setdefault('refresh_reopen',[]).append({'crs':crs,'changed_well_reloaded':True,'survey_end_changed':end.tolist(),'prior_display_symbol':oldsymbol,'display_symbol_tracks_changed_endpoint_after_reopen':True});db.close()
result['path_parity_assertions']=24;result['mismatch_cases']=sum(not c['maps_agree']for c in result['cases']);assert result['mismatch_cases']==0
(B/'map-parity-evidence.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
