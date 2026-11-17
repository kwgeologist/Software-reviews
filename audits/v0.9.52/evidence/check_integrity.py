from pathlib import Path
import zipfile,json,hashlib
B=Path('/workspace/audit-v0.9.52');base=json.loads((B/'baseline.json').read_text());archive=Path(base['archive']);root=B/'OandG_Workbench_v0.9.52'
changed=[];missing=[];expected=set()
with zipfile.ZipFile(archive) as z:
 for i in z.infolist():
  if i.is_dir():continue
  relative=Path(i.filename).relative_to('OandG_Workbench_v0.9.52');expected.add(relative.as_posix());p=root/relative
  if not p.exists():missing.append(str(relative))
  elif p.read_bytes()!=z.read(i):changed.append(str(relative))
extra=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in expected)
result={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'original_files':len(expected),'missing':missing,'changed':changed,'added':extra};(B/'source-integrity.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
