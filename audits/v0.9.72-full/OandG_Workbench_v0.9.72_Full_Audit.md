# O&G Workbench v0.9.72 — Comprehensive Pre-v1.0 Audit

Read-only independent full-suite audit. 23 November 2026.

## Executive assessment

**Not ready for commercial v1.0 qualification.** Current source still has actionable correctness, persistence and import defects, and the documented intermittent Tk native crash remains unresolved. The core design does not justify a wholesale rewrite. The safest next release is a focused corrective pass with regression tests, followed by Windows customer-package qualification.

Audited `release/1.0` commit **cbc253ccf2793859fa909e9b8521331ddf389f22**, version **0.9.72**, build marker empty. The received source release ZIP SHA-256 is **41ece88abe5430264e5e3905e4ee1df425cffab10c5a66fe0d2d5ca4edba2b17**, exactly the expected checksum. All production code matches the checkout. Three tracked scanned test images are intentionally export-ignored; the ZIP adds its release manifest. All 977 manifest entries verify, and the shipped verification tool imports every release module and entry point successfully.

This is a **source-release audit**. The supplied archive contains no Windows customer executable or shipped licensing/calculation `.pyd` payload to qualify. Audit-built Linux Cython extensions were independently exercised and hashed; they are not customer Windows artifacts.

No Workbench production code, existing test, version, project dependency or received release was changed. Diagnostic scripts and temporary synthetic projects were separate. No live client project or personal drive was accessed. No v0.9.73 or product release was created. Reports are published only to Software-reviews.

## Main results

The register below contains **22** current entries: 1 Critical, 7 High, 8 Medium, 4 Low, 2 Cleanup. Seven are retained Tk investigation/ownership items with their original TK IDs; they are not seven newly proven causes of the original SIGSEGV. Fifteen are current workflow/numerical/reporting findings, including three incomplete corrections from the earlier 17-item audit. Classification and confidence distinguish direct reproductions from hypotheses, supplied crash evidence and qualification gaps.

Of the **17 original combined-audit findings**, **14 are corrected for the original audited regressions** and **3 are incomplete**: FA-002, PI-005 and PI-006. Passing shipped regressions did not detect the independent edge/failure cases that reopened those three. Separate newly exposed paths, such as Geo Save As, are not hidden by declaring the related original Save Project regression corrected.

- FA-002: a realistic shallow upward interval (MD 10,000–12,000 ft, TVD 10,000–9,990 ft) returns TVD gross 0 / net 10 / PhiH 2 with no reversal warning, instead of the agreed N/A convention. Source and compiled engines agree on the wrong result.
- PI-005: after a real SQLite lock prevents generation stamping, close succeeds with the old stamp; an older same-generation copy is then accepted silently. Previously committed edits remain durable until the external stale replacement.
- PI-006: after a shape feature commits, a display-refresh exception leaves its draft active; retrying Finish inserts a duplicate. Genuine database-save failure now preserves the draft correctly.
- FA72-001/002: project-owned LIC inputs can be overwritten without consent/backup, and generated LICs discard GROUP identity needed for same-name section round trips.
- FA72-003: Geo Save As snapshots before dirty-form resolution; the original gets the accepted edit but the newly opened copy does not.
- FA72-010: Petro can report a successful save while its newly stored zone definition disagrees with stale published zone values after a swallowed publication failure.

## Test and measurement summary

**Independent full serial run:** 3224 passed, 10 skipped, 365 warnings, 1214 subtests passed in 4231.52s (1:10:31); inferior exit 0; gdb exit 0. Runtime/peak memory and the native debugger's inferior result are recorded separately in Audit_Evidence. An interrupted or native-stopped process is never accepted as a pass. This is one full attempt, not a rerun campaign to obtain a green result.

The main test count reconciles to all 3,234 collected cases. Pytest time: 4231.52 s; driver time: 4260.91 s. Peak main-inferior RSS: 6,887,200 KiB (6.57 GiB). This is process high-water memory, not a measured leak. Individual skip reasons are listed in the evidence report.

Additional isolated audit-built Linux Cython / Tk 9 checks: **128 passed, 4 skipped, 74 subtests passed, exit 0**, in 47.63 s of pytest time (49.45 s driver). The four skips require Git metadata absent from that separate build copy; the verified Git checkout's full run includes them. All 15 protected modules import as the audit-built `.so` files. Source and compiled shallow-upturn pay probes both fail the expected convention.

Eighteen independent reference checks pass across depth conversion, directional minimum-curvature geometry, Archie saturation, Rw/temperature, depth-time units, manual/grid volumetrics, trend interpolation, bilinear sampling, pay products and production metrics. These controls do not cancel the failing shallow-upturn and production-window counterexamples. No real production forecast/hindcast is claimed.

The 112,000-well synthetic scale probe measured Map data load 0.89 s, one-well Map refresh 0.17 s, Seismic well load 0.70 s, Geo project/list load 1.37 s and a full Geo list refresh 0.91 s, with all 112,000 rows displayed. Its process high-water RSS was 361,432 KiB. It had **no large LAS/raster library or SEG-Y volume**, and ran while the serial suite was active. It is a bounded favorable result, not proof of complete client-project performance.

