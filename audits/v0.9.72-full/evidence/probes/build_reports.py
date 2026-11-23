from pathlib import Path
import json,csv,collections,shutil,re
B=Path('/workspace/audit-v0.9.72-full');O=B/'deliverables';O.mkdir(exist_ok=True);N='OandG_Workbench_v0.9.72_'
F=json.loads((B/'findings.json').read_text());V=json.loads((B/'previous-findings-verification.json').read_text());rank={'Critical':0,'High':1,'Medium':2,'Low':3,'Cleanup':4};F.sort(key=lambda x:(rank[x['severity']],x['id']));counts=collections.Counter(x['severity']for x in F)
status_file=B/'full-serial/final-summary.json';S=json.loads(status_file.read_text())if status_file.exists()else{'terminal_summary':'IN PROGRESS — not a completed qualification','native_signals':[],'seconds':None,'peak_inferior_RSS_KiB':None,'finished':False}
def write(name,s):(O/(N+name)).write_text(s.strip()+'\n')
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---'for _ in headers)+' |']+['| '+' | '.join(str(x).replace('|','/').replace('\n',' ')for x in r)+' |'for r in rows])
text=r'''
# O&G Workbench v0.9.72 — Comprehensive Pre-v1.0 Audit

Read-only independent full-suite audit. 23 November 2026.

## Executive assessment

**Not ready for commercial v1.0 qualification.** Current source still has actionable correctness, persistence and import defects, and the documented intermittent Tk native crash remains unresolved. The core design does not justify a wholesale rewrite. The safest next release is a focused corrective pass with regression tests, followed by Windows customer-package qualification.

Audited `release/1.0` commit **cbc253ccf2793859fa909e9b8521331ddf389f22**, version **0.9.72**, build marker empty. The received source release ZIP SHA-256 is **41ece88abe5430264e5e3905e4ee1df425cffab10c5a66fe0d2d5ca4edba2b17**, exactly the expected checksum. All production code matches the checkout. Three tracked scanned test images are intentionally export-ignored; the ZIP adds its release manifest. All 977 manifest entries verify, and the shipped verification tool imports every release module and entry point successfully.

This is a **source-release audit**. The supplied archive contains no Windows customer executable or shipped licensing/calculation `.pyd` payload to qualify. Audit-built Linux Cython extensions were independently exercised and hashed; they are not customer Windows artifacts.

No Workbench production code, existing test, version, project dependency or received release was changed. Diagnostic scripts and temporary synthetic projects were separate. No live client project or personal drive was accessed. No v0.9.73 or product release was created. Reports are published only to Software-reviews.

## Main results

The register below contains **COUNT** current entries: COUNTS. Seven are retained Tk investigation/ownership items with their original TK IDs; they are not seven newly proven causes of the original SIGSEGV. Fifteen are current workflow/numerical/reporting findings, including three incomplete corrections from the earlier 17-item audit. Classification and confidence distinguish direct reproductions from hypotheses, supplied crash evidence and qualification gaps.

Of the **17 original combined-audit findings**, **14 are corrected for the original audited regressions** and **3 are incomplete**: FA-002, PI-005 and PI-006. Passing shipped regressions did not detect the independent edge/failure cases that reopened those three. Separate newly exposed paths, such as Geo Save As, are not hidden by declaring the related original Save Project regression corrected.

- FA-002: a realistic shallow upward interval (MD 10000-12000 ft, TVD10000-9990 ft) returns TVD gross0/net10/PhiH2 with no reversal warning, instead of the agreed N/A convention. Source and compiled engines agree on the wrong result.
- PI-005: after a real SQLite lock prevents generation stamping, close succeeds with the old stamp; an older same-generation copy is then accepted silently. Previously committed edits remain durable until the external stale replacement.
- PI-006: after a shape feature commits, a display-refresh exception leaves its draft active; retrying Finish inserts a duplicate. Genuine database-save failure now preserves the draft correctly.
- FA72-001/002: project-owned LIC inputs can be overwritten without consent/backup, and generated LICs discard GROUP identity needed for same-name section round trips.
- FA72-003: Geo Save As snapshots before dirty-form resolution; the original gets the accepted edit but the newly opened copy does not.
- FA72-010: Petro can report a successful save while its newly stored zone definition disagrees with stale published zone values after a swallowed publication failure.

## Test and measurement summary

**Independent full serial run:** SERIAL_RESULT. Runtime/peak memory and the native debugger's inferior result are recorded separately in Audit_Evidence. An interrupted or native-stopped process is never accepted as a pass. This is one full attempt, not a rerun campaign to obtain a green result.

Additional isolated audit-built Linux Cython/Tk9 checks: **128 passed, 4 skipped, 74 subtests passed, exit0**, in47.63s of pytest time (49.45s driver). The four skips require Git metadata absent from that separate build copy; the verified Git checkout's full run includes them. All15 protected modules import as the audit-built `.so` files. Source and compiled shallow-upturn pay probes both fail the expected convention.

Eighteen independent reference checks pass across depth conversion, directional minimum-curvature geometry, Archie saturation, Rw/temperature, depth-time units, manual/grid volumetrics, trend interpolation, bilinear sampling, pay products and production metrics. These controls do not cancel the failing shallow-upturn and production-window counterexamples. No real production forecast/hindcast is claimed.

The112000-well synthetic scale probe measured Map data load0.89s, one-well Map refresh0.17s, Seismic well load0.70s, Geo project/list load1.37s and a full Geo list refresh0.91s, with all112000 rows displayed. Its process high-water RSS was361432KiB. It had **no large LAS/raster library or SEG-Y volume**, and ran while the serial suite was active. It is a bounded favorable result, not proof of complete client-project performance.

## Prior findings: all17 independently revisited

Status means the original named regression and reviewed source paths, not blanket v1.0 or Windows approval. The evidence CSV expands each row.

PRIOR_TABLE

## Current findings register

REGISTER_TABLE

## Data-integrity assessment

The v0.9.71 save-outcome contract is a substantial correction: Seismic, Geosteering, Digitizer, Correlation, Cross Section and Map now preserve the exercised dirty state on database failure or Cancel. Current tests use disposable files, check the old committed value, retry and read stored values from fresh connections. Those are meaningful checks, not merely return-value assertions.

Remaining gaps are at other transaction/acknowledgement boundaries: copying before pending edits are saved; reporting a complete Petro save after a derived-publication savepoint fails; leaving a saved shape draft active when refresh fails; silently failing the close-time generation write; and allowing a second writer of an input LIC outside the user's overwrite option. These need narrow corrections that preserve accepted data and expose partial/uncertain outcomes.

Normal transaction/savepoint tests and forensic recovery controls pass in the isolated target run. Forensic reading leaves the original synthetic files unchanged. That does not prove arbitrary Dropbox replicas, interrupted whole-project folder transfers, drive failures or corrupt customer databases are safe. No client recovery or interpretation reconstruction was attempted. The stale-copy guard must not be presented as fully effective after the demonstrated stamp failure.

## Numerical and geological assessment

The original inverse-depth defect is corrected in the audited reference case: requested TVD1050 on the undulating survey now returns MD2750, which maps back to1050. Conventional pay controls, weighted products, unit conversions, volumetrics and the independent reference matrix behave as documented in the tested cases.

The N/A convention for reversing TVD is explicit and should remain. Its current sampling/tolerance test is incomplete (FA-002), not a reason to invent another geological convention or silently substitute MD. Testing only a steep/coarse undulation misses a shallow but cumulative turn upward. In a second reference case, the same 50-ft-upturn survey is N/A with a 100-ft curve grid but returns numeric net 50 ft with a 0.25-ft grid, demonstrating sampling-dependent validity.

Production first-N windows and non-finite input acceptance have independent counterexamples. Actual cumulative history must remain intact while the time-window predicate is corrected. Existing explicit raw fraction/percent behavior is deliberate; this audit does not reinterpret stored curves by magnitude or mnemonic. Volumetric corner-mean/cell-centre conventions and the explicit feet/metres/TWT conversion contracts should not be redesigned to address unrelated failures.

## LIC import and the supplied apparent-stall screenshot

The intended new UI flow is present: options before parsing, chosen-root image lookup, unresolved duplicate/missing-image choices, Add New/Update/Add-Update, source overwrite consent, per-file savepoints, batch commits and post-commit original-LIC rewriting. The isolated32-test LIC suite passes inside the compiled target run, including a repository Petra-format fixture, cp1252, metre units, DEPTHSHIFT and GROUP variations. No live LIC collection was opened.

Independent edge cases expose input/output aliasing, GROUP round-trip identity, per-batch-only cancellation and misleading post-rollback progress counters. In a synthetic2327-file run, cancellation at begin(2001) still added every file. With a real concurrent write lock there, all327 remaining files were attempted/failed; a10ms probe busy timeout measured4.33s. Multiplying327 by the ordinary5s SQLite timeout gives roughly27minutes of potential waits, **an extrapolation**, not a measured Windows duration. A stalled Tk event pump or slow filesystem step remains another possibility.

The screenshot's2000 completed/current2001 boundary is consistent with the batch transition but does not identify its native stack or prove which writes are durable. The separate unlocked synthetic import completed in about0.93s after0.13s planning, so a deterministic hang at2327 records was not established. The cause of the actual Windows stall remains **unverified**. No customer well names, screenshot data or project databases are bundled.

## Tk, memory and resource assessment

The supplied v0.9.72 results document an intermittent Tk8.6 exit139 in Cross Section. Later supplied full passes do not close it. The independent full serial run's actual outcome is stated above and in the evidence document. Native debugging changes timing; a clean run under it cannot exclude a timing-sensitive fault.

The current source probes reconfirm ten destroyed Geo root graphs and ten Petro root graphs retained through owner traces/listeners. Owner-specific diagnostic removal releases them. Geo startup/poll timers survive destruction while their callback commands are absent. These are confirmed lifecycle states, distinct from a proven original SIGSEGV cause. Repeated-root tests are a stronger exposure than a desktop process simply ending.

The prior focused audit's standalone wrong-thread GC panic has native stacks through Tcl_AsyncDelete/Tkapp_Dealloc on Tk8.6 and9, but with SIGABRT/SIGILL, not the original SIGSEGV. Its800 isolated section cycles cleaned up after main-thread GC; the mixed sequence retained graphs. Those are **prior-baseline** measurements, not newly claimed v0.9.72 figure counts. The current full process has separate RSS records. High-water RSS is not a count of leaked bytes, and pyplot Gcf misses independently embedded figures.

A new small bookkeeping issue keeps completed callback-ID strings in Cross Section's _jobs set until close. It is Cleanup, not evidence of native callback use-after-free. Preserve independent renderers and investigate owner disposal rather than replacing Tk/Matplotlib or suppressing GC as a purported fix.

## Architecture and suite consistency

Shared services already handle depth, identifiers, survey placement, source normalization, pay, cached curves, project paths, themes/icons and save outcomes. The reviewed prior theme/icon cleanup removes the specific reported duplication/dormant Map icon module. Distinct application models/renderers remain appropriate for their workflows. The nominal import cycle between project and sync_safety is resolved through lazy imports and the received source import verification succeeds.

No evidence warrants a whole UI overhaul, framework replacement or module merger. The concrete architectural hazards are ownership and outcome contracts crossing helper boundaries: multiple writers to an LIC path, UI refresh after a durable write, partial derived publication, and close-time generation recording. Centralize those contracts narrowly where necessary, while retaining geological behavior and layouts.

The older single/bulk LIC engines remain tested library/compatibility paths even though the new UI uses lic_import. Their presence alone does not prove dead code. No additional deletion is recommended without a supported-caller check.

## Test coverage assessment

The source inventory covers662 Python files (362 non-test files,186341 non-test lines; the remainder includes tests/helpers). All293 test modules are included in the full serial invocation, collecting3234 main tests. Inventory/AST parsing is not a claim that every function received exhaustive line-by-line manual verification. The review/execution ledger is not a measured line/branch-coverage percentage. The coverage ledger states source paths, workflows, probes, existing tests and remaining limits across14 areas.

Useful tests include genuine SQLite transactions, save/Cancel/retry cycles with fresh reads, identity preservation, compilation/source parity, geometry and numerical references. Weak spots exposed by this audit are specifically missing cross-boundary cases: shallow reversal tolerance, Save As before dirty resolution, refresh after commit, partial publication after accepted-state save, source/output LIC path identity, exported GROUP round trips, cancellation after a batch begins, rolled-back success tallies, corrupt valid JSON and current-schema recovery notes. Tests of nominal booleans or shared-function identity cannot establish those behaviors.

Compiled/source parity establishes equal behavior for exercised inputs, not scientific truth: both engines reproduce FA-002. Skipped Windows, external-data and slow packaged-build checks remain unverified rather than counted as passes. No test was weakened, disabled or edited to accommodate a failure.

## Packaging, security and Windows gaps

The received source ZIP is complete against its manifest and matches the audited production tree. The source packaging/import gates work in the exercised checks. Formula evaluation uses an arithmetic AST allowlist and empty builtins; inspected NumPy archive readers disable pickle. The assistant layer receives a restricted plain context and validated help responses. This audit did not identify a new confirmed arbitrary-code-execution or embedded-private-key defect in those inspected paths; that is not a blanket security certification.

The customer packaging allowlist/protected-module checks are relevant source safeguards, but no v0.9.72 Windows customer folder, `.pyd` binaries or frozen EXE was supplied. This audit's15 Linux extension hashes identify only the audit build. Native Windows DPAPI, locking, DLL/SEG-Y distribution, font/DPI behavior, cold launch, installed-directory permissions and real customer executable persistence/import/export remain qualification gaps. Historical Windows evidence for earlier releases is not recast as current package verification.

## Recommended fix order

1. Preserve/capture the native crash evidence and address demonstrated owner traces/listeners/timers with narrow tests; retain the open SIGSEGV gate until the original mechanism is qualified.
2. Correct handoff-generation failure handling and Geo Save As ordering; test failure/Cancel paths before releasing any UI/model state.
3. Complete FA-002 against actual survey segments and the approved N/A policy, using source and compiled numerical references.
4. Protect input LICs across all writers and preserve GROUP identity; add round-trip/backups tests before batch usability changes.
5. Make Map save acknowledgement independent of redraw success and expose Petro partial-publication failures/staleness.
6. Correct per-file cancellation and reconcile batch progress after rollback; verify the actual Windows stall separately.
7. Correct production window/finite-value handling and metadata/schema messages; keep cumulative history and supported unit conventions intact.
8. Apply contained callback-ID/documentation cleanup where it does not complicate the critical changes.
9. Run the regression plan and one complete serial native-monitored suite after the corrective release, preserving every failed/crashed attempt.
10. Qualify the exact rebuilt Windows customer package separately, including fresh/reopen, failure recovery, source/compiled parity and the frozen executable. No v1.0 approval before the unresolved gates are resolved.

## Safe to leave alone

- Independent Map, Petro, Correlation, Cross Section, Geosteering and Seismic renderers and their module-specific layouts.
- Conventional depth/pay and the explicit raw-value fraction/percent policy where the independent controls pass; fix the demonstrated edge, not the geological convention.
- Lazy Geo-backed Petro loading/unloading, compact Map well arrays and the corrected LAS buffer-accounting service; the bounded scale/cache tests support retaining them.
- Genuine save/Cancel/retry contracts that now retain the original failed-save edits.
- Shared semantic theme/icon tokens and existing namespaced controls; no release-risk budget should be spent on a cosmetic overhaul.
- Intentional legacy migrations/library import APIs with active tests/callers; a large file or old name is not proof of dead code.

## Remaining unverified risks

The original native crash mechanism and Windows customer behavior; the screenshot's exact stalled operation;100000+ wells combined with many actual LAS runs, large raster libraries,200 complex layers and large SEG-Y volumes; arbitrary cloud-sync conflict lineage; full native vendor files absent from tests; installer/distribution execution; and every possible cross-module interleaving. No client-data inference or promise to have discovered every unknown defect is made.

## Detailed findings

DETAILS

## Audit disposition

Read-only audit complete only when the evidence ledger records the final full-run outcome. No corrective implementation is included. The next step is review of these findings together with the existing focused Tk audit, then a narrowly scoped corrective protocol and exact Windows artifact qualification.
'''
if S.get('finished'):
 text=text.replace('Read-only audit complete only when the evidence ledger records the final full-run outcome.', 'Read-only audit complete. The final full-run outcome is recorded in the evidence ledger.')
