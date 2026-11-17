from pathlib import Path
import re,json,xml.etree.ElementTree as X
B=Path('/workspace/audit-v0.9.53');out={};skips={};fails={}
for label,stem in [('full','full'),('targeted','targeted'),('compiled','compiled'),('compiled_integration','compiled-integration')]:
 logp=B/(stem+'-tests.log');xmlp=B/(stem+'-results.xml')
 if not xmlp.exists():continue
 lines=[s for s in logp.read_text().splitlines() if re.search(r'\d+ passed.* in [\d.]+s',s)]
 if not lines:continue
 line=lines[-1];summary={'summary':line};root=X.parse(xmlp).getroot();cases=list(root.iter('testcase'))
 for key in ['passed','failed','skipped','errors']:
  m=re.search(r'(\d+) '+key+r'\b',line);summary[key]=int(m.group(1)) if m else 0
 m=re.search(r'(\d+) subtests passed',line);summary['subtests_passed']=int(m.group(1)) if m else 0
 summary['xml_testcases']=len(cases);summary['files']=sorted({c.get('classname').split('.')[1] for c in cases})
 skips[label]=[{'class':c.get('classname'),'test':c.get('name'),'reason':c.find('skipped').get('message')} for c in cases if c.find('skipped') is not None]
 fails[label]=[{'class':c.get('classname'),'test':c.get('name'),'message':c.find('failure').get('message'),'trace':c.find('failure').text} for c in cases if c.find('failure') is not None]
 out[label]=summary
for n,d in [('test-summary',out),('skipped-tests',skips),('failed-tests',fails)]:(B/(n+'.json')).write_text(json.dumps(d,indent=2))
print(json.dumps({k:v['summary']for k,v in out.items()},indent=2))
