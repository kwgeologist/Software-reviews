from pathlib import Path
import re,json,xml.etree.ElementTree as X
B=Path('/workspace/audit-v0.9.52');out={};skips={};fails={}
for label,logname,xmlname in [('full','full-tests.log','full-results.xml'),('parallel_full','parallel-full.log','parallel-full-results.xml'),('targeted','targeted-tests.log','targeted-results.xml'),('compiled','compiled-tests.log','compiled-results.xml'),('parallel_gui','parallel-gui.log','parallel-gui-results.xml'),('parallel_gui_extended','parallel-gui-extended.log','parallel-gui-extended-results.xml')]:
 log=(B/logname).read_text();lines=[s for s in log.splitlines() if re.search(r'\d+ passed.* in [\d.]+s',s)];line=lines[-1] if lines else 'summary pending';summary={'summary':line};root=X.parse(B/xmlname).getroot();cases=list(root.iter('testcase'))
 for key in ['passed','failed','skipped','errors']:
  m=re.search(r'(\d+) '+key+r'\b',line);summary[key]=int(m.group(1)) if m else 0
 m=re.search(r'(\d+) subtests passed',line);summary['subtests_passed']=int(m.group(1)) if m else 0
 summary['xml_testcases']=len(cases)
 skips[label]=[{'class':c.get('classname'),'test':c.get('name'),'reason':c.find('skipped').get('message')} for c in cases if c.find('skipped') is not None]
 fails[label]=[{'class':c.get('classname'),'test':c.get('name'),'message':c.find('failure').get('message'),'trace':c.find('failure').text} for c in cases if c.find('failure') is not None]
 out[label]=summary
for n,d in [('test-summary',out),('skipped-tests',skips),('failed-tests',fails)]:(B/(n+'.json')).write_text(json.dumps(d,indent=2))
print(json.dumps(out,indent=2))
