from pathlib import Path
import sys,json,tempfile,gc
from unittest import mock
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from geoworkbench.main_window import WellDataManagerApp
from ogcore import well_selection
with tempfile.TemporaryDirectory(prefix='audit-owner-')as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
 a=WellDataManagerApp();a.withdraw();a.destroy();rows=[]
 for job in a.tk.call('after','info'):
  info=a.tk.call('after','info',job);script=str(info[0]);rows.append({'job':job,'script':script,'type':str(info[1]),'script_command_exists':bool(a.tk.call('info','commands',script))})
 print(json.dumps({'pending_after_destroy':rows},indent=2))
 well_selection.unsubscribe(a._selection_changed)
