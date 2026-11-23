from pathlib import Path
import json,re,xml.etree.ElementTree as E,collections,subprocess,hashlib
B=Path('/workspace/audit-v0.9.70-tk-segfault');r={'runs':[],'original_SIGSEGV_reproduced':False,'pytest_totals':collections.Counter(),'controlled_native':[],'lifecycle':{}}
for p in sorted((B/'runs').glob('*/status.json')):
 d=json.loads(p.read_text())
 if not isinstance(d,dict):continue
 log=p.with_name('run.log').read_text(errors='replace');row={k:d.get(k)for k in ['name','Tk_requested','observer','native','exit_code','seconds','parent_peak_RSS_KiB','timed_out']};row['native_signals']=re.findall(r'received signal (SIG\w+)',log);row['fatal_markers']=re.findall(r'Fatal Python error: ([^\n]+)',log)
 if 'Segmentation fault'in log or d['exit_code']==-11:r['original_SIGSEGV_reproduced']=True
 xml=p.with_name('results.xml')
 if xml.exists():
  x=E.parse(xml).getroot().find('testsuite');row['xml']=x.attrib
  row['failures']=[{'class':t.get('classname'),'test':t.get('name'),'message':t.find('failure').get('message')}for t in x.iter('testcase')if t.find('failure')is not None]
  for k in ['tests','failures','errors','skipped']:r['pytest_totals'][k]+=int(x.get(k,'0'))
 obs=p.with_name('observations.jsonl')
 if obs.exists():
  data=[json.loads(x)for x in obs.read_text().splitlines()];samples=[x for x in data if'counts'in x];row['observation_samples']=len(samples)
  if samples:row['last_sample']=samples[-1];row['peak_roots_observed']=max(len(x.get('roots',[]))for x in samples);row['peak_figures_observed']=max(x.get('retained_figures',0)for x in samples)
  row['worker_gc_events']=sum(x['event']=='gc_on_worker'for x in data);row['worker_Tk_Python_entries']=sum(x['event']=='cross_thread_tk_python_entry'for x in data)
 r['runs'].append(row)
for v in ['86','9']:
 r['lifecycle'][v]={}
 for mode in ['normal','destroy']:
  p=B/f'runs/B-{v}/{mode}.jsonl'
  if p.exists():r['lifecycle'][v][mode]=[json.loads(x)for x in p.read_text().splitlines()]
for p in (B/'runs/minimal').glob('native-*.log'):
 log=p.read_text();r['controlled_native'].append({'file':str(p.relative_to(B)),'signals':re.findall(r'received signal (SIG\w+)',log),'Tkapp_Dealloc':'Tkapp_Dealloc'in log,'Tcl_AsyncDelete':'Tcl_AsyncDelete'in log})
(B/'summary.json').write_text(json.dumps(r,indent=2));print(json.dumps({'runs':len(r['runs']),'tests':r['pytest_totals'],'segv':r['original_SIGSEGV_reproduced']}))