## Prior findings: all 17 independently revisited

Status means the original named regression and reviewed source paths, not blanket v1.0 or Windows approval. The evidence CSV expands each row.

| ID | Original severity | Current verification |
| --- | --- | --- |
| PI-001 | Critical | Corrected for original audited regression |
| PI-002 | Critical | Corrected for original audited regression |
| FA-001 | High | Corrected for original audited regression |
| FA-002 | High | Partial / incomplete correction |
| FA-003 | High | Corrected for original audited regression |
| FA-004 | High | Corrected for original audited regression |
| PI-003 | High | Corrected for original audited regression |
| PI-004 | High | Corrected for original audited regression |
| PI-005 | High | Partial / incomplete correction |
| PI-006 | High | Partial / incomplete correction |
| FA-005 | Medium | Corrected for original audited regression |
| PI-007 | Medium | Corrected for original audited regression |
| PI-008 | Medium | Corrected for original audited regression |
| PI-009 | Medium | Corrected for original audited regression |
| FA-006 | Low | Corrected for original audited regression |
| FA-007 | Cleanup | Corrected for original audited regression |
| FA-008 | Cleanup | Corrected for original audited regression |

## Current findings register

| ID | Severity | Finding | Classification |
| --- | --- | --- | --- |
| TK-01 | Critical | Intermittent Tk SIGSEGV remains an open release-stability gate | Supplied native crash evidence; original root cause unresolved |
| FA-002 | High | Shallow TVD reversals still escape the N/A pay convention | Confirmed incomplete correction of earlier FA-002 |
| FA72-001 | High | Overwrite No does not protect an imported project-owned LIC | Confirmed code defect |
| FA72-003 | High | Geo Save As copies before pending form edits are saved | Confirmed code defect |
| PI-005 | High | A failed close-generation write silently leaves stale-copy protection ineffective | Confirmed incomplete correction of earlier PI-005 |
| TK-02 | High | Destroyed Geo roots remain strongly owned by traces and selection subscriptions | Confirmed retention on exercised path; possible native-crash contributor |
| TK-03 | High | Petro search trace retains destroyed application roots | Confirmed retention on exercised path; possible contributor |
| TK-04 | High | Wrong-thread finalization remains a demonstrated native Tcl failure class | Confirmed root cause of controlled panic only; original link unresolved |
| FA72-002 | Medium | Generated LICs lose Petra GROUP identity and fail same-name section round trips | Confirmed code defect |
| FA72-006 | Medium | LIC Cancel is checked only between 1,000-file write batches | Confirmed code defect; screenshot cause remains unverified |
| FA72-007 | Medium | First-N-month production includes adjustments before first production | Confirmed code defect |
| FA72-010 | Medium | Petro successful-save reporting hides stale published zone results | Confirmed code defect |
| PI-006 | Medium | Post-commit Map refresh failure leaves a saved shape draft that duplicates on retry | Confirmed remaining failure path related to earlier PI-006 |
| TK-05 | Medium | Geo destruction leaves startup and poll timers naming deleted Tcl commands | Confirmed stale callback state; possible contributor |
| TK-06 | Medium | Repeated-root fixtures amplify lifecycle state left by earlier modules | Strongly supported amplification hypothesis |
| TK-07 | Medium | Embedded figure ownership still needs sequence-level qualification | Possible contributing factor; not a confirmed native library defect |
| FA72-004 | Low | Valid JSON with malformed generation fields escapes project-open error handling | Confirmed code defect |
| FA72-005 | Low | Recovery Access labels its own current schema as a newer application version | Confirmed code defect |
| FA72-008 | Low | Production import accepts non-finite volumes as successful numeric data | Confirmed code defect |
| FA72-012 | Low | LIC progress claims success for a whole batch that rolled back | Confirmed UI reporting defect |
| FA72-009 | Cleanup | Cross Section retains IDs of completed scheduled callbacks until close | Confirmed code defect |
| FA72-011 | Cleanup | Current crash report incorrectly says Cross Section code is unchanged since v0.9.61 | Confirmed documentation defect |

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

Independent edge cases expose input/output aliasing, GROUP round-trip identity, per-batch-only cancellation and misleading post-rollback progress counters. In a synthetic 2,327-file run, cancellation at begin(2001) still added every file. With a real concurrent write lock there, all 327 remaining files were attempted/failed; a 10 ms probe busy timeout measured 4.33 s. Multiplying327 by the ordinary 5 s SQLite timeout gives roughly 27 minutes of potential waits, **an extrapolation**, not a measured Windows duration. A stalled Tk event pump or slow filesystem step remains another possibility.

The screenshot's2000 completed/current2001 boundary is consistent with the batch transition but does not identify its native stack or prove which writes are durable. The separate unlocked synthetic import completed in about 0.93 s after 0.13 s planning, so a deterministic hang at2327 records was not established. The cause of the actual Windows stall remains **unverified**. No customer well names, screenshot data or project databases are bundled.

## Tk, memory and resource assessment

The supplied v0.9.72 results document an intermittent Tk 8.6 exit 139 in Cross Section. Later supplied full passes do not close it. The independent full serial run's actual outcome is stated above and in the evidence document. Native debugging changes timing; a clean run under it cannot exclude a timing-sensitive fault.

