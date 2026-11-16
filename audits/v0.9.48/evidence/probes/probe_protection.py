from pathlib import Path
import sys,json,tempfile,shutil,py_compile
B=Path('/workspace/audit-v0.9.48');R=B/'OandG_Workbench_v0.9.48'
sys.path.insert(0,str(R/'tools/release'))
import check_protected as C, inventory
from PyInstaller.archive.writers import CArchiveWriter,ZlibArchiveWriter
M=json.loads((R/'release/manifest.json').read_text()); results={}
with tempfile.TemporaryDirectory() as td:
 T=Path(td);D=T/'dist';D.mkdir();s=T/'module.py';s.write_text('VALUE=42\n');py_compile.compile(str(s),cfile=str(T/'module.pyc'))
 empty=T/'empty.pyz';ZlibArchiveWriter(str(empty),[])
 leak=T/'leak.pyz';ZlibArchiveWriter(str(leak),[('ogcore.formulas',str(s),'PYMODULE')],code_dict={'ogcore.formulas':compile(s.read_text(),str(s),'exec')})
 for module in C.PROTECTED:
  p=D/'_internal'/module.replace('.','/');p.parent.mkdir(parents=True,exist_ok=True);p.with_suffix('.so').write_bytes(b'placeholder - tests presence gate only')
 def write_archive(name,kind='empty'):
  entries=[('PYZ.pyz',str(leak if kind=='pyz' else empty),0,'z')]
  if kind=='raw_module':entries.append(('ogcore.formulas',str(T/'module.pyc'),0,'m'))
  if kind=='embedded_source':entries.append(('ogcore/formulas.py',str(s),0,'x'))
  CArchiveWriter(str(D/name),entries,'libpython3.12.so.1.0')
 for n in M['executables']:write_archive(n)
 for rel in M['required']:
  p=D/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('audit fixture')
 results['synthetic_clean']=C.check(D)
 first=next(iter(M['executables']))
 p=D/'_internal/ogcore/formulas.so';p.unlink();results['missing_extension']=C.check(D);p.write_bytes(b'placeholder')
 for suffix in ['.py','.pyx','.c','.cpp','.pyc']:
  p=D/('_internal/ogcore/formulas'+suffix);p.write_text('audit source');results['direct'+suffix]=C.check(D);p.unlink()
 for suffix in ['.py','.pyx','.c','.cpp']:
  p=D/('_internal/backup/ogcore/formulas'+suffix);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('audit source');results['nested'+suffix]={'protection':C.check(D),'inventory':inventory.scan(D,M)['failures']};p.unlink()
 for kind in ['pyz','raw_module','embedded_source']:
  write_archive(first,kind);results[kind]=C.check(D);write_archive(first)
 write_archive('AdditionalWorkbench','pyz');results['additional_bundle']=C.check(D)
(B/'protection-negative-evidence.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
