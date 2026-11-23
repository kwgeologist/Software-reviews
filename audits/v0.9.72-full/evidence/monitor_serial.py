from pathlib import Path
import json,time
B=Path('/workspace/audit-v0.9.72-full/full-serial');pid=json.loads((B/'status.json').read_text())['gdb_pid'];peak=0
with (B/'resource-metrics.jsonl').open('w')as h:
 while Path(f'/proc/{pid}').exists():
  ids=set()
  for p in Path(f'/proc/{pid}/task').glob('*/children'):
   try:ids.update(p.read_text().split())
   except OSError:pass
  rows=[]
  for child in ids:
   try:
    s=Path(f'/proc/{child}/status').read_text().splitlines();r={l.split(':')[0]:l.split(':',1)[1].strip()for l in s};rss=int(r.get('VmRSS','0').split()[0]);peak=max(peak,rss);rows.append({'pid':int(child),'rss_KiB':rss,'VmHWM':r.get('VmHWM')})
   except OSError:pass
  h.write(json.dumps({'time':time.time(),'inferior':rows,'peak_RSS_KiB':peak})+'\n');h.flush();time.sleep(5)
(B/'resource-summary.json').write_text(json.dumps({'peak_inferior_RSS_KiB':peak},indent=2))
