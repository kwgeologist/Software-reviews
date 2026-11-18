from pathlib import Path
import sys,json,hashlib,zipfile,io
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56';D=R/'dist/OandG_Workbench';sys.path.insert(0,str(R/'tools/release'))
from cython_modules import PROTECTED
original=json.loads((B/'original-files.json').read_text())['files'];known={};paths=[]
for n in PROTECTED:
 rel=n.replace('.','/');folder,stem=rel.rsplit('/',1)
 for path,h in original.items():
  if path==rel+'.py' or path.startswith('build/cython/')and path.endswith('/'+rel+'.c') or path.startswith(folder+'/__pycache__/'+stem+'.')and path.endswith('.pyc'):
   known[h]=n+':'+path;paths.append(path)
raw_hits=[];normalized_hits=[];zip_hits=[];normalized={}
for path in paths:
 p=R/path
 if p.suffix in ['.py','.c']:
  normalized[hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()]=path
for p in D.rglob('*'):
 if not p.is_file():continue
 rel=str(p.relative_to(D));h=original['dist/OandG_Workbench/'+rel]
 if h in known:raw_hits.append({'path':rel,'matches':known[h]})
 if p.stat().st_size<32*1024*1024:
  data=p.read_bytes();h=hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
  if h in normalized:normalized_hits.append({'path':rel,'matches':normalized[h]})
 if p.suffix.lower()in['.zip','.egg','.whl']:
  with zipfile.ZipFile(p)as z:
   for info in z.infolist():
    if info.is_dir():continue
    data=z.read(info);h=hashlib.sha256(data).hexdigest()
    if h in known:zip_hits.append({'archive':rel,'member':info.filename,'matches':known[h]})
out={'source_bytecode_generated_C_reference_files':len(paths),'exact_source_or_bytecode_hits':raw_hits,'newline_normalized_source_hits':normalized_hits,'zip_member_hits':zip_hits,'scope':'actual loose customer files and ZIP members; separate checker covered CArchive/PYZ names and nested archives'};(B/'exact-copy-scan-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
