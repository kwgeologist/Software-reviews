from pathlib import Path
import ast,json,sys,platform,importlib.metadata as md,tkinter
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';records=[];errors=[]
for p in sorted(R.rglob('*.py')):
 s=p.read_text(encoding='utf-8-sig');entry={'file':p.relative_to(R).as_posix(),'lines':len(s.splitlines())}
 try:
  t=ast.parse(s);entry.update(functions=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(t)),classes=sum(isinstance(n,ast.ClassDef) for n in ast.walk(t)))
 except SyntaxError as e:errors.append({'file':entry['file'],'error':str(e)})
 records.append(entry)
out={'original_files':sum(p.is_file() for p in R.rglob('*')),'python_files':len(records),'python_lines':sum(x['lines'] for x in records),'syntax_errors':errors,'test_files':len(list((R/'tests').glob('test_*.py'))),'files':records};(B/'source-inventory.json').write_text(json.dumps(out,indent=2))
versions={}
for n in ['numpy','matplotlib','pyproj','segyio','pyshp','lasio','pytest','Pillow','pypdfium2','cryptography','reportlab']:
 try:versions[n]=md.version(n)
 except md.PackageNotFoundError:versions[n]=None
out={'platform':platform.platform(),'python':sys.version,'executable':sys.executable,'tcl':tkinter.Tcl().eval('info patchlevel'),'versions':versions};(B/'environment.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in json.loads((B/'source-inventory.json').read_text()).items() if k!='files'});print(out)
