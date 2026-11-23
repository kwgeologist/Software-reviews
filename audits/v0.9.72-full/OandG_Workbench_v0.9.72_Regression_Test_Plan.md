# Regression test plan — v0.9.72 corrective release

Run against a clean disposable checkout/copy with isolated synthetic projects. No client projects. Existing tests remain intact. The diagnostics in this bundle are demonstrations: an exit-zero probe may have collected a failing expected/observed result; turn the intended behavior into an asserting regression before implementing a correction.

## Required behavioral regressions

### TK-01

Trigger: Use the original full order/runtime and a native debugger. This audit independently runs the complete available source suite once under gdb; see final Audit_Evidence for its actual outcome.

Assert: Long GUI sessions complete without native fault; closure rests on a captured/understood reproducer, not selected green reruns.

Protect: Windows impact and frozen executable behavior are unverified; do not presume a Linux Tcl panic is the same SIGSEGV.

### FA-002

Trigger: Run probes/numerical_reference.py: MD 10,000–12,000, TVD 10000-9990, all samples pay. Repeat using the audit-built compiled pay extension.

Assert: Any genuinely upward/reversing TVD interval follows the stated convention: TVD gross/net/N:G/products N/A, MD interval separate. Conventional controls unchanged.

Protect: Nearly horizontal wells, unit scaling, plateaus, sparse/irregular stations, and conventional-well results need independent reference tests; do not introduce MD substitution.

### FA72-001

Trigger: Run probes/lic_edges.py: import a log, edit its generated project LIC calibration and add a harmless extra metadata line, reimport that file with overwrite_lic=False.

Assert: The selected input LIC remains byte-for-byte unchanged when No is chosen, or an explicit conflict is disclosed before modifying it.

Protect: Project LIC paths, same-file aliases, automatic synchronization, permission failures and imported calibration must retain existing behavior.

### FA72-003

Trigger: Run probes/save_as.py with the existing synthetic GeoPendingEdits fixture. Set well name Edited Draft, Save As, answer Yes to the save question.

Assert: The saved-as project contains the edits the user agreed to save, or Save As clearly refuses until they are resolved.

Protect: Do not create/open an unintended partial copy after cancellation or save failure; test header, tab and child-editor edits and original/copy identities.

### PI-005

Trigger: Run probes/sync_edges.py: commit a well edit, hold BEGIN IMMEDIATE on another connection, shorten the probe busy timeout to 50ms, close the Workbench DB, release lock, then restore the earlier same-generation copy.

Assert: A failed handoff-generation step is surfaced and cannot certify the changed/older copy as current. Previously committed edits remain durable.

Protect: Multi-module connections on one PC, busy timeout, WAL checkpoint failure, concurrent close and crash recovery; preserve committed data and explicit Open Anyway semantics.

### TK-02

Trigger: Run probes/ownership_probe.py on v0.9.72: ten raw root destruction cycles, main-thread GC, then separate diagnostic listener/search/all-owner-trace removal controls.

Assert: Disposed owners are releasable on their owner thread; fixtures do not carry obsolete roots into unrelated tests.

Protect: Normal close versus raw destroy, worker lifetime and fixture teardown; no proof this causes original SIGSEGV or leaks client processes after they exit.

### TK-03

Trigger: Run probes/petro_retention.py: ten raw destroy/GC cycles and diagnostic owner trace cleanup.

Assert: No linear retention of disposed root graphs across repeated GUI lifecycle tests.

Protect: Do not lose search/filter state or infer Windows customer memory leakage from a raw-destroy test alone.

### TK-04

Trigger: Use the prior focused audit minimal_gc.py in disposable subprocesses; compare owner-thread collection with deliberate worker collection/allocation. This is a controlled negative test, not the original application crash.

Assert: Application owners are deterministically disposed on their owning thread; workers hold plain data.

Protect: No global GC disabling; do not substitute this controlled panic for original SIGSEGV reproduction. The v0.9.72 application trigger remains unproved.

### FA72-002

Trigger: Run group_roundtrip in probes/lic_edges.py: same well/image/name GR, GROUP 1 and GROUP 2, export automatic project LICs and plan their reimport.

Assert: Section identity survives save/export/reimport, and each own LIC resolves to its known registration.

Protect: Older registrations without lic_section, renamed logs, multiple sections with identical labels and moved images.

### FA72-006

Trigger: Run probes/lic_cancel_batch.py with 2,327 synthetic LICs; request cancellation at begin(2001), with and without a concurrent SQLite writer.

Assert: Finish/rollback the current file safely, stop before the next file and report unprocessed files accurately.

Protect: Do not abort an active file halfway, lose completed imports, rewrite LICs for rolled-back items, or misreport skipped versus cancelled records.

### FA72-007

Trigger: Run probes/production_edges.py: Dec2019 -100 bbl, Jan2020 200, Feb100, Mar100, same source.

Assert: First production Jan2020; first 3 months Jan-Mar total 400. Overall cumulative may correctly include all history and equal 300.

Protect: Reported zeros, pre-production adjustments, gaps, source priority and incomplete histories; do not discard legitimate corrections globally.

### FA72-010

Trigger: Run probes/petro_partial_publish.py: save a 60ft zone, extend base to5520 for80ft, inject an OperationalError only in publish_zone_values, save.

Assert: Surface the partial publication failure and prevent old map/Geo zone values from appearing current for the newly accepted state.

