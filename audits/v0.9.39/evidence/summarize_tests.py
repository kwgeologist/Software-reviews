import json,re,xml.etree.ElementTree as ET
from pathlib import Path
B=Path('/workspace/audit-v0.9.39');results=json.loads((B/'isolated-results.json').read_text());totals={k:0 for k in ['passed','failed','skipped','errors','subtests_passed']};issues=[];skips=[]
for r in results:
 p=B/'isolated-tests'/Path(r['file']).with_suffix('.log');s=p.read_text(errors='replace')
 lines=[line for line in s.splitlines() if re.search(r'\b\d+ (passed|failed|skipped|error)',line) and not line.startswith(('FAILED','ERROR'))]
 line=lines[-1] if lines else ''
 for key,rx in [('passed',r'(?<!subtests )\b(\d+) passed'),('failed',r'\b(\d+) failed'),('skipped',r'\b(\d+) skipped'),('errors',r'\b(\d+) errors?'),('subtests_passed',r'\b(\d+) subtests passed')]:
  m=re.search(rx,line)
  if m:totals[key]+=int(m[1])
 xml=B/'isolated-tests'/Path(r['file']).with_suffix('.xml')
 if xml.exists():
  for case in ET.parse(xml).iter('testcase'):
   for child in list(case):
    if child.tag in ('failure','error'):issues.append({'file':r['file'],'class':case.get('classname'),'test':case.get('name'),'message':child.get('message')})
    if child.tag=='skipped':skips.append({'file':r['file'],'test':case.get('name'),'reason':child.get('message')})
 if r['exit_code'] not in (0,1):issues.append({'file':r['file'],'exit_code':r['exit_code'],'summary':line})
summary={'completed_files':len(results),'expected_files':243,'collected_test_cases':2615,'mode':'one fresh process per test file, serial; original monolithic run crashed','counts':totals,'subprocess_seconds':sum(r['seconds'] for r in results),'issues':issues}
(B/'test-summary.json').write_text(json.dumps(summary,indent=2));(B/'skipped-tests.json').write_text(json.dumps(skips,indent=2));print(json.dumps(summary,indent=2))