The current source probes reconfirm ten destroyed Geo root graphs and ten Petro root graphs retained through owner traces/listeners. Owner-specific diagnostic removal releases them. Geo startup/poll timers survive destruction while their callback commands are absent. These are confirmed lifecycle states, distinct from a proven original SIGSEGV cause. Repeated-root tests are a stronger exposure than a desktop process simply ending.

The prior focused audit's standalone wrong-thread GC panic has native stacks through Tcl_AsyncDelete/Tkapp_Dealloc on Tk 8.6 and9, but with SIGABRT/SIGILL, not the original SIGSEGV. Its800 isolated section cycles cleaned up after main-thread GC; the mixed sequence retained graphs. Those are **prior-baseline** measurements, not newly claimed v0.9.72 figure counts. The current full process has separate RSS records. High-water RSS is not a count of leaked bytes, and pyplot Gcf misses independently embedded figures.

A new small bookkeeping issue keeps completed callback-ID strings in Cross Section's _jobs set until close. It is Cleanup, not evidence of native callback use-after-free. Preserve independent renderers and investigate owner disposal rather than replacing Tk/Matplotlib or suppressing GC as a purported fix.

## Architecture and suite consistency

Shared services already handle depth, identifiers, survey placement, source normalization, pay, cached curves, project paths, themes/icons and save outcomes. The reviewed prior theme/icon cleanup removes the specific reported duplication/dormant Map icon module. Distinct application models/renderers remain appropriate for their workflows. The nominal import cycle between project and sync_safety is resolved through lazy imports and the received source import verification succeeds.

No evidence warrants a whole UI overhaul, framework replacement or module merger. The concrete architectural hazards are ownership and outcome contracts crossing helper boundaries: multiple writers to an LIC path, UI refresh after a durable write, partial derived publication, and close-time generation recording. Centralize those contracts narrowly where necessary, while retaining geological behavior and layouts.

The older single/bulk LIC engines remain tested library/compatibility paths even though the new UI uses lic_import. Their presence alone does not prove dead code. No additional deletion is recommended without a supported-caller check.

## Test coverage assessment

The source inventory covers 662 Python files (362 non-test files, 186,341 non-test lines; the remainder includes tests/helpers). All 293 test modules are included in the full serial invocation, collecting 3,234 main tests. Inventory/AST parsing is not a claim that every function received exhaustive line-by-line manual verification. The review/execution ledger is not a measured line/branch-coverage percentage. The coverage ledger states source paths, workflows, probes, existing tests and remaining limits across 14 areas.

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

### TK-01 — Intermittent Tk SIGSEGV remains an open release-stability gate

Severity: **Critical**. Classification: Supplied native crash evidence; original root cause unresolved. Confidence: **High for supplied open crash; Low for exact root cause**.

Files / function: `docs/v0.9.72/LIC_Import_Test_Results.md:11-37; tests/test_xsection.py:1866-1920` — Tk update during Cross Section reopen.

**Current behavior and cause:** The supplied current release report records an exit 139 fault in Tk 8.6 during the settings reopen test. No native root cause has been established. A passing later run does not close the fault.

**Reproduction:** Use the original full order/runtime and a native debugger. This audit independently runs the complete available source suite once under gdb; see final Audit_Evidence for its actual outcome.

**Expected:** Long GUI sessions complete without native fault; closure rests on a captured/understood reproducer, not selected green reruns.

**Observed / why it matters:** Supplied v0.9.72 evidence: Tk 8.6 run1 crashed, then Tk 9 and Tk 8.6 passed. Those are author-supplied results, separate from this audit run. The original cause remains unresolved.

**Evidence:** full-serial/pytest-native.log; docs/v0.9.72/LIC_Import_Test_Results.md; prior focused Tk audit

**Recommended correction:** Capture the native fault and correct the demonstrated owner/thread lifecycle path. Preserve traces and test order. Do not label the issue fixed merely because this audit run or a targeted run passes.

**Regression risks / tests:** Windows impact and frozen executable behavior are unverified; do not presume a Linux Tcl panic is the same SIGSEGV.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### FA-002 — Shallow TVD reversals still escape the N/A pay convention

Severity: **High**. Classification: Confirmed incomplete correction of earlier FA-002. Confidence: **High**.

Files / function: `ogcore/pay.py:192-211,246-274; ogcore/batch_zones.py:907-928` — tvd_rises_through; summarize.

**Current behavior and cause:** The allowed negative difference is proportional to absolute TVD and applied separately to every grid step. At TVD 10,000 ft the per-step allowance is about 0.01 ft; a cumulative 10-ft rise spread over 2,000 samples passes. A finite grid also is not a proof over survey stations.

**Reproduction:** Run probes/numerical_reference.py: MD 10,000–12,000, TVD 10000-9990, all samples pay. Repeat using the audit-built compiled pay extension.

**Expected:** Any genuinely upward/reversing TVD interval follows the stated convention: TVD gross/net/N:G/products N/A, MD interval separate. Conventional controls unchanged.

