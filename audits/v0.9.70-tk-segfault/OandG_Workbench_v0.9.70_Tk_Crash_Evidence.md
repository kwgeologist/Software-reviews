# Crash evidence and completed experiment ledger

Exact source: `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa` (v0.9.70). Source ZIP SHA-256: `a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797`. All 961 tracked files match their pre-run hashes and checkout status is clean. See `evidence/input-integrity.json`.

## Environment

Linux x86_64, Debian 13, kernel 6.18.57; CPython 3.12.14 for both comparisons. Tcl/Tk 8.6.16 uses a separately compiled upstream _tkinter overlay; Tcl/Tk 9.0.4 uses the runtime extension. NumPy 2.5.5, Matplotlib 3.11.2, SciPy 1.18.1, pytest 9.2.0. Xvfb package 2:21.1.16-1.3+deb13u4; gdb 16.3-1. Exact extension paths and hashes are in `evidence/runtime.json`; per-process patch versions and selected origins are in observation/minimal logs. This is not the original failing machine and does not replicate its precise dependency build.

## Pytest experiment results

Each row is a separate process, except that all module names within one row ran serially in that process. Counts overlap across repetitions and are not unique software-test coverage. XML counts may include passed subtests as testcase elements; authoritative pytest terminal summaries are quoted below. Full commands are in `evidence/runs/<name>/command.json`. No xdist was used.

| Run | Exit / seconds | Pytest terminal result |
| --- | --- | --- |
| A-86-1 | 0 / 62.1 | 67 passed, 1 warning in 60.36s (0:01:00) |
| A-86-2 | 0 / 117.4 | 67 passed, 1 warning in 115.27s (0:01:55) |
| A-86-3 | 0 / 112.2 | 67 passed, 1 warning in 109.31s (0:01:49) |
| A-9-1 | 0 / 62.1 | 67 passed, 1 warning in 60.46s (0:01:00) |
| A-9-2 | 0 / 115.6 | 67 passed, 1 warning in 113.54s (0:01:53) |
| A-9-3 | 0 / 111.0 | 67 passed, 1 warning in 108.29s (0:01:48) |
| C-86-serial-GUI | 0 / 1337.3 | 300 passed, 1 skipped, 14 warnings in 1326.29s (0:22:06) |
| C-9-serial-GUI | 1 / 1342.1 | 1 failed, 299 passed, 1 skipped, 14 warnings in 1330.63s (0:22:10) |
| D-86-after-correlation | 0 / 65.7 | 48 passed, 1 warning in 64.71s (0:01:04) |
| D-86-after-map | 0 / 22.9 | 25 passed, 1 warning in 21.97s |
| D-86-after-seismic | 0 / 65.8 | 65 passed, 13 warnings in 64.44s (0:01:04) |
| D-86-first | 0 / 15.9 | 2 passed, 1 warning in 14.67s |
| D-9-after-correlation | 1 / 64.3 | 1 failed, 47 passed, 1 warning in 63.21s (0:01:03) |
| D-9-after-map | 0 / 24.0 | 25 passed, 1 warning in 23.12s |
| D-9-after-seismic | 0 / 67.6 | 65 passed, 13 warnings in 66.54s (0:01:06) |
| D-9-first | 0 / 16.5 | 2 passed, 1 warning in 15.31s |
| F-86-native-xsection | 0 / 126.2 | 67 passed, 1 warning in 123.61s (0:02:03) |

Fresh A runs: three full Cross Section files per Tk version, first uninstrumented and next two observed. D uses the settings-reopen and map-selected-section targets first or after the named preceding modules. C uses the eight-module serial order documented in the reproduction instructions, ending in the whole Cross Section file. F-86 is a complete Cross Section file under gdb; its normal-exit log is a native diagnostic baseline, not a crash stack.

Each long sequence skipped the Windows-only Explorer-drop test at tests/test_geo_tabs.py:580 on Linux. Made/destroy counters count method invocations, not unique native interpreter lifetimes. Assertion failures in the ledger remain failures; inspect the accompanying XML and terminal logs. They are not SIGSEGV. The repeated Correlation settings box-width assertion observed in Tk 9 is separate from this native-stability investigation.

## Long-sequence state

Tk 86: maximum observed {"root_wrappers": 136, "figures": 155, "widgets": 19235, "rss_high_water_KiB": 2640504}. Last event `sessionfinish 0`; tracked made/destroy/GC counts `{"made": 267, "destroy": 268, "gc": 26693, "cross_thread_tk_calls": 0}`. Worker-GC observations: 8; off-main Python tkinter entries: 0.

