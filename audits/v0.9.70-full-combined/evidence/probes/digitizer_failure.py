from pathlib import Path
import sys,tempfile,json,sqlite3,os,subprocess,time
from unittest import mock
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')]
import conftest
from PIL import Image
from ogcore.raster import Calibration
from ogcore.digitize import Curve
from geoworkbench.main_window import WellDataManagerApp
x=subprocess.Popen(['/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb',':206','-screen','0','1600x1000x24','-nolisten','tcp'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);os.environ['DISPLAY']=':206';time.sleep(.2)
try:
 with tempfile.TemporaryDirectory(prefix='v0970-digitizer-failure-')as td:
  r=Path(td);Image.new('RGB',(400,1200),'white').save(r/'log.png')
  with mock.patch('pathlib.Path.home',return_value=r):
   a=WellDataManagerApp();a.withdraw();a.load_project(r/'fixture.ogwdb');db=a.db;wid=db.add_well('Synthetic','');rid=db.add_raster(wid,r/'log.png','Synthetic',Calibration([(1000,0),(2000,1000)]));a.refresh_wells(select_id=wid);a.current_well_id=wid;tab=next(t for t in a.tabs if type(t).__name__=='RasterTab');a.notebook.select(tab);tab.refresh();a.update();tab.tree.selection_set(str(rid));w=tab.digitize();w.update()
   curve=Curve(mnemonic='SYNTH',segments=[[[100,100,0],[200,110,0]]]);w.digitizer.add_curve(curve)
   with mock.patch.object(w.digitize_link,'store',side_effect=sqlite3.OperationalError('injected disk full')):
    w._dig_store(now=True);status=w.dig_status.get();allowed=w._dig_finish();w.close()
   out={'synthetic_image':True,'draft_nodes':curve.node_count,'curve_already_exported':bool(curve.saved),'finish_allowed_after_store_failure':allowed,'window_destroyed':not bool(w.winfo_exists()),'status_before_close':status,'database_digitizing_after_close':db.raster_digitizing(rid)}
   assert curve.node_count==2 and allowed and not w.winfo_exists() and not out['database_digitizing_after_close']
   a.on_close()
  (B/'digitizer-failure.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:x.terminate();x.wait()
