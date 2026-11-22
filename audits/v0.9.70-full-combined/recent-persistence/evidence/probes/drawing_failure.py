from pathlib import Path
import sys,json,sqlite3
from unittest import mock
B=Path('/workspace/audit-v0.9.70-integrity');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')]
import conftest
from test_map_drawing_objects import DrawingTabTests
x=DrawingTabTests();x.setUp()
try:
 t=x.win.drawing_tab;t.start('polygon')
 for k,(fx,fy)in enumerate([(0.2,0.2),(0.4,0.2),(0.4,0.4)]):
  xx,yy=x.at(fx,fy);t.press(xx,yy,mock.Mock(x=100*k,y=50*k,dblclick=False))
 before=list(t.nodes)
 with mock.patch('ogmap.drawings.save',side_effect=sqlite3.OperationalError('injected disk full')):
  try:t.finish(name='Unsaved polygon')
  except sqlite3.OperationalError:raised=True
 out={'vertices_before':before,'vertices_after':list(t.nodes),'state_after':t.state,'write_error_propagated':raised,'persisted_rows':x.db.row("select count(*) from map_drawings where name='Unsaved polygon'")[0]};assert len(before)==3 and not t.nodes and out['persisted_rows']==0
 (B/'drawing-failure.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:x.doCleanups()
