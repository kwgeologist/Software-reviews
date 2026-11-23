from pathlib import Path
import json,hashlib,shutil,zipfile
B=Path('/workspace/audit-v0.9.72-full');O=B/'deliverables';N='OandG_Workbench_v0.9.72_';S=json.loads((B/'full-serial/final-summary.json').read_text());assert S['finished']
root=B/'bundle-stage';shutil.rmtree(root,ignore_errors=True);root.mkdir()
required=[N+x for x in ['Full_Audit.md','Findings.csv','Audit_Evidence.md','Review_Coverage.csv','Recommended_Fixes.md','Regression_Test_Plan.md','Full_Audit.pdf']]
for n in required+[N+'Previous_Findings_Verification.csv']:shutil.copy2(O/n,root/n)
for p in root.glob('*.md'):assert 'IN PROGRESS'not in p.read_text()
e=root/'evidence';e.mkdir()
# Explicit allowlist: no databases, release source, generated C/objects, customer files or tools.
for p in B.iterdir():
 if p.is_file()and p.suffix in {'.json','.jsonl','.log','.csv','.txt','.py'}and p.name not in {'HANDOFF.md','bundle-verification.json'}:
  shutil.copy2(p,e/p.name)
for sub in ['probes','full-serial','compiled-checks','retention','package-checks']:
 for p in (B/sub).rglob('*'):
  if not p.is_file()or p.suffix not in {'.json','.jsonl','.log','.xml','.py'}:continue
  rel=p.relative_to(B/sub)
  if any(x in rel.parts for x in ['cache','mpl','__pycache__']):continue
  dest=e/sub/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
protocol=Path('/workspace/attachments/9caf1f27-399e-4bac-84a8-2d9b93d8d810/Pasted text.txt');shutil.copy2(protocol,e/'Audit_Protocol.txt')
prior=Path('/workspace/Software-reviews/audits/v0.9.70-tk-segfault/evidence');priorout=e/'prior-v0.9.70';priorout.mkdir()
for rel in ['probes/minimal_gc.py','runs/minimal/native-detailed-86.log','runs/minimal/native-detailed-9.log']:
 shutil.copy2(prior/rel,priorout/Path(rel).name)
(priorout/'README.md').write_text('Historical controlled native-panic evidence from v0.9.70 (1e0867f). These are not v0.9.72 full-run crashes and do not establish the original SIGSEGV root cause. See the focused audit at https://github.com/kwgeologist/Software-reviews/tree/main/audits/v0.9.70-tk-segfault .\n')
(root/'README.md').write_text(f'''# O&G Workbench v0.9.72 — Read-only audit bundle

Baseline: `cbc253ccf2793859fa909e9b8521331ddf389f22`, release/1.0.
Received source ZIP SHA-256: `41ece88abe5430264e5e3905e4ee1df425cffab10c5a66fe0d2d5ca4edba2b17`.

Start with `{N}Full_Audit.pdf` or its Markdown version. All seven required standalone reports are included, plus the previous-findings matrix and evidence.

Full serial run: **{S['terminal_summary']}**. Additional compiled Linux target checks: 128 passed, 4 skipped, 74 subtests passed. Counts overlap; do not sum them as unique coverage.

There are 22 current entries: 12 new FA72 items, 3 incomplete earlier corrections, and 7 retained Tk investigation/ownership items. Fourteen of 17 original combined-audit regressions are corrected. The original intermittent Tk SIGSEGV remains open. No Windows customer binaries were supplied for this source-release audit.

No Workbench code, tests, dependency declarations, versions or release artifacts were changed. All data probes use disposable synthetic projects. No client databases, screenshot, credentials, unnecessary application source or product binaries are included.

`evidence/` contains exact commands, logs/XML, source/input hashes, runtime identity, compiled-extension origins, scripts, measurements and reproductions. Historical Tk panic traces are explicitly labelled under `evidence/prior-v0.9.70/`. Scripts record absolute paths on the audit host; adapt environment roots when reproducing. Probe completion is not a claim that the deliberately failing behavior is correct. `SHA256SUMS.json` covers every member except itself.

Published destination: https://github.com/kwgeologist/Software-reviews/tree/main/audits/v0.9.72-full .
''')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={p.relative_to(root).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(root.rglob('*'))if p.is_file()}
(root/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
shutil.copy2(root/'README.md',O/'README.md')
z=O/(N+'Audit_Bundle.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as h:
 for p in sorted(root.rglob('*')):
  if p.is_file():h.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(z)as h:
 assert h.testzip()is None
 names=h.namelist();assert len(names)==len(set(names));assert all(n in names for n in required)
 for n,m in manifest.items():
  data=h.read(n);assert hashlib.sha256(data).hexdigest()==m['sha256']and len(data)==m['bytes']
 assert not any(Path(n).suffix.lower()in {'.sqlite','.db','.exe','.pyd','.so','.tif','.tiff','.png','.lic','.las','.diff'}for n in names)
r={'archive':z.name,'sha256':sha(z),'bytes':z.stat().st_size,'members':len(names),'all_required_reports_present':True,'CRC_check':'pass','member_sha256_checks':len(manifest),'client_databases_or_product_source_included':False}
(B/'bundle-verification.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copy2(B/'bundle-verification.json',O/'bundle-verification.json');shutil.copy2(root/'SHA256SUMS.json',O/'SHA256SUMS.json')
downloads=Path('/workspace/shared/downloads');downloads.mkdir(parents=True,exist_ok=True)
for n in [N+'Audit_Bundle.zip',N+'Full_Audit.pdf']:shutil.copy2(O/n,downloads/n)
print(json.dumps(r,indent=2))
