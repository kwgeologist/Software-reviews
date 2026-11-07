import sys,tempfile,json
from pathlib import Path,PureWindowsPath
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path[:0]=[str(R),str(R/'tests')]
from test_seismic_picks_io import open_project
from seismicworkbench import picks_io as IO
from ogmap.grids import _file_name
from ogcore.project import _safe_name
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);path,db,sid,shape=open_project(p/'A');file=p/'previous.csv';file.write_bytes(b'previous reviewed export')
 try:
  with patch('seismicworkbench.picks_io.csv.DictWriter.writerows',side_effect=OSError('synthetic output failure')):IO.export_native(db,'Horizon',[],file)
 except OSError as e:out['failed_export']={'error':str(e),'old_bytes_preserved':file.read_bytes()==b'previous reviewed export','new_file_prefix':file.read_text()[:90]}
 db.close()
out['windows_reserved_names']={name:{'project_name':_safe_name(name),'grid_file':_file_name(name)+'.oggrid','reserved_windows_path':PureWindowsPath(_file_name(name)+'.oggrid').is_reserved()}for name in ['CON','NUL','AUX']}
(B/'output-boundaries-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
