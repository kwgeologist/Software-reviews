"""Read-only reconciliation of supplied Windows B56-W05 evidence against inspected ZIP."""
from pathlib import Path, PureWindowsPath
import json, hashlib, xml.etree.ElementTree as ET
B=Path('/workspace/verify-v0.9.58-B56-W05')
D=B/'windows-results-input/B56-W05-v0958-results'
def read(p):return json.loads(p.read_text())
pkg=read(B/'package-baseline.json')
expected={m['module'].split('.')[-1]:m['sha256'] for m in pkg['modules']}
recorded=read(D/'package-licensing-hashes.json')
assert recorded['independently_pinned_to_release_zip']is True
assert recorded['archive_sha256']==read(B/'archive-baseline.json')['sha256']
assert recorded['recorded_on_windows_host']==expected
summary=read(D/'windows-B56-W05-summary.json')
assert not summary.get('error') and 'traceback'not in summary
assert summary['host_clock_changed']is False and summary['source_or_package_modified']is False
root=PureWindowsPath(summary['package'])/'_internal'/'ogcore'
origins=[]
for pattern in ['origins-*.json','pytest-origins-*.json']:
 files=sorted(D.glob(pattern));assert files
 for p in files:
  data=read(p);modules=data.get('modules',data)
  assert set(modules)==set(expected),p.name
  for stem,digest in expected.items():
   item=modules[stem]
   assert item['sha256']==digest,(p.name,stem)
   assert PureWindowsPath(item['path'])==root/(stem+'.cp312-win_amd64.pyd'),(p.name,stem)
   if 'modules'in data:assert item['loader']=='ExtensionFileLoader'
  if 'pid'in data:assert p.stem=='origins-'+str(data['pid'])
  origins.append({'file':p.name,'module_hashes_match':True,'package_paths_match':True})
cases=summary['cases']
assert cases['DPAPI_restart_reimport_renewal_original_denied']=='passed'
assert cases['DPAPI_concurrent_processes']=='passed'
timeout=cases['DPAPI_real_lock_timeout']
assert timeout['wait_seconds']>=10
assert timeout['record_present_before_holder_release']is True
assert timeout['record_present_after_holder_release']is True
for n in ['expired_status','restart_status','rollback_status','reimport_status','original_after_renewal']:assert timeout[n]=='expired',n
for n in ['renewal_status','renewal_check_status']:assert timeout[n]=='valid',n
assert timeout['pending_files_after_merge']==0 and timeout['reproduced']is False
assert summary['pytest_exit_code']==0 and summary['verdict_for_timeout_probe']=='held-lock regression passed'
log=(D/'windows-compiled-tests.log').read_text()
line='56 passed, 1 deselected, 5 subtests passed in 73.22s (0:01:13)'
assert line in log and summary['pytest_summary']==[line]
xml=ET.parse(D/'windows-compiled-results.xml').getroot()
suites=list(xml.iter('testsuite'));assert len(suites)==1
suite=suites[0];assert suite.attrib['tests']=='61'
for n in ['errors','failures','skipped']:assert suite.attrib[n]=='0',n
assert len(list(xml.iter('testcase')))==56
assert not list(xml.iter('failure'))and not list(xml.iter('error'))and not list(xml.iter('skipped'))
assert all('test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository'not in case.attrib['name']for case in xml.iter('testcase'))
command=summary['pytest_command'];assert 'no:cacheprovider'in command
for f in ['test_licensing.py','test_v0957_fixes.py','test_v0958_fixes.py']:assert any(PureWindowsPath(v).name==f for v in command)
assert command[command.index('-k')+1]=='not test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository'
assert '-O'not in command
out={'verdict':'closed for the shipped Windows licensing extensions','source_commit':'104bf4f32cbc66ab2f01ca865f388ea016cc7922','results_zip_sha256':'a7ce052bc7d7a833c39c29ffab31c8e858aa69a3941ad3d3846e183710dc3c11','all_origin_records_match':True,'helper_origin_records':len(list(D.glob('origins-*.json'))),'pytest_origin_records':len(list(D.glob('pytest-origins-*.json'))),'origins':origins,'timeout_seconds':timeout['wait_seconds'],'all_requested_lifecycle_checks_passed':True,'pytest':{'passed':56,'passing_subtests':5,'deselected':1,'failed':0,'errors':0,'skipped':0,'exit_code':0,'xml_suite_tests':61,'xml_testcase_elements':56,'explanation':'Suite count 61 comprises 56 tests plus five passing subtests; XML contains 56 testcase elements.'},'customer_executable_executed':False,'evidence_provenance':'User-executed Windows run; independently reconciled here against prior customer ZIP inspection, not rerun on this Linux host.'}
(B/'windows-evidence-reconciliation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
