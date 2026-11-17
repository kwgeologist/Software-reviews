import sys,json,tempfile
from pathlib import Path
from unittest.mock import patch
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path.insert(0,str(R))
from database import ProjectDatabase
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'p.ogwdb';a=ProjectDatabase(p);w=a.add_well('Well','');a.set_formation_top(w,'A',100,source='XON');a.set_formation_top(w,'B',1000,source='XON');ids={n:a.top_definition(n)[0] for n in ['A','B']};b=ProjectDatabase(p);events=[];real=a._alias_owner
 def interleave(alias):
  result=real(alias)
  b.add_top_alias(ids['B'],alias);events.append({'after_B_add_returned':'success','alias_owner':b.canonical_top_name(alias)})
  return result
 with patch.object(a,'_alias_owner',side_effect=interleave):a.add_top_alias(ids['A'],'Shared legacy')
 events.append({'after_A_add_returned':'success','alias_owner':a.canonical_top_name('Shared legacy')})
 out={'interleaving':'A checks alias owner; B adds and commits alias; A completes using its earlier check','events':events,'final_aliases':a.top_aliases()};a.close();b.close()
(B/'alias-concurrency-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
