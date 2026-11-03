import zipfile,hashlib,json
from pathlib import Path
z=Path('/workspace/attachments/571b397d-05ec-4281-9569-f54346e685fe/OandG_Workbench_v0.8.58.zip');root=Path('/workspace/audit-v0.8.58');changed=[];missing=[];files=[]
with zipfile.ZipFile(z) as a:
 for i in a.infolist():
  if i.is_dir():continue
  p=root/i.filename;files.append(p)
  if not p.exists():missing.append(i.filename)
  elif hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(a.read(i)).digest():changed.append(i.filename)
source=root/'OandG_Workbench_v0.8.58';expected=set(files);extra=[str(p.relative_to(source))for p in source.rglob('*')if p.is_file() and p not in expected]
out={'archive_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_files':len(files),'changed':changed,'missing':missing,'extra_source_files':extra,'python_files':sum(p.suffix=='.py' for p in files),'python_lines':sum(len(p.read_bytes().splitlines())for p in files if p.suffix=='.py')}
(root/'source-integrity.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