**Observed / why it matters:** Gross 0 ft, net 10 ft, PhiH 2 ft, empty warning; MD interval 2000 ft. Same result from compiled extension. A second physically identical 50-ft-upturn survey is correctly N/A with 100-ft sample spacing but wrongly numeric net50 with 0.25-ft spacing.

**Evidence:** numerical-reference.json; compiled-origins.json; numerical-breadth.json

**Recommended correction:** Check actual MD-ordered survey segments and use an appropriate absolute tolerance against cumulative reversal, not an allowance multiplied by grid resolution. Preserve the agreed N/A convention.

**Regression risks / tests:** Nearly horizontal wells, unit scaling, plateaus, sparse/irregular stations, and conventional-well results need independent reference tests; do not introduce MD substitution.

**Release relationship:** Exposed in v0.9.72; pre-existing

### FA72-001 — Overwrite No does not protect an imported project-owned LIC

Severity: **High**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `ograster/lic_import.py:541-567; database.py:4098-4168` — execute; sync_raster_lic.

**Current behavior and cause:** Project LIC synchronization always runs for small successful imports before the optional original-LIC rewrite path. When the input is that same project LIC, it is rewritten directly regardless of overwrite_lic.

**Reproduction:** Run probes/lic_edges.py: import a log, edit its generated project LIC calibration and add a harmless extra metadata line, reimport that file with overwrite_lic=False.

**Expected:** The selected input LIC remains byte-for-byte unchanged when No is chosen, or an explicit conflict is disclosed before modifying it.

**Observed / why it matters:** Input changed; extra line lost; no backup; lic_rewritten=False; no warning note. Registration update itself succeeds.

**Evidence:** lic-edge-results.json; lic-edge-results.log

**Recommended correction:** Detect input/output path identity and stage/skip project-LIC synchronization or require explicit consent/backup. Enforce input preservation across every writer, not only rewrite_lic_image.

**Regression risks / tests:** Project LIC paths, same-file aliases, automatic synchronization, permission failures and imported calibration must retain existing behavior.

**Release relationship:** Introduced/exposed by v0.9.72 import flow

### FA72-003 — Geo Save As copies before pending form edits are saved

Severity: **High**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `geoworkbench/main_window.py:922-953; ogcore/project.py:598-616` — save_project_as; copy_project.

**Current behavior and cause:** The snapshot/copy is made from committed DB data first. load_project then asks to save the original dirty form, so the saved edit is missing from the copy already created.

**Reproduction:** Run probes/save_as.py with the existing synthetic GeoPendingEdits fixture. Set well name Edited Draft, Save As, answer Yes to the save question.

**Expected:** The saved-as project contains the edits the user agreed to save, or Save As clearly refuses until they are resolved.

**Observed / why it matters:** Original stores Edited Draft; the newly opened copy stores Tab Well. The original retains the edit; the new copy is stale.

**Evidence:** save-as-results.json; save-as-results.log

**Recommended correction:** Resolve/save pending editors before taking the copy and honor failures/Cancel. Copy a coherent accepted application state, not a pre-prompt DB snapshot.

**Regression risks / tests:** Do not create/open an unintended partial copy after cancellation or save failure; test header, tab and child-editor edits and original/copy identities.

**Release relationship:** Exposed in v0.9.72; pre-existing

### PI-005 — A failed close-generation write silently leaves stale-copy protection ineffective

Severity: **High**. Classification: Confirmed incomplete correction of earlier PI-005. Confidence: **High**.

Files / function: `database.py:1739-1757; ogcore/sync_safety.py:144-169,374-395` — ProjectDatabase.close; on_close; new_generation.

**Current behavior and cause:** Generation stamping is an extra close-time transaction. A SQLite write lock makes it fail; close catches/logs the error and closes normally with the previous generation and handoff still valid.

**Reproduction:** Run probes/sync_edges.py: commit a well edit, hold BEGIN IMMEDIATE on another connection, shorten the probe busy timeout to 50ms, close the Workbench DB, release lock, then restore the earlier same-generation copy.

**Expected:** A failed handoff-generation step is surfaced and cannot certify the changed/older copy as current. Previously committed edits remain durable.

**Observed / why it matters:** Close returns normally; the committed edit exists, but generation remains 1. Replacing it with the older generation-1 file produces no stale/handoff warning. No immediate SQLite loss is alleged.

**Evidence:** sync-edge-results.json; sync-edge-results.log

**Recommended correction:** Treat generation/handoff failure as an explicit incomplete close/publication outcome. Ensure a changed project cannot retain a matching old verification record, and require retry or a clear unverified state.

**Regression risks / tests:** Multi-module connections on one PC, busy timeout, WAL checkpoint failure, concurrent close and crash recovery; preserve committed data and explicit Open Anyway semantics.

**Release relationship:** Exposed in v0.9.72; pre-existing

### TK-02 — Destroyed Geo roots remain strongly owned by traces and selection subscriptions

Severity: **High**. Classification: Confirmed retention on exercised path; possible native-crash contributor. Confidence: **High for retention; Low for SIGSEGV causality**.

Files / function: `geoworkbench/main_window.py:174,383,2671-2681; geoworkbench/common.py:97-126; ogcore/well_selection.py:41-56` — Geo destruction; DepthEditTracker.

