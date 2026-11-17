from pathlib import Path
import sys,json,ast
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';OLD=Path('/workspace/audit-v0.9.45/OandG_Workbench_v0.9.45');sys.path[:0]=[str(R),str(R/'tools/release')]
import well_symbols as W,cython_modules
from build_help_html import build
from ogcore import __version__
fixture=R/'tests/fixtures/petra_well_symbols.WSD'
out={'version':__version__,'catalog_count':len(W.BUILTIN_SYMBOLS),'fixture_metadata_order_equal':W.load_wsd(fixture)==W.BUILTIN_SYMBOLS,'protected_modules':list(cython_modules.PROTECTED),'historical_context_only':True}
def definitions(root):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse((root/'well_symbols.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=definitions(OLD);b=definitions(R);out['glyph_definitions_changed_vs_historical']=[k for k in a if k in b and a[k]!=b[k] and any(x in k.lower() for x in ['glyph','draw','path','symbol'])]
h=build();(B/'regenerated-help.html').write_text(h);out['help_removed_control_labels_found']=[s for s in ['Auto-steer','Fit selected segment','Fit to the log'] if s in h];out['help_version_correct']=f'Workbench {__version__}' in h
out['staged_wsd']=[str(p.relative_to(B/'staged-payload')) for p in (B/'staged-payload').rglob('*') if p.is_file() and p.suffix.casefold()=='.wsd']
(B/'catalog-help-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
