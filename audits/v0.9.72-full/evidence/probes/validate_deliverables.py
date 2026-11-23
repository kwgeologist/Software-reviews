from pathlib import Path
import json,csv,hashlib,subprocess,zipfile,collections
B=Path('/workspace/audit-v0.9.72-full');O=B/'deliverables';N='OandG_Workbench_v0.9.72_';F=json.loads((B/'findings.json').read_text());S=json.loads((B/'full-serial/final-summary.json').read_text())
assert S['finished']
assert len(F)==22 and len({r['id']for r in F})==22
with (O/(N+'Findings.csv')).open(encoding='utf-8-sig')as h:rows=list(csv.DictReader(h))
assert len(rows)==22 and {r['id']for r in rows}=={r['id']for r in F}
with (O/(N+'Previous_Findings_Verification.csv')).open(encoding='utf-8-sig')as h:previous=list(csv.DictReader(h))
assert len(previous)==17 and sum('Partial'in r['status']for r in previous)==3
with (O/(N+'Review_Coverage.csv')).open(encoding='utf-8-sig')as h:coverage=list(csv.DictReader(h))
assert len(coverage)==14
text=subprocess.check_output(['pdftotext','-layout',str(O/(N+'Full_Audit.pdf')),'-'],text=True)
for f in F:assert f['id']in text,f['id']
assert S['pytest_terminal']in (O/(N+'Audit_Evidence.md')).read_text()
for p in O.glob('*.md'):assert 'IN PROGRESS'not in p.read_text()
assert str(S['counts']['passed'])in text
for p in O.glob('*.md'):assert 'SERIAL_RESULT'not in p.read_text()and'REGISTER_TABLE'not in p.read_text()
assert len(json.loads((B/'source-hashes.json').read_text()))==980
r={'finding_rows':22,'severity_counts':dict(collections.Counter(x['severity']for x in F)),'prior_findings':17,'partial_prior_findings':3,'coverage_areas':14,'all_finding_ids_present_in_PDF':True,'final_test_result_in_evidence':True,'unfinished_placeholders':False,'source_integrity_checked':json.loads((B/'integrity.json').read_text())['tracked_files_checked'],'pdf_bytes':(O/(N+'Full_Audit.pdf')).stat().st_size}
(B/'deliverables-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
