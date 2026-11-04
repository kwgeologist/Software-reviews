import argparse,os,sys,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--gui',action='store_true');p.add_argument('--performance',action='store_true');a=p.parse_args()
src=Path(a.source).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True);dest=out/'probes';dest.mkdir(exist_ok=True)
for f in (Path(__file__).parent/'probes').glob('*.py'):
 s=f.read_text().replace('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4','__SOURCE_ROOT__').replace('/workspace/audit-v0.9.4',str(out)).replace('__SOURCE_ROOT__',str(src));s=s.replace('ROOT.parent',f'Path({str(out)!r})').replace('R.parent',f'Path({str(out)!r})');(dest/f.name).write_text(s)
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR=str(out/'mpl'),APPDATA=str(out/'appdata'),LOCALAPPDATA=str(out/'appdata'),OGW_SYMBOL_CATALOG=str(out/'catalog.json'),OGW_REPOSITORIES=str(out/'repositories.json'),OGW_RASTER_CACHE=str(out/'raster'))
files=['boundaries.py','native_edges.py','fault_persistence.py','identity_persistence.py','horizon_app.py','save_failure.py']
if a.gui:files+=['editor.py','rejected_rename.py','map_style.py']
if a.performance:files+=['performance.py']
for f in files:subprocess.run([sys.executable,str(dest/f)],env=env,check=True)