**Current behavior and cause:** Raw destroy bypasses normal listener cleanup and variable trace callbacks retain the owner graph. Normal close removes the listener but does not prove every trace graph is released.

**Reproduction:** Run probes/ownership_probe.py on v0.9.72: ten raw root destruction cycles, main-thread GC, then separate diagnostic listener/search/all-owner-trace removal controls.

**Expected:** Disposed owners are releasable on their owner thread; fixtures do not carry obsolete roots into unrelated tests.

**Observed / why it matters:** Ten destroyed roots/listeners remain; removing listeners or search traces alone is insufficient; removing the remaining210 variable traces releases all ten. Diagnostic cleanup changes only disposable probe objects.

**Evidence:** retention/ownership_probe.py.log

**Recommended correction:** Own each trace/subscription token and provide idempotent disposal for supported destruction paths. Do not blanket-delete all variable traces in production.

**Regression risks / tests:** Normal close versus raw destroy, worker lifetime and fixture teardown; no proof this causes original SIGSEGV or leaks client processes after they exit.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### TK-03 — Petro search trace retains destroyed application roots

Severity: **High**. Classification: Confirmed retention on exercised path; possible contributor. Confidence: **High for retention; Low for SIGSEGV causality**.

Files / function: `petroworkbench/app.py:387-395,460-488` — API search trace; Petro destruction.

**Current behavior and cause:** The variable trace retains a bound owner method after raw destruction.

**Reproduction:** Run probes/petro_retention.py: ten raw destroy/GC cycles and diagnostic owner trace cleanup.

**Expected:** No linear retention of disposed root graphs across repeated GUI lifecycle tests.

**Observed / why it matters:** Ten roots retained; removing ten trace commands releases all ten (16320 objects collected).

**Evidence:** retention/petro_retention.py.log

**Recommended correction:** Retain/remove the search trace token in owner disposal and exercise all termination paths.

**Regression risks / tests:** Do not lose search/filter state or infer Windows customer memory leakage from a raw-destroy test alone.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### TK-04 — Wrong-thread finalization remains a demonstrated native Tcl failure class

Severity: **High**. Classification: Confirmed root cause of controlled panic only; original link unresolved. Confidence: **High for controlled native failure; Low for link to SIGSEGV**.

Files / function: `CPython _tkinter Tkapp_Dealloc; Tcl_AsyncDelete; tests/conftest.py:116-133` — Finalization of cyclic Tk-owning graphs.

**Current behavior and cause:** The earlier isolated same-runtime probe proves a destroyed root cycle collected on a worker can panic Tcl without Workbench or Matplotlib. Existing main-thread fixture collection cannot collect graphs still strongly rooted by traces.

**Reproduction:** Use the prior focused audit minimal_gc.py in disposable subprocesses; compare owner-thread collection with deliberate worker collection/allocation. This is a controlled negative test, not the original application crash.

**Expected:** Application owners are deterministically disposed on their owning thread; workers hold plain data.

**Observed / why it matters:** Prior native stacks: Tk 8.6.16 SIGABRT through Tcl_AsyncDelete/Tkapp_Dealloc; Tk 9.0.4 SIGILL panic trap. Main controls pass. Neither signal is the reported SIGSEGV / exit 139.

**Evidence:** prior focused Tk native traces; runtime-Tk86.json; runtime-Tk9.json

**Recommended correction:** Release Tk-containing graphs deterministically on their owner thread; keep the existing fixture guard as mitigation, not closure.

**Regression risks / tests:** No global GC disabling; do not substitute this controlled panic for original SIGSEGV reproduction. The v0.9.72 application trigger remains unproved.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### FA72-002 — Generated LICs lose Petra GROUP identity and fail same-name section round trips

Severity: **Medium**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `database.py:4144-4155; ogcore/raster.py:327-340; ograster/lic_import.py:335-359` — sync_raster_lic; write_lic; _match.

**Current behavior and cause:** lic_section stores GROUP identity, but sync_raster_lic omits the group argument when exporting. Both sections become GROUP 0; ambiguous name matching runs before the exact own-lic_path fallback.

**Reproduction:** Run group_roundtrip in probes/lic_edges.py: same well/image/name GR, GROUP 1 and GROUP 2, export automatic project LICs and plan their reimport.

**Expected:** Section identity survives save/export/reimport, and each own LIC resolves to its known registration.

**Observed / why it matters:** Stored sections 1|gr and 2|gr export as groups 0 and 0. Both own LICs fail with two registrations could be this control file.

**Evidence:** lic-edge-results.json

**Recommended correction:** Preserve the stored GROUP metadata in project LIC output; ensure exact identity is not lost behind an ambiguous fallback.

**Regression risks / tests:** Older registrations without lic_section, renamed logs, multiple sections with identical labels and moved images.

**Release relationship:** Introduced/exposed by v0.9.72 GROUP-aware identity

### FA72-006 — LIC Cancel is checked only between 1,000-file write batches

Severity: **Medium**. Classification: Confirmed code defect; screenshot cause remains unverified. Confidence: **High**.

Files / function: `ograster/lic_import.py:509-539; ogcore/task_progress.py:cancel,pump` — execute.

