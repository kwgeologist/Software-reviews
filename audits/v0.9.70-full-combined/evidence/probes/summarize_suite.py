from pathlib import Path
import json,xml.etree.ElementTree as E,re,collections
b=Path('/workspace/audit-v0.9.70-full');out={'passed':0,'failed':0,'skipped':0,'subtests_passed':0,'groups':[],'failures':[],'skips':[]}
status=json.loads((b/'suite-status.json').read_text());assert all(r['exit_code']is not None for r in status)
for i in range(1,5):
 log=(b/f'group-{i}/pytest.log').read_text()
 def num(pattern):
  m=re.search(pattern,log);return int(m.group(1))if m else 0
 r={'group':i,'passed':num(r'(\d+) passed'),'failed':num(r'(\d+) failed'),'skipped':num(r'(\d+) skipped'),'subtests_passed':num(r'(\d+) subtests passed'),'exit_code':status[i-1]['exit_code']}
 root=E.parse(b/f'group-{i}/results.xml').getroot();suite=root.find('testsuite');r['xml']=suite.attrib
 for k in ['passed','failed','skipped','subtests_passed']:out[k]+=r[k]
 for t in root.iter('testcase'):
  for elem in ['failure','error','skipped']:
   e=t.find(elem)
   if e is not None:out['skips'if elem=='skipped'else'failures'].append({'group':i,'class':t.get('classname'),'test':t.get('name'),'type':elem,'message':e.get('message'),'text':e.text})
 assert int(suite.get('tests'))==r['passed']+r['failed']+r['skipped']+r['subtests_passed']
 out['groups'].append(r)
out['modules_in_plan']=json.loads((b/'suite-plan.json').read_text())['module_count'];out['partitioned_not_serial']=True
(b/'suite-summary.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items()if k not in ['failures','skips']},indent=2))
