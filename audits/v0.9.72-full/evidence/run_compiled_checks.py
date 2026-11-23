from pathlib import Path
import subprocess,os,json,time
B=Path('/workspace/audit-v0.9.72-full');C=B/'compiled-probe';R=B/'compiled-checks';R.mkdir(exist_ok=True);x=subprocess.Popen(['/workspace/audit-v0.9.68-full/xserver/root/usr/bin/Xvfb',':244','-screen','0','1600x1000x24','-nolisten','tcp'],stdout=(R/'xvfb.log').open('w'),stderr=subprocess.STDOUT);time.sleep(.3);env=os.environ.copy();env.update(DISPLAY=':244',PYTHONPATH='/workspace/audit-v0.9.68-full/deps',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR=str(R/'mpl'),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
cmd=['/workspace/audit-v0.9.56-windows/tooling/bin/python','-X','faulthandler','-m','pytest','-q','-p','no:cacheprovider','tests/test_cython_build.py','tests/test_v0971_persistence.py','tests/test_v0971_integrity.py','tests/test_v0971_numerics.py','tests/test_v0971_cleanup.py','tests/test_v0971_packaging.py','tests/test_v0972_lic_import.py','tests/test_batch_zones.py','tests/test_v0970_tk_lifecycle.py','--tb=short','-rs',f'--junitxml={R}/results.xml'];d={'command':cmd,'cwd':str(C),'Tk':'9.0.4','start':time.time(),'note':'isolated audit-built Linux extensions, not customer Windows binaries'};(R/'command.json').write_text(json.dumps(d,indent=2))
try:
 with (R/'pytest.log').open('w')as h:p=subprocess.run(cmd,cwd=C,env=env,stdout=h,stderr=subprocess.STDOUT)
 d.update(exit_code=p.returncode,seconds=time.time()-d['start']);(R/'status.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2))
finally:x.terminate();x.wait()
