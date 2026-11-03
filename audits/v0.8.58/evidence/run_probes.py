import argparse,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--gui',action='store_true');a=p.parse_args()
src=Path(a.source).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True);dest=out/'probes';dest.mkdir(exist_ok=True)
for f in (Path(__file__).parent/'probes').glob('*.py'):
 text=f.read_text().replace('/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58','__AUDIT_SOURCE_ROOT__').replace('/workspace/audit-v0.8.58',str(out)).replace('__AUDIT_SOURCE_ROOT__',str(src));(dest/f.name).write_text(text)
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['MPLCONFIGDIR']=str(out/'mpl');env['APPDATA']=str(out/'appdata');env['OGW_RASTER_CACHE']=str(out/'raster');env['OGW_REPOSITORIES']=str(out/'repositories.json')
files=['curves.py','curve_boundaries.py','repository.py','volumetrics.py','geometry_assets.py','science.py','surveys.py','analytical.py']
if a.gui:files+=['fonts.py','scale.py','repeat_rw.py']
for f in files:subprocess.run([sys.executable,str(dest/f)],env=env,check=True)
