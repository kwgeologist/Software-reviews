from pathlib import Path
import re
O=Path('/workspace/audit-v0.9.70-full/deliverables')
for p in O.glob('*.md'):
 text=p.read_text();parts=re.split(r'(`[^`\n]*`)',text)
 for i in range(0,len(parts),2):
  s=parts[i]
  s=re.sub(r'\b(all|every|in|with|at|of|by|for|from|were|to|including|contains|has|is|and|plus|across|only|before|after)(?=\d)',r'\1 ',s,flags=re.I)
  s=re.sub(r'(?<=\d)(bytes|byte|seconds|MiB|MB|KiB|GB|files|entries|digits|nodes|bbl|Mcf|BOE|scf|ft|datasets|test modules)\b',r' \1',s)
  s=re.sub(r'\b(TVDSS|TVD|MD|N:G|PHIE|SW|BOE|GOR|EUR|span|spacing|scaling)(?=\d)',r'\1 ',s)
  s=s.replace('3.84MB','3.84 MB').replace('in77','in 77').replace('in16','in 16').replace('to1','to 1').replace('all652','all 652')
  parts[i]=s
 p.write_text(''.join(parts))
