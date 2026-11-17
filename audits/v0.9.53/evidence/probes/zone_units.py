import sys,tempfile,json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path.insert(0,str(R))
from database import ProjectDatabase
from petroworkbench.geo_link import GeoLinkMixin,PETRO_SOURCE
from ogmap import sources
with tempfile.TemporaryDirectory() as td:
 db=ProjectDatabase(Path(td)/'p.ogwdb');ctx=SimpleNamespace(geo_db=db,curve_source=lambda name:name,_calculation_axis=GeoLinkMixin._calculation_axis)
 wells=[]
 for name,unit,end in [('Feet','ft',100.0),('Metres','m',30.48)]:
  wid=db.add_well(name,'');db.update_well(wid,{'elevation_units':unit});db.execute('INSERT INTO locations(well_id,surface_x,surface_y) VALUES (?,?,?)',(wid,500000+wid*100,4800000))
  depth=np.linspace(0,end,11);well=SimpleNamespace(depth=depth,depth_unit=unit,curves={'X':np.ones(11)},units={'X':''})
  state={'depth_unit':unit,'zones':[{'name':'SAME_ZONE','top':0,'base':end}],'pay_flags':[{'name':'SAME_PAY','zone':'SAME_ZONE','criteria':[{'curve':'X','op':'>','value':0.5}]}]}
  out=GeoLinkMixin._zone_results(ctx,wid,well,state);db.publish_zone_values(wid,out,PETRO_SOURCE);wells.append({'well':name,'unit':unit,'expected_net_own_unit':end,'published_net':out[('SAME_ZONE','SAME_PAY net')]})
 rows=[dict(r) for r in db.rows('SELECT w.well_name,a.name,a.units,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id JOIN wells w ON w.id=v.well_id WHERE a.name=? ORDER BY w.id',('SAME_PAY net',))]
 source={'kind':'zone_attribute','zone':'SAME_ZONE','name':'SAME_PAY net'}
 pts=sources.collect(db,source)
 result={'published':wells,'stored':rows,'map_unit':sources.unit(db,source),'map_values':pts.value.tolist()};print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.53/zone-units-evidence.json').write_text(json.dumps(result,indent=2));db.close()
