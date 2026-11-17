from pathlib import Path
import subprocess,json,os,time,sys
B=Path('/workspace/audit-v0.9.52');env=os.environ.copy();env.update(DISPLAY=':100',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR='/tmp/audit0952-broad-mpl',APPDATA='/tmp/audit0952-broad-settings',LOCALAPPDATA='/tmp/audit0952-broad-settings')
results=[]
for name in ['own_axis_pay.py', 'own_axis_phih.py', 'multiple_own_axes.py', 'manual_pay_flag.py', 'thin_bed_pay.py', 'coarsest_axis_pay.py', 'late_curve_publication.py', 'preview_zone.py', 'accepted_series.py', 'volumetrics_content.py', 'zone_units.py', 'scientific_references.py', 'grid_reader_publication.py', 'grid_commit_recovery.py', 'grid_unlisted.py', 'grid_creation.py', 'header_transition_matrix.py', 'tests_transition_matrix.py', 'other_editor_transition.py', 'archive_security.py', 'seismic_rename.py', 'image_opacity.py']:
 p=B/'probes'/name
 if not p.exists():continue
 t=time.perf_counter()
 with (B/(p.stem+'.log')).open('w') as h:
  try:r=subprocess.run([sys.executable,str(p)],env=env,stdout=h,stderr=subprocess.STDOUT,timeout=180);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 results.append({'probe':name,'exit_code':code,'seconds':time.perf_counter()-t});(B/'broad-probes.json').write_text(json.dumps(results,indent=2));print(results[-1],flush=True)
