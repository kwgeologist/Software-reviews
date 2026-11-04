from pathlib import Path
import zipfile,hashlib,json
B=Path('/workspace/audit-v0.9.4');Z=Path('/workspace/attachments/a71bf65e-d71e-44c5-bb33-2484e3e4f6f5/OandG_Workbench_v0.9.4.zip');changed=[];missing=[];expected=set()
with zipfile.ZipFile(Z)as a:
 for i in a.infolist():
  if i.is_dir():continue
  p=B/i.filename;expected.add(p)
  if not p.exists():missing.append(i.filename)
  elif p.read_bytes()!=a.read(i):changed.append(i.filename)
root=B/'OandG_Workbench_v0.9.4';extra=[str(p.relative_to(root))for p in root.rglob('*')if p.is_file()and p not in expected];out={'zip_sha256':hashlib.sha256(Z.read_bytes()).hexdigest(),'archive_files':len(expected),'changed':changed,'missing':missing,'extra_source_files':extra,'python_files':sum(p.suffix=='.py'for p in expected),'python_lines':sum(len(p.read_bytes().splitlines())for p in expected if p.suffix=='.py')};(B/'source-integrity.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
