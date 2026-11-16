from pathlib import Path
import sys,json,hashlib,ast,importlib.util
B=Path('/workspace/audit-v0.9.48');R=B/'OandG_Workbench_v0.9.48';OLD=Path('/workspace/audit-v0.9.45/OandG_Workbench_v0.9.45');sys.path[:0]=[str(R),str(R/'tools/release')]
import well_symbols as W,cython_modules
from build_help_html import build
from ogcore import __version__
oldwsd=OLD/'well symbols.WSD';fixture=R/'tests/fixtures/petra_well_symbols.WSD';out={'version':__version__,'catalog_count':len(W.BUILTIN_SYMBOLS),'metadata_order_equal':W.load_wsd(oldwsd)==W.BUILTIN_SYMBOLS,'fixture_identical':oldwsd.read_bytes()==fixture.read_bytes(),'protected_source_changed':[m for m in cython_modules.PROTECTED if (OLD/(m.replace('.','/')+'.py')).read_bytes()!=(R/(m.replace('.','/')+'.py')).read_bytes()]}
# Compare actual glyph grammar/rendering function ASTs against the accepted baseline.
def definitions(root):
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse((root/'well_symbols.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=definitions(OLD);b=definitions(R);out['symbol_definitions_changed']=[k for k in a if k in b and a[k]!=b[k]];out['symbol_definitions_removed']=[k for k in a if k not in b]
h=build();(B/'regenerated-help.html').write_text(h);out['generated_help_has_removed_labels']=any(s in h for s in ['Auto-steer','Fit selected segment','Fit to the log']);out['generated_help_version_correct']=f'Workbench {__version__}' in h
(B/'catalog-help-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
