from pathlib import Path
import json,hashlib,subprocess,platform,sys,sqlite3
B=Path('/workspace/audit-v0.9.70-integrity');C=B/'checkout'
before=json.loads((B/'source-hashes.json').read_text());mismatch=[]
for name,h in before.items():
 p=C/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:mismatch.append(name)
archive=Path('/workspace/attachments/cf143bd2-1898-4574-9ff7-99544e4a18d9/OandG_Workbench_v0.9.70.zip')
def git(path,*args):return subprocess.run(['git','-C',str(path),*args],check=True,text=True,capture_output=True).stdout.strip()
r={'source_files_rehashed':len(before),'changed_or_missing':mismatch,'commit':git(C,'rev-parse','HEAD'),'git_status':git(C,'status','--porcelain'),'archive_sha256_after':hashlib.sha256(archive.read_bytes()).hexdigest(),'compare_commit':git('/workspace/audit-v0.9.69-tk/checkout','rev-parse','HEAD'),'compare_git_status':git('/workspace/audit-v0.9.69-tk/checkout','status','--porcelain'),'Software_reviews_commit':git('/workspace/Software-reviews','rev-parse','HEAD'),'Software_reviews_status':git('/workspace/Software-reviews','status','--porcelain'),'python':sys.version,'platform':platform.platform(),'sqlite':sqlite3.sqlite_version}
import numpy,scipy,matplotlib,pytest,tkinter
r['versions']={'numpy':numpy.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,'pytest':pytest.__version__,'Tcl_patchlevel':str(tkinter.Tcl().call('info','patchlevel')),'Tk_major':tkinter.TkVersion}
assert not mismatch and not r['git_status'] and r['archive_sha256_after']==json.loads((B/'baseline.json').read_text())['archive_sha256']
(B/'final-integrity.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
