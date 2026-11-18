from pathlib import Path
import sys,json,hashlib,types,marshal,pefile
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56';D=R/'dist/OandG_Workbench';S=R/'build/stage/OandG_Workbench_v0.9.56';sys.path[:0]=[str(R/'tools/release'),str(R)]
import check_protected as CP
from PyInstaller.archive.readers import CArchiveReader
manifest=json.loads((R/'release/manifest.json').read_text());out={'customer_protection_problems':CP.tree_problems(D),'modules':[],'executables':[],'stage_comparison':{}}
for n in CP.PROTECTED:
 folder,name=n.rsplit('.',1);files=list((D/'_internal'/folder.replace('.','/')).glob(name+'.*.pyd'));rec={'module':n,'files':[]}
 for p in files:
  pe=pefile.PE(str(p));rec['files'].append({'path':str(p.relative_to(D)),'machine':hex(pe.FILE_HEADER.Machine),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'imports':[x.dll.decode()for x in getattr(pe,'DIRECTORY_ENTRY_IMPORT',[])]});pe.close()
 if len(files)!=1:out['customer_protection_problems'].append(n+': expected exactly one pyd')
 out['modules'].append(rec)
for name in manifest['executables']:
 p=D/(name+'.exe');problems=CP.executable_problems(p);out['customer_protection_problems']+=problems;a=CArchiveReader(str(p));pyz=next((k for k,v in a.toc.items()if v[-1]=='z'),None);z=a.open_embedded_archive(pyz);names=list(z.toc)
 rec={'name':p.name,'carchive_entries':len(a.toc),'pyz_entries':len(names),'owner_or_tests_modules':[n for n in names if n=='license_manager' or n.startswith(('license_manager.','tests.','pytest.'))],'protected_pyz_names':[n for n in names if n in CP.PROTECTED],'source_consistency':{}}
 for module in ['ogcore.userdata','ogcore.licensing_keys','ogcore.__init__']:
  key=module if module in z.toc else module.removesuffix('.__init__')
  if key not in z.toc:continue
  actual=z.extract(key);source=R/(key.replace('.','/')+('/__init__.py' if (R/key.replace('.','/')).is_dir()else'.py'))
  if not source.exists():continue
  expected=compile(source.read_text(encoding='utf-8-sig'),actual.co_filename,'exec',dont_inherit=True,optimize=0)
  def normalize(c):
   if not isinstance(c,types.CodeType):return c
   return (c.co_code,tuple(normalize(x)for x in c.co_consts),c.co_names,c.co_varnames,c.co_argcount,c.co_kwonlyargcount,c.co_flags)
  rec['source_consistency'][key]={'bytecode_and_constants_match':normalize(actual)==normalize(expected),'source':str(source.relative_to(R))}
 out['executables'].append(rec)
 for q in [p,*[D/'_internal'/m['files'][0]['path'].removeprefix('_internal/')for m in out['modules'] if m['files']]]:
  t=S/q.relative_to(D)
  if t.exists():out['stage_comparison'][str(q.relative_to(D))]=hashlib.sha256(q.read_bytes()).digest()==hashlib.sha256(t.read_bytes()).digest()
owner=R/'dist/Owner Tools/O&G Workbench License Manager.exe';out['owner_protection_problems']=CP.check_owner(owner);a=CArchiveReader(str(owner));out['owner_archive_python_dlls']=[n for n in a.toc if n.lower().startswith('python') and n.lower().endswith('.dll')]
(B/'actual-package-assessment.json').write_text(json.dumps(out,indent=2));print('15 modules',len(out['modules']),'protection problems',out['customer_protection_problems'],'owner',out['owner_protection_problems']);print('source consistency',[(r['name'],r['source_consistency'])for r in out['executables']]);print('staged matching',all(out['stage_comparison'].values()))