**Current behavior and cause:** Cancellation is tested at batch entry, not inside its per-file loop, so Cancel cannot stop after the current file. A last-batch request may never be reflected in report.cancelled.

**Reproduction:** Run probes/lic_cancel_batch.py with 2,327 synthetic LICs; request cancellation at begin(2001), with and without a concurrent SQLite writer.

**Expected:** Finish/rollback the current file safely, stop before the next file and report unprocessed files accurately.

**Observed / why it matters:** Unlocked: all 2327 added, cancelled count 0. Locked with 10ms probe busy timeout: first 2000 stored, all remaining 327 attempted/failed over 4.33s, cancelled count 0.

**Evidence:** lic-batch-cancel.json; lic-batch-cancel.log

**Recommended correction:** Check cancellation at each safe per-file boundary inside the batch; commit only completed items consistently and count remaining work. Distinguish database waits from parsing and UI refresh.

**Regression risks / tests:** Do not abort an active file halfway, lose completed imports, rewrite LICs for rolled-back items, or misreport skipped versus cancelled records.

**Release relationship:** Introduced by v0.9.72 execute path

### FA72-007 — First-N-month production includes adjustments before first production

Severity: **Medium**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `ogcore/production.py:371-386` — summarize.

**Current behavior and cause:** The window predicate is m < n and lacks m >= 0, although offsets are relative to the first producing month. Negative-volume adjustments before that month are included in first-N totals.

**Reproduction:** Run probes/production_edges.py: Dec2019 -100 bbl, Jan2020 200, Feb100, Mar100, same source.

**Expected:** First production Jan2020; first 3 months Jan-Mar total 400. Overall cumulative may correctly include all history and equal 300.

**Observed / why it matters:** first_month is Jan2020 but first3_oil is 300, including the preceding December correction.

**Evidence:** production-edge-results.json

**Recommended correction:** Constrain the first-N window to 0 <= month_offset < N while leaving actual cumulative history unchanged.

**Regression risks / tests:** Reported zeros, pre-production adjustments, gaps, source priority and incomplete histories; do not discard legitimate corrections globally.

**Release relationship:** Exposed in v0.9.72; pre-existing

### FA72-010 — Petro successful-save reporting hides stale published zone results

Severity: **Medium**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `petroworkbench/geo_link.py:504-534; petroworkbench/workspace.py:730-751` — _save_geo_workspace; save_project.

**Current behavior and cause:** Zone publication failure rolls back its savepoint but is logged and swallowed; the accepted Petro state commits and save_project reports True with no partial-save warning.

**Reproduction:** Run probes/petro_partial_publish.py: save a 60ft zone, extend base to5520 for80ft, inject an OperationalError only in publish_zone_values, save.

**Expected:** Surface the partial publication failure and prevent old map/Geo zone values from appearing current for the newly accepted state.

**Observed / why it matters:** Stored zone base5520; published gross remains60 rather than80; save returnsTrue; no error/warning dialog; last_zone_refusals empty. Raw state survives.

**Evidence:** petro-partial-publish.json; petro-partial-publish.log

**Recommended correction:** Propagate/record partial-publication status, retain a reliable retry and show stale/uncertain published results explicitly. Preserve accepted curve data while making the inconsistency visible.

**Regression risks / tests:** Do not discard accepted raw curves, overwrite another producer, or turn a recoverable publication failure into silent data loss.

**Release relationship:** Exposed in v0.9.72; pre-existing

### PI-006 — Post-commit Map refresh failure leaves a saved shape draft that duplicates on retry

Severity: **Medium**. Classification: Confirmed remaining failure path related to earlier PI-006. Confidence: **High**.

Files / function: `ogmap/drawing_tab.py:403-440,441-471; ogmap/project.py:404-429` — DrawingsTab._into_shape_layer; finish.

**Current behavior and cause:** The feature commits, then refresh_layers runs before _into_shape_layer returns success and finish clears the draft. A refresh exception preserves the already-saved draft.

**Reproduction:** Run probes/map_postcommit.py: draw into a real temporary polygon layer, inject an exception only in refresh_layers, then retry Finish after refresh recovers.

**Expected:** Once committed, the draft is acknowledged exactly once; a display failure does not invite repeating the insert.

**Observed / why it matters:** One feature is stored after the exception; state remains draw with 3 vertices. Retry stores a second identical feature. Original database-write failure controls are corrected.

**Evidence:** map-postcommit.json; map-postcommit.log

**Recommended correction:** Separate committed-save acknowledgement from optional UI refresh; end the saved draft before refreshing and offer redraw retry without reinsertion.

**Regression risks / tests:** Keep drafts on genuine save failure/Cancel, and preserve undo/redo and active-shape-layer behavior.

**Release relationship:** Exposed in v0.9.72; pre-existing

### TK-05 — Geo destruction leaves startup and poll timers naming deleted Tcl commands

Severity: **Medium**. Classification: Confirmed stale callback state; possible contributor. Confidence: **High for stale callbacks; Low for native causality**.

Files / function: `geoworkbench/main_window.py:171-175,2671-2681` — startup_project; _poll_requests.

