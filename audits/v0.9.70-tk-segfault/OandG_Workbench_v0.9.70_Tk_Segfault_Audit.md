# O&G Workbench v0.9.70 — Focused Tkinter Segmentation Fault Audit

Baseline: `release/1.0`, commit `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`. Read-only forensic investigation, 23 November 2026. No production code, existing tests, project dependencies, or release files were changed. All workloads used synthetic fixtures and isolated settings.

## Disposition

**The reported intermittent SIGSEGV / shell exit 139 remains unresolved. Do not declare it fixed.** The supplied traceback locates the event pump where the fault surfaced; it does not identify the native operation that failed. This investigation found confirmed lifecycle defects and a reproducible native Tcl finalization failure, but that controlled failure is a different signal and execution path. See the evidence document and run ledger for the exact completed experiment results.

The strongest supported explanation for the long-run sensitivity is accumulation of destroyed Tk-owning Python object graphs across tests, combined with repeated interpreter creation and event-loop activity. Current Geo and Petro trace ownership defects were demonstrated with controlled cleanup experiments. Their causal connection to the original SIGSEGV is a **strongly supported investigation hypothesis**, not a confirmed native root cause. A native stack from the original SIGSEGV is still required.

## Completed test evidence

- Long serial GUI sequence, Tk 86: 300 passed, 1 skipped, 14 warnings in 1326.29s (0:22:06); process exit 0. No native crash.
- Long serial GUI sequence, Tk 9: 1 failed, 299 passed, 1 skipped, 14 warnings in 1330.63s (0:22:10); process exit 1. No native crash.
- Six fresh complete Cross Section runs: 67 passed each; a seventh Tk 8.6 run under gdb also passed all 67.
- Cross Section lifecycle stress: 800 windows; no native crash and zero retained sections/Figures after the controlled main-thread GC boundary.
- Standalone minimal native probe: reproducible Tcl wrong-thread finalization, SIGABRT on Tk 8.6 and SIGILL on Tk 9; neither is the original SIGSEGV.

Exact commands, ordering results, assertion details, memory/GC observations and limits are in the Crash Evidence document and bundled logs. Repeated-run counts are not unique test coverage.

## Findings

### TK-01 — Original SIGSEGV lacks a reproducing native stack

Priority: Critical investigation gap. Classification: **Unresolved**. Confidence: High that closure is unsupported; Low on the exact SIGSEGV mechanism.

The reported fault occurs inside `tkinter.update`, including `tests/test_xsection.py` settings reopen paths. Fresh Cross Section runs, ordering experiments, and lifecycle stress provide bounded evidence only. No passing repetition can exclude an intermittent native defect. The user-supplied crash occurred in other releases as well; the exact original failing host runtime and native stack were not supplied.

Scenario: a long GUI test process fails during a later window update, even though the same test passes fresh. Recommendation: capture SIGSEGV in a native debugger using the exact failing runtime, full preceding test order, and matching symbols. Regression acceptance must include that reproducer, repeated serial runs, and native signal classification. Do not substitute the separate Tcl panic below for the original crash.

### TK-02 — Geo root graphs survive destruction through traces and subscriptions

Priority: High. Classification: **Confirmed production ownership defect on the exercised destroy path; possible contributing factor to SIGSEGV**. Confidence: High for retention; Medium for long-run contribution; Low for exact native causality.

Files: `geoworkbench/main_window.py:174`, `:383`, `:2625`; `geoworkbench/common.py:105`; `ogcore/well_selection.py:41`; `tests/test_xsection.py:2202`.

Geo subscribes a bound method to a strong process-global selection listener list and registers variable traces whose callbacks retain owners. Normal `on_close` unsubscribes the selection listener, but direct `destroy()` bypasses that path; several GUI fixtures use direct destruction. DepthEditTracker also registers traces. In an isolated ten-cycle probe, all ten destroyed Geo root wrappers remained after main-thread collection. Removing selection listeners alone did not release them. Removing the search trace alone also did not release them. After the diagnostic removed the remaining 210 variable traces from those disposable owners, all ten root wrappers were released (7,800 objects collected).

This establishes ownership retention, not ten still-visible windows or proof of native interpreter leakage. The surviving Python roots retain Tcl interpreter references; their finalization time is deferred. Cross Section tests that instantiate Geo can inherit this process state.

Recommendation: owner-specific trace tokens, idempotent disposal reached by every supported destruction path, explicit subscription ownership, and safe main-thread ordering. Do not globally erase variable traces as a production remedy. Regression: create/destroy Geo repeatedly with weak references, subscription counts, variable traces, and post-GC baselines; exercise both normal close and fixture teardown, including child windows.

### TK-03 — Petro search trace retains destroyed application roots

Priority: High. Classification: **Confirmed ownership defect on exercised destroy path; possible contributing factor**. Confidence: High for retention, Low for SIGSEGV causality.

