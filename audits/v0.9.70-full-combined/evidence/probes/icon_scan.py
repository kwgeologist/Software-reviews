from pathlib import Path
import ast,sys,json
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path.insert(0,str(C))
from ogcore.icons import ACTIONS,action_key
uses=[];mismatches=[]
for p in C.rglob('*.py'):
 if 'tests'in p.relative_to(C).parts:continue
 for n in ast.walk(ast.parse(p.read_text(encoding='utf-8-sig'))):
  if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='icon_button'and len(n.args)>=3:
   icon,text=n.args[1:3]
   if isinstance(icon,ast.Constant)and isinstance(icon.value,str)and isinstance(text,ast.Constant)and isinstance(text.value,str):
    key=action_key(text.value);r={'file':str(p.relative_to(C)),'line':n.lineno,'text':text.value,'icon':icon.value,'canonical':ACTIONS.get(key)};uses.append(r)
    if key in ACTIONS and ACTIONS[key]!=icon.value:mismatches.append(r)
(B/'icon-consistency.json').write_text(json.dumps({'literal_icon_button_calls':len(uses),'mismatches':mismatches,'uses':uses},indent=2));print(json.dumps({'literal_calls':len(uses),'mismatches':mismatches}))
