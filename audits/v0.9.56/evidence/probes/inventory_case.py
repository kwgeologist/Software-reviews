from pathlib import Path
import sys,json,tempfile,zipfile
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56';sys.path[:0]=[str(R),str(R/'tools/release'),str(R/'tests')]
from test_release_payload import good_payload
import inventory,check_protected
out={}
with tempfile.TemporaryDirectory() as td:
 d=good_payload(Path(td))
 with zipfile.ZipFile(d/'_internal/base_library.zip','w'):pass
 out['baseline_inventory_failures']=inventory.scan(d)['failures']
 for name in ['_internal/ogcore/formulas.py.bak','_internal/geoworkbench/extra.py','_internal/geoworkbench/extra.PY','_internal/geoworkbench/extra.py.bak','_internal/OGCORE/userdata.PY','_internal/data/archive.OGWDB','_internal/.GIT/config']:
  p=d/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/'ogcore/formulas.py').read_bytes() if name.endswith('formulas.py.bak') else b'audit fixture only')
  out[name]={'inventory_failures':inventory.scan(d)['failures'],'protected_tree_problems':check_protected.tree_problems(d)};p.unlink()
(B/'inventory-case-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
