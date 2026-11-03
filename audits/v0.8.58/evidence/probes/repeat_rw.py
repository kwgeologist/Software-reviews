import sys,unittest,json
from pathlib import Path
sys.path[:0]=['/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58','/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58/tests']
from test_petro_integration import PetroIntegrationTests
suite=unittest.TestSuite(PetroIntegrationTests('test_rw_calculator') for _ in range(20));r=unittest.TextTestRunner(verbosity=1).run(suite)
Path('/workspace/audit-v0.8.58/rw-repeat-evidence.json').write_text(json.dumps({'runs':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'interpretation':'Repeated same-process UI regression; passing runs do not establish the cause of an earlier intermittent failure.'},indent=2));sys.exit(not r.wasSuccessful())