Tk 9: maximum observed {"root_wrappers": 136, "figures": 155, "widgets": 19240, "rss_high_water_KiB": 2809416}. Last event `sessionfinish 1`; tracked made/destroy/GC counts `{"made": 267, "destroy": 268, "gc": 26537, "cross_thread_tk_calls": 0}`. Worker-GC observations: 8; off-main Python tkinter entries: 0.

The root samples include destroyed Python root wrappers. They are not a count of simultaneously mapped windows or an independent measurement of allocated Tcl interpreters. Off-main Python tkinter entries, if present, are not automatically native Tk calls. Observer queries can fail once Tk is destroyed; missing after/widget data are unavailable, not zero. High-water RSS does not subtract freed allocations. Instrumentation can alter timing and memory. The uninstrumented fresh controls reduce but do not remove this limitation.

## B: repeated Cross Section lifecycle

Four separate workloads, 200 windows each: normal close and raw destroy, on each Tk version. Total 800 windows. All exited normally. After explicit main-thread collection each ended with zero retained section windows and Figures, one synthetic fixture root/widget, and no pending after callbacks. Native command counts stabilized near baseline (+3 commands). Intermediate weak-reference counts sometimes retained a few closed sections/figures until collection; no monotonic section-retention trend was demonstrated. Peak high-water RSS was approximately 173 MiB on Tk 8.6 and 168 MiB on Tk 9; consult lifecycle JSONL for exact KiB values. These results do not prove every project/raster workflow is leak-free.

## Standalone native failures

The controlled root self-cycle is created with automatic GC disabled, the window is destroyed on its owner thread, and one root wrapper remains in GC with zero Figures and an empty Tcl after queue. Forcing collection on main succeeds. Forcing collection on a worker terminates Tcl. Re-enabling GC and allocating on a worker also terminates Tcl. No Workbench imports or data are involved.

| Runtime | Main control | Worker result | Native frames |
| --- | --- | --- | --- |
| Tk 8.6.16 | exit 0 | SIGABRT, child -6 / shell 134 | abort, Tcl_Panic, Tcl_AsyncDelete, Tkapp_Dealloc, Python GC, worker |
| Tk 9.0.4 | exit 0 | SIGILL, child -4 / shell 132 | Tcl_Panic, Tcl_AsyncDelete, Tkapp_Dealloc, Python GC, worker |

This is **not the original SIGSEGV / 139**. Native and faulthandler traces are retained under `evidence/runs/minimal/`: `native-detailed-86.log`, `native-detailed-9.log`, `native-auto-worker-86.log`, `gc-detailed-*-*.log`, and `auto-worker-*.log`. The main thread waits for its worker in these failures rather than crashing in `tkinter.update`. Debugger parent exit 0 means gdb processed its commands; examine the inferior signal. No original SIGSEGV core was captured; kernel core settings were not changed.

The Tk-only and Tk+Matplotlib simple root-loop controls each completed 200 cycles per Tk version (800 root cycles total), with normal exits. This is a bounded control, not a general library clearance.

## Controlled ownership evidence

- `evidence/runs/ownership/all-traces-control.log`: ten Geo roots retained after raw destroy and owner-thread GC; listener-only and search-only controls insufficient; 210 remaining trace removals released all ten.
- `evidence/runs/ownership/petro.log`: ten Petro roots retained; removing ten trace commands released all ten.
- `evidence/runs/ownership/pending-after-destroy.log`: Geo startup/poll timers survived but their Tcl callback commands did not.
- `evidence/runs/ownership/referrers.log`: retaining bound selection callback, Tk variables, owner/widget graphs and closure cells.
- `evidence/runs/retention-comparison/69.log` and `70.log`: twenty Fields and twenty Seismic cycles each; v69 retains twenty per case, v70 zero. This validates those specific cleanup fixes.

Diagnostic removal controls operate only on disposable synthetic objects. They establish retention paths without editing production files. They do not constitute implemented corrections.

## Artifact and audit limits

No client project, Windows customer executable, Windows licensing extensions, geological calculation, or release artifact was exercised or modified. This focused investigation is separate from the prior whole-suite audit. The original crash trace is user-supplied evidence; the logs in this ZIP are independently generated evidence. The report retains the original finding as unresolved.

The bundle includes reports, machine-readable summaries, native/Python traces, full per-run command/status/XML/observation records, standalone probes, upstream extension source and hashes, setup scripts, and source-integrity verification. Full downloaded Debian debugger packages, installed debugger trees, complete application source, unrelated prior audits and temporary caches are intentionally excluded. Reproduction requires the matching external runtime/tooling; paths in scripts must be adapted on another host.