Protect: Do not discard accepted raw curves, overwrite another producer, or turn a recoverable publication failure into silent data loss.

### PI-006

Trigger: Run probes/map_postcommit.py: draw into a real temporary polygon layer, inject an exception only in refresh_layers, then retry Finish after refresh recovers.

Assert: Once committed, the draft is acknowledged exactly once; a display failure does not invite repeating the insert.

Protect: Keep drafts on genuine save failure/Cancel, and preserve undo/redo and active-shape-layer behavior.

### TK-05

Trigger: Run probes/timer_probe.py: destroy a disposable Geo root, then inspect Tcl after info and info commands directly.

Assert: No queued callbacks reference deleted owner commands after disposal.

Protect: Startup delay, polling, unexpected close and parent/child cancellation ordering.

### TK-06

Trigger: Compare the recorded fresh, ordered and long-process runs in the focused audit and this full serial run; inspect the direct teardown calls and current retention controls.

Assert: Fixtures have explicit owner/worker/callback cleanup and serial stress remains meaningful.

Protect: Do not hide failures by weakening tests or replacing serial qualification with only isolated runs.

### TK-07

Trigger: Use actual Figure/canvas weak references and owner cleanup checks under the full GUI sequence, not only pyplot.close/Gcf.

Assert: Owner/canvas/job counts return to defined baselines after close and owner-thread collection.

Protect: Keep renderers independent; high-water RSS alone is not proof of a leak, and no evidence supports blaming a library by name alone.

### FA72-004

Trigger: Run malformed_handoff in probes/sync_edges.py with generation_seq set to corrupt-but-valid-json.

Assert: Treat malformed metadata as an unverified copy with an actionable warning and safe explicit-open path.

Protect: Corrupt valid JSON, missing/negative/oversized fields and old handoff formats; do not silently accept an invalid record.

### FA72-005

Trigger: Create/open a current synthetic database using Recovery Access and read notes (probes/sync_edges.py).

Assert: Current schema is recognized; genuine newer schemas retain the conservative warning.

Protect: Maintain recovery independence from normal migrating/writing database import paths and older/newer schema safety.

### FA72-008

Trigger: Run nonfinite_import in probes/production_edges.py with oil=1e999.

Assert: Reject/report invalid non-finite volumes without treating them as a measured monthly quantity.

Protect: Existing null markers, legitimate negative adjustments, large finite volumes and update/replace transaction semantics.

### FA72-012

Trigger: Run probes/lic_commit_progress.py with two files, a real ProgressWindow and a failing commit wrapper.

Assert: Final success/failure tallies and heading reflect committed outcomes consistently with the detailed report.

Protect: Keep per-file savepoints, summary details and partial-batch cancellation accounting consistent.

### FA72-009

Trigger: Run probes/section_jobs.py: schedule/drain 1000 no-op callbacks in one real synthetic Cross Section window.

Assert: The active-job collection tracks pending jobs rather than growing with historical completed work.

Protect: Cancelled, failed and nested callbacks and close ordering; no evidence ties this bookkeeping issue to SIGSEGV.

### FA72-011

Trigger: Compare git log/diff for xsection/window.py; commit4a92878 changes persistence/close paths.

Assert: Version-change statements distinguish unchanged tests from product paths actually changed.

Protect: Keep original crash evidence and clearly label historical versus current test/code revisions.

## Required verification layers

1. Pure independent numerical cases for source and rebuilt protected modules, including realistic absolute MD/TVD, unit changes, shallow upturns, station plateaus and irregular sampling.
2. Real SQLite transaction/lock/failure-injection tests with fresh connection reads, not only mocks of a success return. Verify partial success is disclosed and stale data is not certified as current.
3. GUI controls through Cancel/Retry/Discard, dirty Save As, source/output path conflicts and post-commit redraw errors. Verify counts, model state, stored values and dialogs together.
4. Owner-thread lifecycle and serial GUI stress: weak references for roots/canvases, pending Tcl jobs/commands, subscriptions/traces, workers and memory. Keep independent-process controls separate from long-process qualification.
5. One complete serial suite on the intended Tk 8.6 runtime under native diagnostics, preserving signal/exit/XML/logs; separate Tk 9 comparison. Never rerun a crash merely to relabel it green.
6. Received archive integrity/import checks and actual Windows rebuilt `.pyd` origin/hash parity. The separate audit-built Linux modules do not satisfy this gate.
7. Disposable Windows customer-executable qualification: cold launch, synthetic project create/import/save/reopen/export, failure/Cancel/retry and long GUI interactions. Use existing production trust; do not patch trust or clock on a working machine.

## Example full-source command

On a disposable Windows audit copy with Git and the exact runtime available:

```powershell
py -3.12 -X faulthandler -m pytest -v tests --tb=short -rs --junitxml=D:\Audit_v0972\full-results.xml *> D:\Audit_v0972\full-tests.log
```

Create the output folder first and retain every attempt. Build extensions only in the disposable build copy using the existing build procedure; do not edit tests to force a pass. A source-test result is separate from executing the frozen customer EXE.

## Acceptance

Record exact commit, package SHA-256, runtime and extension origins/hashes, main-test/subtest counts, skips and reasons, time, peak-process memory, native signal and actual process result. No interrupted run is a pass. An original SIGSEGV remains open without evidence supporting its closure; a controlled SIGABRT/SIGILL panic is a distinct finding. Windows/external-data/package skips are outstanding qualification, not successful tests.
