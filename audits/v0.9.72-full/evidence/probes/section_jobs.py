from pathlib import Path
import sys,json
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from test_xsection import WindowTests
x=WindowTests();x.setUp()
try:
 w=x.window();before=len(w._jobs);done=[]
 for k in range(1000):w.later(lambda:done.append(1))
 x.root.update();out={'before_jobs':before,'after_completed_callbacks':len(done),'stored_job_ids_after':len(w._jobs),'pending_tcl_callbacks':list(x.root.tk.call('after','info'))};w.close()
finally:x.tearDown()
(B/'section-job-results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