**Current behavior and cause:** Owner timers are not explicitly cancelled before destruction deletes their callback commands.

**Reproduction:** Run probes/timer_probe.py: destroy a disposable Geo root, then inspect Tcl after info and info commands directly.

**Expected:** No queued callbacks reference deleted owner commands after disposal.

**Observed / why it matters:** Two timers remain, startup_project and _poll_requests; both script_command_exists flags are false. No native fault is inferred.

**Evidence:** timer-probe.log

**Recommended correction:** Store/cancel owner job IDs before command destruction and prevent rescheduling after disposal.

**Regression risks / tests:** Startup delay, polling, unexpected close and parent/child cancellation ordering.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### TK-06 — Repeated-root fixtures amplify lifecycle state left by earlier modules

Severity: **Medium**. Classification: Strongly supported amplification hypothesis. Confidence: **Medium**.

Files / function: `tests/test_xsection.py:977-1010,1717-1755,2202-2221; tests/conftest.py:92-133` — WindowTests; PunchListWindowTests; GeoCrossSectionTests.

**Current behavior and cause:** Tests repeatedly create roots, pump update and use raw destruction; strong graphs can outlive their fixture despite owner-thread GC. This differs from a desktop process ending on close.

**Reproduction:** Compare the recorded fresh, ordered and long-process runs in the focused audit and this full serial run; inspect the direct teardown calls and current retention controls.

**Expected:** Fixtures have explicit owner/worker/callback cleanup and serial stress remains meaningful.

**Observed / why it matters:** Current ten-cycle probes confirm retained roots. Test-order/finalization timing is a supported amplification hypothesis; no proof identifies this as the original SIGSEGV trigger.

**Evidence:** retention logs; full-serial log; prior focused audit A-D logs

**Recommended correction:** Correct owner cleanup, assert weak-reference/callback baselines and keep a long serial stress job; subprocess isolation can contain independent groups but cannot prove a product fix.

**Regression risks / tests:** Do not hide failures by weakening tests or replacing serial qualification with only isolated runs.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### TK-07 — Embedded figure ownership still needs sequence-level qualification

Severity: **Medium**. Classification: Possible contributing factor; not a confirmed native library defect. Confidence: **Medium for ownership risk; Low for SIGSEGV cause**.

Files / function: `xsection/window.py:96-164,1649-1670; Matplotlib _backend_tk.py` — Embedded canvas lifecycle; raster idle processing.

**Current behavior and cause:** Embedded figures are not all tracked by pyplot Gcf. Long GUI processes can retain graphs through owners, and nested idle pumping changes finalization timing. No native Matplotlib fault was proved.

**Reproduction:** Use actual Figure/canvas weak references and owner cleanup checks under the full GUI sequence, not only pyplot.close/Gcf.

**Expected:** Owner/canvas/job counts return to defined baselines after close and owner-thread collection.

**Observed / why it matters:** Earlier focused audit:800 isolated section cycles ended with zero retained sections/Figures after GC; mixed sequence retained many graphs. Current full-run memory is recorded separately; it is not a new figure-count measurement.

**Evidence:** prior focused Tk lifecycle/sequence evidence; full-serial resource logs; section-job-results.json

**Recommended correction:** Trace retained owners before changing canvas integration; qualify idle draw, toolbar, bindings and close during raster preparation on both toolkit versions.

**Regression risks / tests:** Keep renderers independent; high-water RSS alone is not proof of a leak, and no evidence supports blaming a library by name alone.

**Release relationship:** Carried from focused v0.9.70 Tk audit; status rechecked for v0.9.72

### FA72-004 — Valid JSON with malformed generation fields escapes project-open error handling

Severity: **Low**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `ogcore/sync_safety.py:285-318; ogcore/project_ui.py:open_checked` — problems; open_checked.

**Current behavior and cause:** JSON syntax/type at the top level is checked, but generation_seq is converted with int without validating its value. The raw ValueError is outside the ProjectError handlers.

**Reproduction:** Run malformed_handoff in probes/sync_edges.py with generation_seq set to corrupt-but-valid-json.

**Expected:** Treat malformed metadata as an unverified copy with an actionable warning and safe explicit-open path.

**Observed / why it matters:** Raw ValueError escapes rather than returning an UnverifiedProjectCopy problem. Project data is not modified by this failure.

**Evidence:** sync-edge-results.json

**Recommended correction:** Validate handoff/accepted-record field types and ranges; convert failures into the existing unverified-copy contract.

**Regression risks / tests:** Corrupt valid JSON, missing/negative/oversized fields and old handoff formats; do not silently accept an invalid record.

**Release relationship:** Exposed in v0.9.72; pre-existing

### FA72-005 — Recovery Access labels its own current schema as a newer application version

Severity: **Low**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `ogcore/recovery.py:33,283-294; database.py:31` — KNOWN_SCHEMA; ReadOnlyProject.notes.

**Current behavior and cause:** Recovery KNOWN_SCHEMA remains 29 while the application supports/writes schema 31.

**Reproduction:** Create/open a current synthetic database using Recovery Access and read notes (probes/sync_edges.py).

**Expected:** Current schema is recognized; genuine newer schemas retain the conservative warning.

