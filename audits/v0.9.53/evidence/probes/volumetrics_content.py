import sys,json,hashlib,importlib.util
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_v0941_fixes import VolumetricsCsv
from ogvol import report
old=Path('/workspace/audit-v0.9.40/OandG_Workbench_v0.9.40/ogvol/report.py')
if not old.exists():raise SystemExit('Optional old-reference comparison needs the separate v0.9.40 source archive')
T=VolumetricsCsv();T.setUp()
try:
 spec=importlib.util.spec_from_file_location('ogvol.old_reference',old);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 newfile=T.out;oldfile=T.out.with_name('reference.csv');report.write_csv(newfile,'Base',T.record);m.write_csv(oldfile,'Base',T.record);out={'reference':'previous supplied v0.9.40 ogvol/report.py, not asserted Git commit provenance','old_module_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'byte_identical':newfile.read_bytes()==oldfile.read_bytes(),'bytes':newfile.stat().st_size};assert out['byte_identical'];Path('/workspace/audit-v0.9.53/volumetrics-content-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:T.doCleanups()
