import sys,tempfile,json
from pathlib import Path
from unittest.mock import patch
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path[:0]=[str(R),str(R/'tests'),str(R/'tools/release')]
import check_protected as CP
from test_v0953_fixes import ProtectedArchives
x=ProtectedArchives();x.setUp()
try:
 data=x.zip_bytes({'ogcore/formulas.py':b'x'*1024})
 program=x.program([('resources/data.bin',data,'x')]);normal=CP.executable_problems(program)
 with patch.object(CP,'MAX_ARCHIVE_BYTES',128):limited=CP.executable_problems(program)
 named=x.program([('resources/data.zip',data,'x')])
 with patch.object(CP,'MAX_ARCHIVE_BYTES',128):namedlimited=CP.executable_problems(named)
 out={'test_limit_bytes':128,'default_limit_bytes':512*1024*1024,'fixture_archive_bytes':len(data),'normal_size_detection':normal,'oversize_magic_only_result':limited,'oversize_archive_named_result':namedlimited,'scope':'reduced limit exercises exact production oversize branch; no 512MB artifact allocated'}
 (B/'protection-limits-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:x.doCleanups()
