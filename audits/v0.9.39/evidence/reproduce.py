import argparse,os,sys,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--gui',action='store_true');p.add_argument('--performance',action='store_true');p.add_argument('--size',type=int,default=100000);a=p.parse_args()
src=Path(a.source).resolve();out=Path(a.output).resolve();dest=out/'probes';dest.mkdir(parents=True,exist_ok=True)
for f in (Path(__file__).parent/'probes').glob('*.py'):
 s=f.read_text().replace('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39','__SOURCE__').replace('/workspace/audit-v0.9.39',str(out)).replace('__SOURCE__',str(src));(dest/f.name).write_text(s)
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR=str(out/'mpl'),APPDATA=str(out/'appdata'),LOCALAPPDATA=str(out/'appdata'),XDG_CACHE_HOME=str(out/'cache'))
files=['zone_units.py','seismic_rename.py','image_opacity.py','grid_unlisted.py','output_failures.py','archive_security.py']
if a.gui:files+=['preview_zone.py','accepted_series.py','crosswell_alias.py']
for f in files:subprocess.run([sys.executable,str(dest/f)],env=env,check=True)
if a.performance:subprocess.run([sys.executable,str(dest/'map_complete.py'),str(a.size)],env=env,check=True)
