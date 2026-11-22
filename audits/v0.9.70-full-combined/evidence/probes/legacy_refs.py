from pathlib import Path
import re,json,subprocess,ast
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');files=subprocess.check_output(['git','ls-files','-z'],cwd=C).decode().strip('\0').split('\0');runtime=[];records=[]
for rel in files:
 p=C/rel
 if p.suffix.lower()in ['.py','.json','.spec','.md','.txt','.bat','.iss','.yml']:
  for no,line in enumerate(p.read_text(errors='replace').splitlines(),1):
   if re.search(r'ogmap[./]icons|from\s+ogmap\s+import\s+icons',line):records.append({'file':rel,'line':no,'category':'archived_scan'if rel.startswith('release/records/')else'literal_reference'})
 if p.suffix!='.py':continue
 for n in ast.walk(ast.parse(p.read_text(encoding='utf-8-sig'))):
  hit=isinstance(n,ast.Import)and any(a.name=='ogmap.icons'for a in n.names)
  if isinstance(n,ast.ImportFrom):
   hit=hit or n.module=='ogmap'and any(a.name=='icons'for a in n.names) or rel.startswith('ogmap/')and n.level==1 and (n.module=='icons' or n.module is None and any(a.name=='icons'for a in n.names))
  if hit:runtime.append({'file':rel,'line':n.lineno})
(B/'legacy-icons-reference-scan.json').write_text(json.dumps({'tracked_files_scanned':len(files),'AST_runtime_imports':runtime,'literal_references':records,'scope':'tracked code/build/docs only; archived security records are not callers'},indent=2));print({'runtime_imports':len(runtime),'literal_references':records})
