from pathlib import Path
import ast,json,collections,hashlib
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');modules=[];funcs=[];issues=[];graph={}
for p in sorted(C.rglob('*.py')):
 rel=str(p.relative_to(C));src=p.read_text(encoding='utf-8-sig');t=ast.parse(src,filename=rel);test=rel.startswith('tests/');name=rel[:-3].replace('/','.');imps=set();counts=collections.Counter();calls=[]
 for n in ast.walk(t):
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
   funcs.append({'file':rel,'function':n.name,'line':n.lineno,'lines':n.end_lineno-n.lineno+1,'test':test})
  if isinstance(n,ast.Import):imps.update(a.name for a in n.names)
  if isinstance(n,ast.ImportFrom):imps.add(n.module or '')
  if isinstance(n,ast.ExceptHandler):
   if n.type is None or isinstance(n.type,ast.Name)and n.type.id in ['Exception','BaseException']:
    counts['broad_except']+=1
    if all(isinstance(x,ast.Pass)for x in n.body):counts['broad_except_pass']+=1
  if isinstance(n,ast.Call):
   try:s=ast.unparse(n.func)
   except:s='?'
   if s in {'eval','exec','os.system','pickle.load','pickle.loads','yaml.load','marshal.load','np.load','numpy.load','tree.tk.eval'} or s.startswith('subprocess.') or s.endswith('.extractall'):calls.append({'line':n.lineno,'call':s})
 graph[name]=sorted(imps);modules.append({'file':rel,'lines':len(src.splitlines()),'test':test,'functions':sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))for n in ast.walk(t)),**dict(counts),'sensitive_calls':calls})
(B/'static-inventory.json').write_text(json.dumps({'modules':modules,'functions':funcs,'imports':graph},indent=2))
print(json.dumps({'python_files':len(modules),'production_files':sum(not x['test']for x in modules),'production_lines':sum(x['lines']for x in modules if not x['test']),'test_lines':sum(x['lines']for x in modules if x['test']),'largest_production_modules':sorted([x for x in modules if not x['test']],key=lambda x:x['lines'],reverse=True)[:12],'broad_except_total':sum(x.get('broad_except',0)for x in modules if not x['test']),'broad_except_pass':sum(x.get('broad_except_pass',0)for x in modules if not x['test'])},indent=2))
