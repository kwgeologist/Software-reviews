from pathlib import Path
import json,csv,platform,subprocess,hashlib
B=Path('/workspace/audit-v0.9.70-tk-segfault');O=B/'deliverables';O.mkdir(exist_ok=True)
N='OandG_Workbench_v0.9.70_Tk_'
def out(n,s):(O/(N+n)).write_text(s.strip()+'\n')
out('Segfault_Audit.md',r'''
# O&G Workbench v0.9.70 — Focused Tkinter Segmentation Fault Audit

Baseline: `release/1.0`, commit `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`. Read-only forensic investigation, 23 November 2026. No production code, existing tests, project dependencies, or release files were changed. All workloads used synthetic fixtures and isolated settings.

## Disposition

**The reported intermittent SIGSEGV / shell exit 139 remains unresolved. Do not declare it fixed.** The supplied traceback locates the event pump where the fault surfaced; it does not identify the native operation that failed. This investigation found confirmed lifecycle defects and a reproducible native Tcl finalization failure, but that controlled failure is a different signal and execution path. See the evidence document and run ledger for the exact completed experiment results.

The strongest supported explanation for the long-run sensitivity is accumulation of destroyed Tk-owning Python object graphs across tests, combined with repeated interpreter creation and event-loop activity. Current Geo and Petro trace ownership defects were demonstrated with controlled cleanup experiments. Their causal connection to the original SIGSEGV is a **strongly supported investigation hypothesis**, not a confirmed native root cause. A native stack from the original SIGSEGV is still required.

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
''')
out('Recommended_Fixes.md',r'''
# Recommended corrections — proposals only

No changes were implemented. Preserve geology, formulas, independent renderers, project schema, persistence behavior and UI design.

## Practical order

1. **Capture the original SIGSEGV native stack.** Retain the failing environment and exact full test order. Use gdb before trying a dependency upgrade. Save runtime/library hashes, signal and all-thread native/Python traces. The current native panic reproduction cannot close the original finding.
2. **Correct demonstrated owner leaks.** Geo and DepthEditTracker must own each trace token and selection subscription. Petro must own its search trace. Make disposal idempotent and available to both supported normal close and destruction paths. Remove only the owner's traces; never blanket-remove all project traces. Keep settings saves and close prompts in their existing intended workflow.
3. **Cancel owner callbacks before deleting their Tcl commands.** Geo startup/poll timers are confirmed orphaned after raw destruction. Prevent callbacks from rescheduling once disposal starts. Test destruction before and during startup/polling.
4. **Enforce thread ownership at object release as well as widget calls.** A worker can trigger Python GC without calling Tk explicitly. Keep Tk-containing graphs on the owning thread through deterministic disposal; pass plain results to UI queues. Do not introduce global GC disabling or swallow Tcl errors as a substitute.
5. **Tighten GUI fixture disposal without hiding failures.** Close children/canvases, stop pending work, join workers, release traces/subscriptions, then root; assert weak-reference and callback baselines. Keep serial long-process stress and root-recreation coverage. Separate processes may contain unrelated GUI groups but cannot demonstrate the product defect is fixed.
6. **Investigate retained figures by owner.** Use real embedded Figure weak references, not only pyplot Gcf. Test canvas idle draws, toolbar, bindings, window closure during raster preparation, and delayed results. Change Matplotlib integration only when a failing owner path is demonstrated.

## Regression acceptance matrix

- Geo/Petro: hundreds of both-close-path cycles; no linear root/widget/trace/listener growth after owner-thread GC; settings/filtering remain correct.
- Callback ownership: no after script references deleted owner commands; closing during startup, polling, redraw, and delayed worker completion causes no background Tcl errors.
- Cross Section: settings reopen, map-selected wells, raster load/destroy and normal/raw child close; pending jobs cleared and no retained section/figure graphs after the documented collection boundary.
- Native: main-thread minimal case succeeds; negative wrong-thread probe retains its explicit expected fatal-signal classification in disposable subprocesses; application stress never reaches that unsafe condition.
- Order: Cross Section fresh, after Seismic, after Map, after Correlation, after the defined mixed GUI sequence, and after the original complete failing sequence when available.
- Environments: same Python/runtime comparison on Tk 8.6 and Tk 9; uninstrumented plus observed repetitions; Windows native/source and packaged executable qualification separately recorded.
- Closure: original SIGSEGV reproducer passes repeatedly with native monitoring and no substituted signals. A single clean rerun or different Tcl panic fix is insufficient.

## Safe to leave alone for now

The v0.9.70 Fields/Seismic trace fixes passed independent retention controls. Pure repeated section creation cleaned up after main-thread GC. No evidence justifies merging renderers, replacing Tk, changing geological algorithms, or broadly rewriting the UI. Existing main-thread collection guards remain useful mitigation while owner-specific problems are addressed.
''')
out('Reproduction_Instructions.md',r'''
# Reproduction instructions

All commands below are diagnostic. Run in a disposable workspace against the exact clean checkout, never client projects. The included original command.json records are authoritative for this run; absolute paths describe this audit machine and must be adjusted on another host. Existing tests remain unchanged.

## Runtime and directory setup

Set B to the extracted evidence directory's parent corresponding to this audit workspace; C is a verified checkout at `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`; P is CPython 3.12.14. Use a separate virtual environment with recorded NumPy 2.5.5, Matplotlib 3.11.2, SciPy 1.18.1 and pytest 9.2.0. Do not install into or update the Workbench checkout. Use an owned Xvfb display on Linux.

The supplied drivers retain this machine's paths for audit reproducibility. Edit a COPY outside source to point B/C/P/X and dependency search paths at your environment before use. They are not a portable one-click installer. `evidence/runtime.json` records native versions and hashes. `evidence/setup_native.py` and `more_native.py` record how the debugger/header overlay was obtained. Downloaded tool packages are not project dependencies.

Tk 8.6 was selected with a CPython 3.12 `_tkinter` overlay compiled from exact upstream CPython v3.12.14 source in `evidence/tk86-extension/`. Tk 9 uses the runtime's original extension. Compile against your interpreter headers and matching Tk libraries; do not copy a Linux extension into a Windows package.

Example environment, matching recorded audit paths:

```bash
export B=/workspace/audit-v0.9.70-tk-segfault
export C=/workspace/audit-v0.9.70-integrity/checkout
export P=/workspace/audit-v0.9.56-windows/tooling/bin/python
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export PYTHONPATH="$B/tk86-extension:/workspace/audit-v0.9.68-full/deps:$B/probes"
export DISPLAY=:221
cd "$C"
"$P" -X faulthandler -m pytest -q -p no:cacheprovider tests/test_xsection.py --tb=short -rs
```

Start an Xvfb server for DISPLAY first. For Tk 9 remove only the tk86-extension entry from PYTHONPATH. Print `_tkinter.__file__`, Tcl `info patchlevel` and Tk `package provide Tk` from an actual root; module constants alone do not establish patch versions.

## Exact experiments

`run_experiments.py` records A (three fresh full Cross Section files per Tk version), D (two target cases first/after Seismic/Map/Correlation), and C (eight modules sequentially in one interpreter per version). Each run saves its full command, stdout/stderr, XML and status. `-p tk_observer` adds external observation for designated runs. The first fresh repetition is uninstrumented.

The serial module order is Geo tabs, Map drawing objects, Petro integration, Digitizer UI, Geosteering project, Seismic app, Correlation, then Cross Section. It is a defined GUI workload, not all software tests. Do not use xdist to reproduce this ordering condition.

`run_lifecycle.py` and `probes/lifecycle.py` run 200 normal-close and 200 raw-destroy Cross Section cycles for each Tk version against synthetic test fixtures. Measurements occur every twenty cycles and after explicit owner-thread collection.

`run_minimal.py` covers 200 roots with Tk only and 200 with TkAgg per Tk version. `probes/retention_compare.py`, `ownership_probe.py`, `petro_retention.py` and `referrers_probe.py` implement the historical and current ownership controls. Diagnostic removal of traces affects only disposable probe objects. It must not be copied as a blanket application cleanup routine.

## Controlled native failure, separate from SIGSEGV

With an X display and selected runtime:

```bash
"$P" -X faulthandler "$B/probes/minimal_gc.py" main
"$P" -X faulthandler "$B/probes/minimal_gc.py" worker
"$P" -X faulthandler "$B/probes/minimal_gc.py" auto-worker
```

The main control passes. The worker variants intentionally arrange collection of a destroyed root's artificial cycle off its owner thread. Observed fatal results: Tk 8.6 SIGABRT, Tk 9 SIGILL. These are unsafe negative tests, so run each in its own subprocess. The auto-worker variant enables automatic GC and allocates objects; it does not explicitly invoke worker `gc.collect`.

Native debugger command used, with LD_LIBRARY_PATH pointing to the external debugger library overlay:

```bash
gdb --batch -ex 'set pagination off' -ex 'set debuginfod enabled off' \
  -ex 'set print thread-events off' -ex run \
  -ex 'thread apply all bt 35' -ex 'info sharedlibrary' \
  --args "$P" -X faulthandler "$B/probes/minimal_gc.py" worker
```

For the original SIGSEGV use the same debugger prefix with the exact failing pytest invocation and full preceding test order. Preserve the signal line and native frames, not just Python's final `update` frame. An exit-zero gdb parent can still contain a fatal inferior signal. This audit did not alter kernel core-dump settings.

## Windows follow-up

No Windows executable was tested here. Run in a disposable Windows test environment with synthetic projects and the exact dependency/build inventory. Use the original failing sequence if available, faulthandler and a Windows native debugger or crash dump collector. Record source-test results separately from packaged compiled modules and frozen executable results. The Linux overlay/gdb scripts do not establish Windows behavior.
''')
rows=[
('TK-01','Critical investigation gap','Unresolved','tests/test_xsection.py; tkinter.update','PunchListWindowTests; GeoCrossSectionTests','Original SIGSEGV has no reproducing native stack','Fresh passes cannot close an intermittent native fault','Capture exact failing runtime and all-thread native stack','Original reproducer repeated serially with signal monitoring','High for open disposition; Low for exact cause'),
('TK-02','High','Confirmed ownership defect; possible contributing factor','geoworkbench/main_window.py:174,383,2625; geoworkbench/common.py:105; ogcore/well_selection.py:41','Geo shutdown; DepthEditTracker','10 roots retained; after listener and 210 trace cleanup, 0','Delayed release of destroyed Tk graphs across repeated roots','Owner-specific idempotent trace/subscription disposal','Weak roots and trace/listener baselines for both close paths','High for retention'),
('TK-03','High','Confirmed ownership defect; possible contributing factor','petroworkbench/app.py:387-395,460','Petro search trace','10 roots retained; remove 10 traces ->0','Destroyed application graphs survive collection','Own/remove search trace token','Hundreds of close/reopen cycles preserving search behavior','High for retention'),
('TK-04','High','Confirmed root cause of controlled native panic only','probes/minimal_gc.py; CPython Tkapp_Dealloc; Tcl_AsyncDelete','Worker GC of destroyed root cycle','Tk86 SIGABRT; Tk9 SIGILL; main controls pass','Thread-affine native finalization can terminate process','Deterministic owner-thread disposal; plain worker data','Subprocess negative/positive controls plus real worker-allocation stress','High for controlled panic; Low for link to SIGSEGV'),
('TK-05','Medium','Confirmed stale callback state; possible contributing factor','geoworkbench/main_window.py:171-175','startup_project; _poll_requests','2 after timers survive with absent callback commands','Later event processing can invoke deleted command','Own/cancel timers before command destruction','Destroy before startup and during poll then pump events','High for orphaning'),
('TK-06','Medium','Strongly supported amplification hypothesis','tests/test_xsection.py:2202-2221; tests/conftest.py:92-133','Repeated roots; raw destroy fixtures','Shutdown bypass plus retained graphs in long process','Test order and GC/event timing can move failure location','Faithful teardown and long serial stress; subprocess containment separately','Compare order, weak graphs, callbacks, worker completion','Medium'),
('TK-07','Medium investigation item','Possible contributing factor','xsection/window.py:96-164,1649-1670; Matplotlib _backend_tk.py','Embedded canvas/idle lifecycle','800 section cycles clean after GC; mixed sequence retains figures','Gcf counts do not cover embedded figures','Track owner references and disposal before changing integration','Canvas/toolbar idle-close and serial figure weak-reference checks','Medium for retention; Low for native causality'),
('CONTROL-01','Informational','Ruled out by evidence for specific exercised retention paths','xsection/widgets.py Fields; seismicworkbench/app.py well_find trace','v69 versus v70 controls','20 retained per v69 case versus0 v70','Old fixed trace leaks do not diagnose remaining defect','Preserve fixes; no redundant rewrite','Keep same owner-specific retention controls','High for bounded control')]
with (O/(N+'Lifecycle_Findings.csv')).open('w',newline='')as f:
 w=csv.writer(f);w.writerow(['ID','Severity','Classification','Files/lines','Function/area','Evidence/current behavior','Risk','Recommended correction','Regression test','Confidence']);w.writerows(rows)
print('Wrote four reports; evidence ledger generated at completion')