Files: `petroworkbench/app.py:387`–395 and close path around `:460`.

The API search variable traces a bound application method. Ten raw create/destroy cycles left ten root wrappers after main-thread GC. Removing one owner trace per root in a separate diagnostic control released all ten, collecting 16,320 objects. This is not speculation based merely on the presence of a lambda or a large class.

Recommendation: retain and remove the trace token during owner disposal; test reopening and both close paths without changing filtering behavior. Regression: weak-root and trace-count baseline after hundreds of cycles, with retained search state verified independently.

### TK-04 — Wrong-thread collection can terminate Tcl natively on both Tk versions

Priority: High. Classification: **Confirmed root cause of the controlled native panic only; unresolved relationship to original SIGSEGV**. Confidence: High.

Files: diagnostic `probes/minimal_gc.py`; CPython `_tkinter.c` `Tkapp_Dealloc`; Tcl `Tcl_AsyncDelete`; relevant test mitigation `tests/conftest.py:116`–133.

A minimal standalone script creates a Tk root on the main thread, retains it in an artificial cycle, destroys its window, then collects the cycle on a worker. It imports no Workbench, NumPy, or Matplotlib. Tk 8.6.16 aborts with SIGABRT (child -6 / shell 134); Tk 9.0.4 traps with SIGILL (child -4 / shell 132). Both native stacks pass through `Tkapp_Dealloc` and `Tcl_AsyncDelete`, reporting asynchronous-handler deletion from the wrong thread. Main-thread controls finish normally. An additional worker-allocation variant triggers automatic GC with the same signals, without explicitly calling `gc.collect` on the worker. GC disabling and a self-cycle deliberately stage the condition; this does not show that Workbench reaches it in these tests.

The Tk 9 SIGILL is a deliberate panic trap in the captured stack, not evidence of an unsupported CPU instruction set. Debugger process exit 0 is not a passing inferior: the debugger stopped at the fatal signal.

The shipped autouse fixture already collects before/after tests when interpreter counts change. That reduces exposure but cannot reclaim graphs still strongly rooted by Tcl trace callbacks or global listeners, and does not guarantee which thread eventually releases every Tk-owning graph. The mitigation also existed in the inspected v0.9.67 source.

Recommendation: deterministic release on the owning thread; workers receive plain data and must not own final references to Tk graphs. Preserve main-thread test cleanup as mitigation, not proof of correctness. Regression: subprocess tests distinguishing main-thread success, controlled negative worker case, and real application lifecycle under ordinary worker allocation. Do not fix this by globally disabling GC.

### TK-05 — Geo timers outlive their Tcl callback commands after destruction

Priority: Medium. Classification: **Confirmed stale callback state; possible contributing factor**. Confidence: High for orphaned timers, Low for SIGSEGV causality.

Files: `geoworkbench/main_window.py:171`–175 and close/destroy paths. Probe: `runs/ownership/pending-after-destroy.log`.

Immediately after destroying the root, Tcl `after info` still contained `startup_project` and `_poll_requests` timers, while their corresponding script commands no longer existed. Subsequent event processing can encounter invalid-command callbacks. This does not establish a use-after-free in native Tk.

Recommendation: store and cancel owner job IDs before Tcl command destruction, make cancellation idempotent, and prevent rescheduling during disposal. Regression: destroy before startup delay, destroy with polling queued, then pump surviving interpreter events; require no stale owner callbacks and no Tcl background errors.

### TK-06 — Repeated roots and teardown paths amplify shared-state exposure

Priority: Medium. Classification: **Strongly supported hypothesis for test amplification; not a confirmed original crash cause**. Confidence: Medium.

Files: `tests/test_xsection.py` WindowTests, PunchListWindowTests, and GeoCrossSectionTests; `tests/conftest.py:92`–133. The settings test destroys and recreates section windows and pumps `update` repeatedly. Fixtures repeatedly create Tk roots; GeoCrossSection teardown directly destroys the Geo application rather than invoking its normal shutdown.

This makes the test process materially different from one desktop session ending with process termination. Persistent root graphs and figures from earlier modules can be present when Cross Section next pumps events. Collection thresholds, allocator layout, callbacks, and test order can change where a native failure surfaces; this explains why a later test name is not necessarily the owner of the defect. That explanation remains a hypothesis for SIGSEGV.

Recommendation: first correct owner cleanup; then document fixture lifecycle, drain/cancel callbacks explicitly, join workers, and verify weak references. Where appropriate, isolate independent root-heavy GUI groups in subprocesses while retaining a dedicated long serial stress job. Process isolation is containment, not a product fix.

### TK-07 — Embedded canvas retention needs sequence-level tracking; no isolated section leak proved

Priority: Medium investigation item. Classification: **Possible contributing factor; no confirmed Matplotlib native defect**. Confidence: Medium for retained graphs, Low for SIGSEGV cause.

