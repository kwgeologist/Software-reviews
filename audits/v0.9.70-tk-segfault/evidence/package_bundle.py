from pathlib import Path
import json,hashlib,shutil,zipfile
B=Path('/workspace/audit-v0.9.70-tk-segfault');O=B/'deliverables';S=B/'bundle-stage';N='OandG_Workbench_v0.9.70_Tk_Segfault_Audit_Bundle'
if S.exists():shutil.rmtree(S)
S.mkdir();E=S/'evidence';E.mkdir()
for p in O.iterdir():
 if p.suffix in ['.md','.csv','.pdf']:shutil.copy2(p,S/p.name)
for p in B.iterdir():
 if p.is_file()and p.suffix in ['.py','.json','.log','.csv','.sh']:shutil.copy2(p,E/p.name)
shutil.copy2('/workspace/attachments/b62839a3-b9ec-43c3-8a1a-e2f9fbdd0968/Pasted text.txt',E/'Audit_Protocol.txt')
shutil.copytree(B/'probes',E/'probes',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for p in (B/'runs').rglob('*'):
 if p.is_file()and p.suffix in ['.json','.jsonl','.xml','.log']and not any(k in p.relative_to(B/'runs').parts for k in ['cache','mpl']):
  target=E/'runs'/p.relative_to(B/'runs');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
shutil.copytree(B/'tk86-extension',E/'tk86-extension',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
(S/'README.md').write_text('''# v0.9.70 focused Tk segmentation-fault audit bundle

Start with OandG_Workbench_v0.9.70_Tk_Segfault_Audit.pdf or its Markdown equivalent. All five required deliverables are at the archive root. The evidence directory contains commands, logs, XML, JSON observations, native traces and external diagnostic probes.

The original SIGSEGV / exit139 remains unresolved. Separate wrong-thread Tcl finalization panics were reproduced; do not treat them as the same crash. No application code, existing tests, project dependencies or releases were changed.

SHA256SUMS.json covers every bundled file except itself. Paths in diagnostic scripts describe the audit machine; adapt copies outside the software checkout before reproducing. Full application source and downloaded tool installations are excluded.
''')
files={str(p.relative_to(S)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(S.rglob('*'))if p.is_file()}
(S/'SHA256SUMS.json').write_text(json.dumps(files,indent=2)+'\n')
z=O/(N+'.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as f:
 for p in sorted(S.rglob('*')):
  if p.is_file():f.write(p,N+'/'+str(p.relative_to(S)))
with zipfile.ZipFile(z)as f:
 assert f.testzip()is None
 manifest=json.loads(f.read(N+'/SHA256SUMS.json'))
 assert all(hashlib.sha256(f.read(N+'/'+n)).hexdigest()==h for n,h in manifest.items())
 required=['Segfault_Audit.md','Crash_Evidence.md','Lifecycle_Findings.csv','Reproduction_Instructions.md','Recommended_Fixes.md']
 assert all(N+'/OandG_Workbench_v0.9.70_Tk_'+n in f.namelist()for n in required)
record={'archive':z.name,'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'bundled_files':len(files)+1,'crc_check':'passed','all_manifest_hashes':'passed','required_deliverables':'5/5'}
(O/'bundle-verification.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
