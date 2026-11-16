from pathlib import Path
import sys,json,tempfile
R=Path('/workspace/audit-v0.9.48/OandG_Workbench_v0.9.48');sys.path.insert(0,str(R/'tools/release'))
import inventory
M=inventory.load_manifest();out={}
with tempfile.TemporaryDirectory() as td:
 D=Path(td)
 for rel in M['required']:
  p=D/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('audit fixture')
 for rel in ['_internal/well symbols.WSD','_internal/petra_well_symbols.WSD','_internal/tests/fixtures/petra_well_symbols.WSD']:
  p=D/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/'tests/fixtures/petra_well_symbols.WSD').read_bytes());result=inventory.scan(D,M);out[rel]={'failures':result['failures'],'warnings':result['warnings']};p.unlink()
Path('/workspace/audit-v0.9.48/wsd-payload-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
