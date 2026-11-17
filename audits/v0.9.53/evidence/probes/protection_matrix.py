from pathlib import Path
import io,json,tempfile,sys,zipfile,py_compile
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path.insert(0,str(R/'tools/release'))
import check_protected as C
from PyInstaller.archive.writers import CArchiveWriter,ZlibArchiveWriter
out={}
def zipped(entries):
 h=io.BytesIO()
 with zipfile.ZipFile(h,'w') as z:
  for k,v in entries.items():z.writestr(k,v)
 return h.getvalue()
with tempfile.TemporaryDirectory() as td:
 T=Path(td);D=T/'dist';D.mkdir();source=T/'simple.py';source.write_text('VALUE=1\n');py_compile.compile(str(source),cfile=str(T/'simple.pyc'))
 ZlibArchiveWriter(str(T/'clean.pyz'),[])
 ZlibArchiveWriter(str(T/'bad.pyz'),[('ogcore.formulas',str(source),'PYMODULE')],code_dict={'ogcore.formulas':compile(source.read_text(),str(source),'exec')})
 for n in C.PROTECTED:
  p=D/'_internal'/n.replace('.','/');p.parent.mkdir(parents=True,exist_ok=True);p.with_suffix('.so').write_bytes(b'presence-only control; not a valid extension')
 manifest=json.loads((R/'release/manifest.json').read_text())
 def program(name,extra=(),pyz='clean'):
  CArchiveWriter(str(D/name),[('PYZ.pyz',str(T/(pyz+'.pyz')),0,'z'),*extra],'libpython3.12.so.1.0')
 for n in manifest['executables']:program(n)
 first=next(iter(manifest['executables']));out['clean_presence_fixture']=C.check(D)
 for suffix in C.SOURCE_SUFFIXES:
  for prefix in ['_internal/ogcore','_internal/backup/sub/ogcore','_internal/backup/ogcore/__pycache__']:
   p=D/prefix/('formulas'+('.cpython-312' if '__pycache__' in prefix else '')+suffix);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('audit probe');out['path:'+str(p.relative_to(D))]=bool(C.check(D));p.unlink()
 for ext in ['zip','egg','whl']:
  p=D/('_internal/base_library.'+ext);p.write_bytes(zipped({'backup/ogcore/formulas.py':b'audit'}));out['standalone_'+ext]=C.check(D);p.unlink()
 p=D/'_internal/standalone.pyz';p.write_bytes((T/'bad.pyz').read_bytes());out['standalone_pyz']=C.check(D);p.unlink()
 program(first,pyz='bad');out['embedded_PYZ']=C.check(D);program(first)
 for typ in ['m','M','s']:
  program(first,[('ogcore.formulas',str(source if typ=='s' else T/'simple.pyc'),0,typ)]);out['raw_'+typ]=C.check(D);program(first)
 payload=T/'payload.zip';payload.write_bytes(zipped({'ogcore/formulas.py':b'audit'}))
 for typ in ['Z','x']:
  program(first,[('payload.zip',str(payload),0,typ)]);out['embedded_zip_type_'+typ]=C.check(D);program(first)
 inner=zipped({'ogcore/formulas.py':b'audit'});p=D/'_internal/outer.zip';p.write_bytes(zipped({'nested.zip':inner}));out['nested_zip']=C.check(D);p.unlink()
 p=D/'_internal/OGCORE/FORMULAS.PY';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('audit');out['case_variant']=C.check(D);p.unlink()
 owner=T/'owner';extension=T/'licensing.so';extension.write_bytes(b'presence-only control')
 for typ in ['Z','x']:
  CArchiveWriter(str(owner),[('ogcore/licensing.so',str(extension),0,'b'),('payload.zip',str(payload),0,typ)],'libpython3.12.so.1.0');out['owner_embedded_zip_'+typ]=C.check_owner(owner)
 (D/first).write_text('unreadable program');out['unreadable_executable']=C.check(D)
 p=D/'_internal/ogcore/formulas.so';p.unlink();out['missing_extension']=C.check(D)
(B/'protection-matrix-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if not k.startswith('path:')},indent=2));print('suffix/path cases caught',sum(v is True for k,v in out.items() if k.startswith('path:')))