text=text.replace('COUNT',str(len(F)),1).replace('COUNTS',', '.join(f'{counts[k]} {k}'for k in rank)).replace('SERIAL_RESULT',S['terminal_summary'])
text=text.replace('PRIOR_TABLE',table(['ID','Original severity','Current verification'],[(r['id'],r['original_severity'],r['status'])for r in V]))
text=text.replace('REGISTER_TABLE',table(['ID','Severity','Finding','Classification'],[(r['id'],r['severity'],r['title'],r['classification'])for r in F]))
details=[]
for r in F:
 details+=['### '+r['id']+' — '+r['title'],'',f"Severity: **{r['severity']}**. Classification: {r['classification']}. Confidence: **{r['confidence']}**.",'',f"Files / function: `{r['files']}` — {r['function']}.",'', '**Current behavior and cause:** '+r['cause'],'','**Reproduction:** '+r['repro'],'','**Expected:** '+r['expected'],'','**Observed / why it matters:** '+r['observed'],'','**Evidence:** '+r['evidence'],'','**Recommended correction:** '+r['recommendation'],'','**Regression risks / tests:** '+r['regression_risks'],'','**Release relationship:** '+r['introduced'], '']
text=text.replace('DETAILS','\n'.join(details));write('Full_Audit.md',text)
with (O/(N+'Findings.csv')).open('w',newline='',encoding='utf-8-sig')as f:
 w=csv.DictWriter(f,fieldnames=list(F[0]));w.writeheader();w.writerows(F)
