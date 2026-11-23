from pathlib import Path
import hashlib,json,subprocess
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';A=B/'archive/OandG_Workbench_v0.9.72';P=B/'compiled-probe';Z=Path('/workspace/attachments/3c6cc131-71d0-4b37-9b0b-2630c4baae4c/OandG_Workbench_v0.9.72.zip');before=json.loads((B/'source-hashes.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[n for n,h in before.items()if not(C/n).is_file()or sha(C/n)!=h];copy_changed=[n for n,h in before.items()if(P/n).is_file()and n.endswith('.py')and sha(P/n)!=h];expected='41ece88abe5430264e5e3905e4ee1df425cffab10c5a66fe0d2d5ca4edba2b17'
r={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=C,text=True).strip(),'tracked_files_checked':len(before),'source_or_tests_changed_or_missing':changed,'git_status':subprocess.check_output(['git','status','--porcelain'],cwd=C,text=True),'received_zip_sha256':sha(Z),'expected_zip_sha256':expected,'audit_copy_python_source_changed':copy_changed,'protected_extensions_built_only_in_separate_audit_copy':True,'no_software_commit_or_version_change':True}
assert r['commit']=='cbc253ccf2793859fa909e9b8521331ddf389f22'and not changed and not copy_changed and not r['git_status']and r['received_zip_sha256']==expected
(B/'integrity.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
