from pathlib import Path
import json,hashlib,subprocess,platform
B=Path('/workspace/audit-v0.9.70-tk-segfault');C=Path('/workspace/audit-v0.9.70-integrity/checkout');hashes=json.loads(Path('/workspace/audit-v0.9.70-integrity/source-hashes.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mismatch=[n for n,h in hashes.items()if not(C/n).exists()or sha(C/n)!=h]
z=Path('/workspace/attachments/cf143bd2-1898-4574-9ff7-99544e4a18d9/OandG_Workbench_v0.9.70.zip')
r={'checkout':str(C),'commit':subprocess.check_output(['git','-C',str(C),'rev-parse','HEAD'],text=True).strip(),'tracked_files_checked':len(hashes),'changed_or_missing':mismatch,'git_status':subprocess.check_output(['git','-C',str(C),'status','--porcelain'],text=True),'source_zip_sha256':sha(z),'source_zip_expected':'a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797','historical_checkout_status':subprocess.check_output(['git','-C','/workspace/audit-v0.9.69-tk/checkout','status','--porcelain'],text=True)}
assert not mismatch and not r['git_status'] and r['source_zip_sha256']==r['source_zip_expected']
(B/'input-integrity.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
