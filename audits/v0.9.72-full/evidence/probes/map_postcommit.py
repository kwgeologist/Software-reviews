from pathlib import Path
import sys,json,shapefile
from unittest import mock
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from test_v0971_persistence import DrawingFinish
from ogmap import project
x=DrawingFinish();x.setUp()
try:
 folder=Path(x.db.path).parent;p=folder/'audit_layer.shp'
 with shapefile.Writer(str(p),shapeType=shapefile.POLYGON)as wr:
  wr.field('NAME','C');wr.poly([[[0,0],[1,0],[1,1],[0,0]]]);wr.record('seed')
 layer=project.add_layer(x.db,p);layer_id=int(x.db.row('SELECT id FROM map_layers ORDER BY id DESC')[0]);x.x.win.active_shape_layer=lambda:layer_id;x.digitize();err=None
 with mock.patch.object(x.x.win,'refresh_layers',side_effect=RuntimeError('audit render refresh failure')):
  try:x.t.finish(name='Saved before refresh')
  except Exception as e:err=type(e).__name__+': '+str(e)
 count=lambda:x.db.row('SELECT COUNT(*) FROM map_layer_features WHERE layer_id=?',(layer_id,))[0]
 out={'exception_after_write':err,'stored_features_after_first_finish':count(),'draft_state_after_failed_refresh':x.t.state,'draft_vertices_after_failed_refresh':len(x.t.nodes)}
 with mock.patch.object(x.x.win,'refresh_layers',return_value=None):x.t.finish(name='Saved before refresh')
 out['stored_features_after_retry']=count()
finally:x.tearDown()
(B/'map-postcommit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
