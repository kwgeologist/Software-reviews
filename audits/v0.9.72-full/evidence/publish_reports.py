from pathlib import Path
import json,hashlib,shutil,subprocess
B=Path('/workspace/audit-v0.9.72-full');R=Path('/workspace/Software-reviews');O=B/'deliverables';N='OandG_Workbench_v0.9.72_';D=R/'audits/v0.9.72-full'
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],text=True).strip()
S=json.loads((B/'full-serial/final-summary.json').read_text());V=json.loads((B/'bundle-verification.json').read_text());assert S['finished']
assert not git('status','--porcelain'),'Unexpected existing repository changes'
git('fetch','origin','main')
assert git('rev-parse','HEAD')==git('rev-parse','origin/main'),'Review repository advanced; reconcile before publishing'
assert not D.exists(),'Audit destination already exists; inspect before replacing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(O/(N+'Audit_Bundle.zip'))==V['sha256']
D.mkdir(parents=True)
for p in O.iterdir():
 if p.is_file()and(p.name.startswith(N)or p.name in {'README.md','SHA256SUMS.json','bundle-verification.json'}):shutil.copy2(p,D/p.name)
shutil.copytree(B/'bundle-stage/evidence',D/'evidence')
readme=R/'README.md';old=readme.read_text();assert old.startswith('# Software reviews\n')
entry=f'''## O&G Workbench v0.9.72 — Comprehensive pre-v1.0 audit

Read-only audit of **cbc253ccf2793859fa909e9b8521331ddf389f22**. **22 current entries: 1 Critical, 7 High, 8 Medium, 4 Low, 2 Cleanup** — comprising 12 new findings, 3 incomplete earlier corrections and 7 retained Tk investigation/ownership items. Of the 17 original combined-audit regressions, 14 are corrected and 3 remain partial. The original intermittent Tk SIGSEGV remains open.

Independent full serial run: **{S['pytest_terminal']}**, main inferior exit **{S['inferior_exit_code_from_gdb']}**, no native signal observed. Additional isolated Linux compiled-extension checks: **128 passed, 4 skipped, 74 subtests passed**. These are overlapping checks, not additive unique coverage. The received source ZIP matches the expected hash and production checkout; Windows customer EXE/PYD qualification remains unverified. No software changes.

- [Download all reports and evidence in one ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.72-full/{N}Audit_Bundle.zip)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.72-full/{N}Full_Audit.pdf)
- [Read the full audit](audits/v0.9.72-full/{N}Full_Audit.md)
- [Findings CSV](audits/v0.9.72-full/{N}Findings.csv)
- [All 17 previous-finding verification statuses](audits/v0.9.72-full/{N}Previous_Findings_Verification.csv)
- [Evidence, commands and qualification limits](audits/v0.9.72-full/{N}Audit_Evidence.md)

'''
assert not S['native_signals'],'Adapt publication summary to the native-stop evidence before publishing'
readme.write_text('# Software reviews\n\n'+entry+old[len('# Software reviews\n'):].lstrip('\n'))
git('add','--','README.md','audits/v0.9.72-full')
staged=git('diff','--cached','--name-only').splitlines()
assert staged and all(n=='README.md'or n.startswith('audits/v0.9.72-full/')for n in staged)
git('commit','-m','Add read-only comprehensive v0.9.72 audit and complete evidence bundle')
commit=git('rev-parse','HEAD');git('push','origin','HEAD:main');remote=git('ls-remote','origin','refs/heads/main').split()[0];assert remote==commit
blob=subprocess.check_output(['git','-C',str(R),'show',f'HEAD:audits/v0.9.72-full/{N}Audit_Bundle.zip']);assert hashlib.sha256(blob).hexdigest()==V['sha256']
r={'commit':commit,'remote_main':remote,'audit_path':'audits/v0.9.72-full','bundle_sha256':V['sha256'],'staged_file_count':len(staged),'git_status_after':git('status','--porcelain'),'push_verified':True,'bundle_git_blob_matches_verified_archive':True}
(B/'publication.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