with (O/(N+'Previous_Findings_Verification.csv')).open('w',newline='',encoding='utf-8-sig')as f:
 w=csv.DictWriter(f,fieldnames=list(V[0]));w.writeheader();w.writerows(V)
shutil.copy2(B/'review-coverage.csv',O/(N+'Review_Coverage.csv'))
fix=['# Recommended fixes — v0.9.72 audit only','', 'No fixes were implemented. Keep the original finding IDs and pair each correction with the concrete failing diagnostic, not just the shipped nominal test. Do not combine unrelated rewrites with the corrective release.', '', '## Priority and sequencing','', 'Resolve the native stability gate, data-integrity boundaries and numerical defect first; LIC protection precedes import UX/reporting cleanup. Windows qualification follows the exact rebuilt artifact. The Full Audit gives the practical sequence.', '', '## Corrections and regression risks','']
for r in F:fix+=[f"### {r['id']} ({r['severity']}) — {r['title']}",'',r['recommendation'],'','Regression risks and required controls: '+r['regression_risks'],'']
fix+=['## Changes that are not justified by this audit','', 'No UI overhaul, renderer merger, framework replacement, speculative cache rewrite, schema redesign, inferred fraction conversion or new TVD geological convention. Keep existing save behavior and explicitly surface failures. Correct only demonstrated paths, then qualify the exact customer package.']
write('Recommended_Fixes.md','\n'.join(fix))
plan=['# Regression test plan — v0.9.72 corrective release','', 'Run against a clean disposable checkout/copy with isolated synthetic projects. No client projects. Existing tests remain intact. The diagnostics in this bundle are demonstrations: an exit-zero probe may have collected a failing expected/observed result; turn the intended behavior into an asserting regression before implementing a correction.', '', '## Required behavioral regressions','']
for r in F:plan+=[f"### {r['id']}",'','Trigger: '+r['repro'],'','Assert: '+r['expected'],'','Protect: '+r['regression_risks'],'']
plan+=['## Required verification layers','', '1. Pure independent numerical cases for source and rebuilt protected modules, including realistic absolute MD/TVD, unit changes, shallow upturns, station plateaus and irregular sampling.', '2. Real SQLite transaction/lock/failure-injection tests with fresh connection reads, not only mocks of a success return. Verify partial success is disclosed and stale data is not certified as current.', '3. GUI controls through Cancel/Retry/Discard, dirty Save As, source/output path conflicts and post-commit redraw errors. Verify counts, model state, stored values and dialogs together.', '4. Owner-thread lifecycle and serial GUI stress: weak references for roots/canvases, pending Tcl jobs/commands, subscriptions/traces, workers and memory. Keep independent-process controls separate from long-process qualification.', '5. One complete serial suite on the intended Tk8.6 runtime under native diagnostics, preserving signal/exit/XML/logs; separate Tk9 comparison. Never rerun a crash merely to relabel it green.', '6. Received archive integrity/import checks and actual Windows rebuilt `.pyd` origin/hash parity. The separate audit-built Linux modules do not satisfy this gate.', '7. Disposable Windows customer-executable qualification: cold launch, synthetic project create/import/save/reopen/export, failure/Cancel/retry and long GUI interactions. Use existing production trust; do not patch trust or clock on a working machine.', '', '## Example full-source command','', 'On a disposable Windows audit copy with Git and the exact runtime available:', '', '```powershell', 'py -3.12 -X faulthandler -m pytest -v tests --tb=short -rs --junitxml=D:\\Audit_v0972\\full-results.xml *> D:\\Audit_v0972\\full-tests.log', '```', '', 'Create the output folder first and retain every attempt. Build extensions only in the disposable build copy using the existing build procedure; do not edit tests to force a pass. A source-test result is separate from executing the frozen customer EXE.', '', '## Acceptance','', 'Record exact commit, package SHA-256, runtime and extension origins/hashes, main-test/subtest counts, skips and reasons, time, peak-process memory, native signal and actual process result. No interrupted run is a pass. An original SIGSEGV remains open without evidence supporting its closure; a controlled SIGABRT/SIGILL panic is a distinct finding. Windows/external-data/package skips are outstanding qualification, not successful tests.']
write('Regression_Test_Plan.md','\n'.join(plan))
print('Built report drafts; full run final?',S['finished'],'entries',len(F),dict(counts))