**Observed / why it matters:** A current v0.9.72 schema-31 project is said to be from a newer version. Reading remains possible and forensic originals are unchanged.

**Evidence:** sync-edge-results.json

**Recommended correction:** Share a dependency-light schema version constant or keep a guarded consistency check so recovery and database metadata cannot drift.

**Regression risks / tests:** Maintain recovery independence from normal migrating/writing database import paths and older/newer schema safety.

**Release relationship:** Exposed in v0.9.72; pre-existing

### FA72-008 — Production import accepts non-finite volumes as successful numeric data

Severity: **Low**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `ogcore/production.py:175-186,292-298,813-824` — number; _clean; import_rows.

**Current behavior and cause:** float conversions accept infinity/overflow and no finite-value validation or problem is recorded before storage.

**Reproduction:** Run nonfinite_import in probes/production_edges.py with oil=1e999.

**Expected:** Reject/report invalid non-finite volumes without treating them as a measured monthly quantity.

**Observed / why it matters:** One row added, no problems, stored oil Infinity and cumulative oil Infinity.

**Evidence:** production-edge-results.json

**Recommended correction:** Validate finite numeric inputs and conversion results and report the offending row/column; keep missing data distinct from invalid values.

**Regression risks / tests:** Existing null markers, legitimate negative adjustments, large finite volumes and update/replace transaction semantics.

**Release relationship:** Exposed in v0.9.72; pre-existing

### FA72-012 — LIC progress claims success for a whole batch that rolled back

Severity: **Low**. Classification: Confirmed UI reporting defect. Confidence: **High**.

Files / function: `ograster/lic_import.py:519-539; ogcore/task_progress.py:251-255,393-430` — execute; ProgressWindow.finish.

**Current behavior and cause:** Per-file success counters are incremented before the batch commits and are not reconciled after a commit failure. The detailed Report correctly marks errors, but the visible tally remains successful.

**Reproduction:** Run probes/lic_commit_progress.py with two files, a real ProgressWindow and a failing commit wrapper.

**Expected:** Final success/failure tallies and heading reflect committed outcomes consistently with the detailed report.

**Observed / why it matters:** Zero database rows; Report has0 added/2 errors, but the visible tally says Succeeded2 Failed0 and heading Completed. The detailed summary does disclose the two errors.

**Evidence:** lic-commit-progress.json; lic-commit-progress.log

**Recommended correction:** Reconcile progress counters after batch commit/rollback and label completion with errors accurately; distinguish provisional processed work from durable additions.

**Regression risks / tests:** Keep per-file savepoints, summary details and partial-batch cancellation accounting consistent.

**Release relationship:** Introduced by v0.9.72 write-batch progress flow

### FA72-009 — Cross Section retains IDs of completed scheduled callbacks until close

Severity: **Cleanup**. Classification: Confirmed code defect. Confidence: **High**.

Files / function: `xsection/window.py:96-102,143-158` — later; _destroyed.

**Current behavior and cause:** later adds every after/idle ID to _jobs but successful callbacks never remove their completed IDs. Destruction eventually clears the history.

**Reproduction:** Run probes/section_jobs.py: schedule/drain 1000 no-op callbacks in one real synthetic Cross Section window.

**Expected:** The active-job collection tracks pending jobs rather than growing with historical completed work.

**Observed / why it matters:** All 1000 callbacks complete, _jobs grows from 5 to1005 while only one Tcl callback remains pending. This retains strings, not the callback function graphs.

**Evidence:** section-job-results.json

**Recommended correction:** Remove each completed job ID in an owner-safe wrapper/finally, preserving cancellation and disposal checks.

**Regression risks / tests:** Cancelled, failed and nested callbacks and close ordering; no evidence ties this bookkeeping issue to SIGSEGV.

**Release relationship:** Exposed in v0.9.72; pre-existing

### FA72-011 — Current crash report incorrectly says Cross Section code is unchanged since v0.9.61

Severity: **Cleanup**. Classification: Confirmed documentation defect. Confidence: **High**.

Files / function: `docs/v0.9.72/LIC_Import_Test_Results.md:30-31; xsection/window.py` — Release evidence statement.

**Current behavior and cause:** The report extends a no-change assertion to Cross Section code, although commits in v0.9.62, v0.9.65 and v0.9.71 changed the window.

**Reproduction:** Compare git log/diff for xsection/window.py; commit4a92878 changes persistence/close paths.

**Expected:** Version-change statements distinguish unchanged tests from product paths actually changed.

**Observed / why it matters:** The current report says tests and Cross Section code unchanged since61. The v0.9.71 product delta disproves the latter; no causal crash regression is inferred.

**Evidence:** source-change-ledger.json; baseline Git history

**Recommended correction:** Correct the evidence statement and retain an exact changed-file/commit ledger.

**Regression risks / tests:** Keep original crash evidence and clearly label historical versus current test/code revisions.

**Release relationship:** Introduced/exposed in v0.9.72 test-results document


## Audit disposition

Read-only audit complete. The final full-run outcome is recorded in the evidence ledger. No corrective implementation is included. The next step is review of these findings together with the existing focused Tk audit, then a narrowly scoped corrective protocol and exact Windows artifact qualification.
