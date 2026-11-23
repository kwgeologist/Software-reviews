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