Files: `xsection/window.py:96`–164, `:1649`–1670; Matplotlib `_backend_tk.py` CanvasTk and FigureManagerTk lifecycle. Cross Section owns/cancels scheduled jobs and canvas idle draw on destruction. Raster preparation pumps idle events, which permits reentrant idle work; no invalid callback there was proved.

The 800-window stress control ended with zero retained Cross Section windows and figures after explicit main-thread GC. Individual snapshots sometimes retained a few figures transiently. The long mixed-module sequence retained many embedded figures even though pyplot's Gcf manager count was zero. Gcf alone is therefore an insufficient leak check. Existing Matplotlib root bindings use weak references, and its FigureManager cancellation does not automatically cover every independently embedded canvas.

Recommendation: identify retained figure owners before changing canvas behavior; measure weak references, callbacks, canvas/toolbar disposal and main-thread collection under the actual failing sequence. Do not merge renderers or blame Matplotlib solely because `draw_idle` exists.

## Historical comparison and ruled-out claims

Twenty Fields and twenty Seismic-root cycles per version were compared at v0.9.69 (`020a48defc83204b8ea28275d44cb7e18fefaa36`) and v0.9.70 using the same Tk 8.6 environment. v0.9.69 retained twenty roots per case; v0.9.70 retained zero after main-thread GC. The particular Fields and Seismic trace fixes therefore work in the exercised cases. Reapplying those same fixes is not a supported diagnosis of the remaining problem.

Two hundred Tk-only and two hundred Tk+Matplotlib root cycles per version completed without native failure. This rules out a deterministic failure of those particular minimal loops; it does not clear either library generally. The controlled Tcl panic requires neither Workbench nor NumPy/Matplotlib, but those libraries remain unexcluded from the distinct original SIGSEGV. No Windows compiled customer package was tested in this investigation.

## Suite coverage and thread review

Reviewed root/close/callback/worker patterns across Cross Section, Geo, Petro, Seismic, Map/Drawings, Correlation, Raster/Digitizer, Geosteering and shared utilities. The ordered eight-module GUI run exercises each major area through existing synthetic tests; it is not all 287 test modules and is not a new whole-software audit.

Thread-site inventory included `ogcore/background.py`, `ogcore/task_progress.py`, `ogcore/assistant/provider.py`, `ogcore/assistant_ui.py`, `ograster/progress.py`, `seismicworkbench/mapping.py`, and `ogmap/window.py`. Inspected grid workers use numeric/plain-data work and UI-side delivery. `task_progress` pumps the main-thread event loop while workers report progress. No direct worker-to-Tk violation was proved in those inspected paths. Absence in sampled paths is not a complete proof over every closure or third-party finalizer.

## Answers to the ten audit questions

1. Most likely cause: lifecycle accumulation and deferred interpreter/object finalization are the best supported direction; the native SIGSEGV operation remains unidentified.
2. Both: production ownership omissions exist; repeated-root fixtures and bypassed shutdown amplify them. Neither is proved to cause exit 139.
3. Long processes accumulate retained graphs and process-global state. Exact finalization timing is sensitive to allocations and event processing.
4. Different Cross Section tests may simply be the next event pump. A varying failure location does not identify a particular geological workflow.
5. The controlled finalization panic affects both tested Tk versions, with different signals. The original SIGSEGV was not independently attributed to either version.
6. Windows impact is unverified. Tcl ownership rules warrant investigation, but no Windows executable/native run was performed and no Windows customer crash is claimed.
7. Yes, retained destroyed Python root graphs are confirmed; native interpreter leakage is not independently quantified.
8. Embedded figures accumulate in the mixed sequence, but isolated section cycles clean up and no original Matplotlib native fault was captured.
9. Own and remove traces/subscriptions/timers, dispose UI objects on their owner thread, and make fixture teardown faithful and measurable. No broad refactor or dependency upgrade is justified by this evidence.
10. Owner-specific retention/callback tests, repeated serial GUI runs on exact Tk 8.6 and Tk 9, worker-allocation subprocess stress, and the original SIGSEGV native reproducer are needed. Windows qualification remains separate.

## Limits and interpretation

The Tk 8.6 comparison uses an independently compiled debug _tkinter overlay, whereas Tk 9 uses the supplied runtime extension; matching Python and Python packages does not make the native builds identical or reproduce the original distribution build. The two Tk-version branches ran concurrently on the audit host, with serial test order inside each branch. Observer snapshots and thread profiling perturb timing and allocations. Fresh uninstrumented controls were included. Root counts are Python wrappers discoverable through weak tracking/GC, not native live-window counts. Destroyed interpreters may reject widget queries; unavailable measurements are not zeros. RSS values are process high-water marks, not a measurement of unfreed heap bytes. A caught TclError or an assertion failure is not a native crash. No original core dump was obtained; available gdb stacks are included. Diagnostic trace removal applies only to synthetic objects and is not an implementation change.
