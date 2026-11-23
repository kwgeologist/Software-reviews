from pathlib import Path
import json,re,xml.etree.ElementTree as E
B=Path('/workspace/audit-v0.9.72-full');R=B/'full-serial';status=json.loads((R/'status.json').read_text());log=(R/'pytest-native.log').read_text(errors='replace')
if not status.get('finished'):raise SystemExit('Full serial process still running; not a completed result')
signals=re.findall(r'(?:received signal|terminated with signal) (SIG\w+)',log);summaries=[l.strip(' =\n')for l in log.splitlines()if re.search(r'\d+ (?:passed|failed|skipped)',l)and re.search(r'\bin \d+(?:\.\d+)?s',l)]
terminal=summaries[-1]if summaries else None;native_normal=bool(re.search(r'\[Inferior .*exited normally',log));code=re.findall(r'\[Inferior .*exited with code ([0-9]+)',log);inferior_code=0 if native_normal else(int(code[-1],8)if code else None)
r={'finished':True,'gdb_exit_code':status.get('gdb_exit_code'),'inferior_normal_exit':native_normal,'inferior_exit_code_from_gdb':inferior_code,'native_signals':signals,'pytest_terminal':terminal,'seconds':status.get('seconds'),'collected_main_tests':3234,'test_modules':293,'counts':{},'skips':[l for l in log.splitlines()if l.startswith('SKIPPED ')],'notes':['One serial interpreter; separate audit probes ran concurrently on host.','gdb parent exit is not inferior status.','Main inferior peak from pinned VmHWM, not initial zero-valued child enumeration.']}
for field,pattern in [('passed',r'\b(\d+) passed'),('failed',r'\b(\d+) failed'),('skipped',r'\b(\d+) skipped'),('errors',r'\b(\d+) errors?'),('subtests_passed',r'\b(\d+) subtests passed')]:
 m=re.search(pattern,terminal or'');r['counts'][field]=int(m.group(1))if m else 0
m=re.search(r'\bin (\d+(?:\.\d+)?)s',terminal or'');r['pytest_seconds']=float(m.group(1))if m else None
m=re.search(r'\b(\d+) warnings?',terminal or'');r['warning_count']=int(m.group(1))if m else 0
metrics=[json.loads(l)for l in(R/'resource-pinned.jsonl').read_text().splitlines()];peak=max([int(c.get('VmHWM','0').split()[0])for m in metrics for c in m['inferior']]+[0]);r['peak_inferior_RSS_KiB']=peak
xml=R/'results.xml'
if xml.exists():
 root=E.parse(xml).getroot();r['junit_suites']=[s.attrib for s in root.iter('testsuite')];r['failed_cases']=[{'class':t.get('classname'),'test':t.get('name'),'message':next(iter(t.find('failure').attrib.values()),'')}for t in root.iter('testcase')if t.find('failure')is not None]
 r['original_settings_reopen_cases']=[{'class':t.get('classname'),'test':t.get('name'),'result':'failed'if t.find('failure')is not None or t.find('error')is not None else('skipped'if t.find('skipped')is not None else'passed')}for t in root.iter('testcase')if 'test_settings_hold_from_one_session_to_the_next'in(t.get('name')or'')]
else:r['junit_suites']=[];r['failed_cases']=[]
r['main_counts_reconcile']=sum(r['counts'][k]for k in ['passed','failed','skipped','errors'])==r['collected_main_tests']
r['junit_tests_including_subtests']=sum(int(x.get('tests',0))for x in r['junit_suites'])
r['junit_count_reconciles']=r['junit_tests_including_subtests']==r['collected_main_tests']+r['counts']['subtests_passed']
if signals:r['terminal_summary']='NATIVE-STOPPED / not a passing full run: '+', '.join(signals)+'. '+(terminal or'No completed pytest summary/XML.')
elif terminal:r['terminal_summary']=terminal+f'; inferior exit {inferior_code}; gdb exit {r["gdb_exit_code"]}'
else:r['terminal_summary']='INCOMPLETE / no completed pytest summary; not a pass'
r['accepted_complete_pass']=bool(terminal and not signals and inferior_code==0 and r['counts']['failed']==0 and r['counts']['errors']==0 and r['main_counts_reconcile']and r['junit_count_reconciles'])
(R/'final-summary.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
