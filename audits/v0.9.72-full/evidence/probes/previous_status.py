from pathlib import Path
import csv,json
B=Path('/workspace/audit-v0.9.72-full');p=Path('/workspace/Software-reviews/audits/v0.9.70-full-combined/OandG_Workbench_v0.9.70_Combined_Findings.csv')
old=list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
evidence={
'PI-001':'compiled-checks: SeismicInterpretation; inspected close_project/release_interpretation/on_close; save error/conflict Cancel retained, retry/discard tested',
'PI-002':'compiled-checks: GeosteeringJob; dirty saved/project job path and failed autosave Retry/Discard/Cancel tested',
'FA-001':'compiled-checks: TvdToMd; independent MD2750 unique crossing reference; original invalid MD2000 no longer returned',
'FA-002':'shipped coarse-reversal tests pass; independent physically valid shallow-upturn source and compiled probes fail (gross0/net10, no note)',
'FA-003':'compiled-checks: LasCache tests measure unique ndarray owners, eviction/reload/data integrity and shared-buffer accounting; implementation now recurses dataclasses',
'FA-004':'compiled-checks: DigitizerNodes failed-store Cancel/Retry/Discard and exactly-once node persistence; no broad close rewrite',
'PI-003':'compiled-checks: GeoPendingEdits; original Save Project/header and Exit controls pass. Separate Save As path fails (FA72-003)',
'PI-004':'compiled-checks: MissingDatabase; checked open paths and create=False; incomplete manifest/database refused before create',
'PI-005':'compiled-checks: Generations nominal stale/handoff checks pass; independent close-under-write-lock leaves old generation and silently accepts restored stale copy',
'PI-006':'compiled-checks: DrawingFinish database/Cancel/refusal controls pass; independent post-commit refresh failure leaves draft and duplicates feature on retry',
'FA-005':'compiled-checks: EurPerFoot; independent empty-history100000/1000 reference returns100; production-window issue separately FA72-007',
'PI-007':'compiled-checks: CorrelationSession, CrossSectionSave, MapSectionLines; explicit failed-save outcomes and coupled section transactions inspected',
'PI-008':'compiled-checks: ForensicRecovery; independent current-schema forensic read verifies originals unchanged; worker-reader side effects documented',
'PI-009':'compiled-checks: test_v0970_tk_lifecycle passes on Tk9; fixed hint wrapping inspected; original independent Tk SIGSEGV remains separate',
'FA-006':'full source serial Correlation pixel-contract case passes; current font alias/capability assertions inspected and full-suite outcomes logged. No Windows DPI qualification implied',
'FA-007':'compiled-checks: SharedChrome; theme, Petro constants and Correlation/CrossSection ribbon changes use shared semantic tokens',
'FA-008':'compiled-checks: LegacyMapIcons; legacy ogmap/icons.py absent and active canonical icon module retained'
}
rows=[]
for r in old:
 id=r['id'];rows.append({'id':id,'original_severity':r['severity'],'title':r['title'],'status':'Partial / incomplete correction'if id in ['FA-002','PI-005','PI-006']else'Corrected for original audited regression','evidence':evidence[id],'limits':'Native Windows/customer EXE not independently qualified; status is bounded to named source/compiled Linux checks'})
assert len(rows)==17
(B/'previous-findings-verification.json').write_text(json.dumps(rows,indent=2));print('17 prior statuses:14 corrected for original regression,3 partial')
