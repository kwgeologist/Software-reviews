# Audit evidence — v0.9.72

## Verified inputs

Git checkout: `cbc253ccf2793859fa909e9b8521331ddf389f22`, fetched from `release/1.0`, audited detached at that exact commit. `ogcore.__version__=0.9.72`, empty build marker. Branch advancement during or after this audit does not change the audited baseline.

Uploaded source ZIP SHA-256: `41ece88abe5430264e5e3905e4ee1df425cffab10c5a66fe0d2d5ca4edba2b17` (matches expected). All production files match Git. 980 tracked files total; 977 exported tracked files plus RELEASE_FILES.txt in the ZIP. Three scanned test TIFFs are explicitly export-ignored, not missing production files.

The archive manifest names 977 files; independent size/SHA-256 checks all pass. `tools/release/source_zip.py verify <received ZIP>` returns `OK: complete, and every module and entry point imports`. This verifies the actual received source ZIP, not a reconstructed archive. It contains no customer Windows EXE/.pyd payload.

Logs: `baseline.json`, `source-hashes.json`, `zip-inventory.json`, `release-manifest-check.json`, `package-checks/verify.log`, final integrity record. The change ledgers preserve v0.9.71r2->v0.9.72 and v0.9.70->v0.9.72 paths/stats and diff hashes; full patches are omitted to avoid unnecessary application source. The former has19 changed files, mostly LIC flow/tests/docs plus the Batch Zones warning; the pay N/A engine change already exists in v0.9.71r2.

Previous audit sources: Software-reviews v0.9.70 Full Combined Audit, its recent-persistence evidence, and the focused Tk audit. The v0.9.71 remediation/closure/test/compatibility documents and v0.9.72 change/test/checklist reports were retrieved from the verified Workbench source docs directory. Author-reported tests are labelled supplied evidence; they are not independent results of this audit.

Evidence paths below are relative to the bundle evidence directory unless a report name is given.

## Independent full serial run

3224 passed, 10 skipped, 365 warnings, 1214 subtests passed in 4231.52s (1:10:31); inferior exit 0; gdb exit 0

The exact native-debugger/pytest command and environment are in `full-serial/command.json`. It is one interpreter running `pytest -v ... tests`, all 293 test modules and 3,234 main collected tests, without xdist or test changes. gdb wraps the main process; separate diagnostic/compiled/scale processes also ran on the host. Thus test order is serial inside this run, but the host was not exclusively idle.

```bash
/workspace/audit-v0.9.70-tk-segfault/native/root/usr/bin/gdb --batch \
  -ex 'set pagination off' -ex 'set debuginfod enabled off' \
  -ex 'set print thread-events off' -ex run \
  -ex 'thread apply all bt 60' -ex 'info sharedlibrary' --args \
  /workspace/audit-v0.9.56-windows/tooling/bin/python -X faulthandler -m pytest -v \
  -p no:cacheprovider tests --tb=short -rs \
  --junitxml=/workspace/audit-v0.9.72-full/full-serial/results.xml
```

Environment: DISPLAY=:241, PYTHONDONTWRITEBYTECODE=1, OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, MKL_NUM_THREADS=1. PYTHONPATH selects the isolated Tk 8.6 _tkinter overlay plus the recorded dependency folder; LD_LIBRARY_PATH supplies the separately unpacked native debugger libraries. Full paths are historical audit-machine paths, not product install paths.

Debugger parent exit 0 never establishes a passing inferior. Examine native signal lines and pytest completion/XML. The final-summary record distinguishes debugger status, inferior outcome, test completion and actual counts. No interrupted or crashing attempt is described as a pass, and no full retry was started to seek a green result.

## Final full-run reconciliation

| Measurement | Result |
| --- | --- |
| Collected main tests | 3234 |
| Test modules | 293 |
| Passed | 3224 |
| Failed | 0 |
| Skipped | 10 |
| Errors | 0 |
| Passed subtests (separate) | 1214 |
| Pytest seconds | 4231.52 |
| Driver seconds | 4260.91 |
| Main inferior peak RSS, KiB | 6887200 |
| Inferior exit | 0 |
| gdb exit | 0 |
| Native signals | None observed |

The completed main-test count reconciles to collection: 3234 / 3234. Passed subtests are additional records, not additional collected main tests. JUnit suite attributes and any failure cases are preserved in `full-serial/final-summary.json`.

### Full-run skip reasons

- SKIPPED [1] tests/test_cython_build.py:115: the protected modules are not compiled (tools/release/build_cython.py)
- SKIPPED [1] tests/test_cython_build.py:63: the protected modules are not compiled (tools/release/build_cython.py)
- SKIPPED [1] tests/test_cython_build.py:69: the protected modules are not compiled (tools/release/build_cython.py)
- SKIPPED [1] tests/test_geo_tabs.py:591: Explorer drops are a Windows message
- SKIPPED [1] tests/test_kingdom_native_full.py:22: full Kingdom files not supplied (OGW_KINGDOM_NATIVE / OGW_KINGDOM_TRUTH)
- SKIPPED [1] tests/test_licensing.py:389: DPAPI is Windows' (a Windows qualification item)
- SKIPPED [1] tests/test_pdf_packaging.py:208: slow packaged build: set OGW_PACKAGING_TEST=1
- SKIPPED [1] tests/test_v0957_fixes.py:268: DPAPI is Windows' (a Windows qualification item)
- SKIPPED [1] tests/test_v0958_fixes.py:254: DPAPI is Windows' (a Windows qualification item)
- SKIPPED [1] tests/test_v0969_fonts_audit.py:83: no font here that is in Tk as an alias and not in Matplotlib

This result does not close the supplied intermittent SIGSEGV. No native crash occurred in this attempt, so no faulting C stack from this run exists. The debugger reports normal process termination; earlier controlled panic traces remain separately labelled historical evidence.

The terminal reports 365 warnings, retained in the full log. Repeated Pyshp DBF-size warnings also reproduce with Pyshp 3.1.9's own writer/reader without any Workbench import (`probes/pyshp_warning_control.py`, `pyshp-warning-control.json`); the synthetic record reads back correctly. This does not establish Workbench project corruption or qualify other GIS readers. Matplotlib legend warnings and other warning contexts remain in the log. No warning filters were added.

The original reported crash-path test, `tests.test_xsection.PunchListWindowTests::test_settings_hold_from_one_session_to_the_next`, completed successfully in this run; its exact XML result is in the final summary. A single successful recheck is not closure of the intermittent native fault.

## Runtime identity

```json
{
  "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
  "executable": "/workspace/audit-v0.9.56-windows/tooling/bin/python",
  "platform": "Linux-6.18.57-x86_64-with-glibc2.41",
  "Tcl": "8.6.16",
  "Tk": "8.6.16",
  "tkinter_extension": "/workspace/audit-v0.9.70-tk-segfault/tk86-extension/_tkinter.cpython-312-x86_64-linux-gnu.so",
  "tkinter_sha256": "fdd6fea19f07f8d5087d5b6ae525cba5dbd62fbc91ab520b7a130cdfbb44b650",
  "NumPy": "2.5.5",
  "Matplotlib": "3.11.2",
  "SciPy": "1.18.1",
  "pytest": "9.2.0"
}
```

The Tk 8.6 overlay was compiled outside the Workbench tree from upstream CPython3.12.14 _tkinter source against Tcl/Tk8.6.16. Tk 9.0.4 uses the existing interpreter runtime extension. Both use CPython3.12.14 and the same recorded Python runtime packages, but the native builds are not identical and are not the original failing distribution build. No project dependencies were updated.

Xvfb package2:21.1.16-1.3+deb13u4; gdb16.3-1. Debian GNU/Linux13, x86_64. Source runtime and actual extension hashes are in `runtime-Tk86.json` and `runtime-Tk9.json`.

## Time, memory and signal accounting

The final full-run summary records elapsed driver time, pytest time/counts, debugger and inferior outcome, skips/reasons, native signals and peak main-inferior RSS. The principal log is `full-serial/pytest-native.log`; XML is included only if the process wrote it. Native backtraces/shared-library tables are in that same log.

The first child-discovery monitor could not enumerate gdb children through this sandbox task-children interface and reported zero; that field is not accepted as a measurement. A second monitor pins the actual inferior PID from the native log and records `/proc/<PID>/status` VmRSS and VmHWM. Final peak is the maximum VmHWM observed (which includes earlier process history) and is explicitly the main inferior, not gdb or total descendant/host memory. `resource-pinned.jsonl` is authoritative; the initial monitor record is retained for transparency.

RSS is a high-water process measurement, not unfreed heap bytes or a native-interpreter count. No full-run Figure/root census plugin was inserted, so earlier focused-audit figure counts are not recast as new v0.9.72 counts. Debugger scheduling and concurrent audit workloads affect timing. /proc mem read-only warnings and an ELF dynstr warning appear; native gdb smoke/control traces in the earlier audit demonstrate usable C unwinding, but not full native debug symbols. No kernel core settings were changed and no original SIGSEGV core is claimed.

## Compiled-module checks

Audit-only copy: `compiled-probe/`, not the verified source checkout. Tools installed only in `build-tools/`: Cython3.2.4, setuptools80.9.0 and wheel (install log included). Existing build_cython.py compiled all 15 protected modules into Linux extensions with unchanged Python sources. Build log and per-module origins/SHA-256 are retained; generated C, object files, full source copy and binaries are excluded from the deliverable ZIP.

```bash
PYTHONPATH=<audit build-tools>:<runtime deps> CC=cc python tools/release/build_cython.py
python -X faulthandler -m pytest -q -p no:cacheprovider \
  tests/test_cython_build.py tests/test_v0971_persistence.py \
  tests/test_v0971_integrity.py tests/test_v0971_numerics.py \
  tests/test_v0971_cleanup.py tests/test_v0971_packaging.py \
  tests/test_v0972_lic_import.py tests/test_batch_zones.py \
  tests/test_v0970_tk_lifecycle.py --tb=short -rs --junitxml=<audit>/compiled-checks/results.xml
```

Actual result:128 passed,4 skipped,74 subtests passed, exit 0; pytest47.63s, driver49.45 s. Tk 9.0.4. Four packaging tests skip because the isolated compiled copy intentionally has no .git metadata. The source checkout has Git and includes those tests in its full run. JUnit tests=206 includes74 subtest entries: do not call that206 independent main tests. Source full-suite counts and compiled target counts overlap and are not summed as unique coverage.

These are audit-built Linux `.so` tests. They do not inspect or execute a shipped Windows `.pyd` or EXE. Parity proves matching outputs, not correctness: `compiled-origins.json` also records the FA-002 failure in the actual loaded compiled pay module.

## Independent diagnostic results

Each script runs against temporary synthetic data with test-session license/preferences isolated by the existing conftest. Probe exit 0 means the diagnostic completed and wrote evidence; several deliberately demonstrate incorrect observed behavior. These are separate from pytest pass totals.

### numerical_reference.py

Command form: `python -X faulthandler probes/numerical_reference.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `numerical-reference.json`. Vertical/inclined controls pass; shallow upturn violates N/A; unique inverse and EUR references corrected.

### numerical_breadth.py

Command form: `python -X faulthandler probes/numerical_breadth.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `numerical-breadth.json`. 18 independent mathematical reference checks pass; synthetic only.

### compiled_origins.py

Command form: `python -X faulthandler probes/compiled_origins.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `compiled-origins.json`. All 15 actual extension origins/hashes; compiled shallow-upturn failure matches source.

### lic_edges.py

Command form: `python -X faulthandler probes/lic_edges.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `lic-edge-results.json`. OverwriteNo modifies own input without backup; GROUP1/2 export as0 and cannot roundtrip.

### lic_cancel_batch.py

Command form: `python -X faulthandler probes/lic_cancel_batch.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `lic-batch-cancel.json`. 2327 items; Cancel at2001 ignored inside last batch; real SQLite lock yields327 attempts/failures.

### lic_commit_progress.py

Command form: `python -X faulthandler probes/lic_commit_progress.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `lic-commit-progress.json`. Real progress UI says Succeeded2/Failed0/Completed after both writes roll back; details correctly show errors.

### save_as.py

Command form: `python -X faulthandler probes/save_as.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `save-as-results.json`. Original Edited Draft; newly opened SaveAs copy Tab Well.

### sync_edges.py

Command form: `python -X faulthandler probes/sync_edges.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `sync-edge-results.json`. Real write-lock prevents generation; normal close and stale acceptance; malformed handoff ValueError; Recovery schema warning drift.

### production_edges.py

Command form: `python -X faulthandler probes/production_edges.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `production-edge-results.json`. First3 expected400/actual300; non-finite row accepted.

### petro_partial_publish.py

Command form: `python -X faulthandler probes/petro_partial_publish.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `petro-partial-publish.json`. Stored zone base5520; published gross60 instead80; saveTrue, no UI warning.

### map_postcommit.py

Command form: `python -X faulthandler probes/map_postcommit.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `map-postcommit.json`. Real shape feature saved before refresh exception; retry duplicates.

### section_jobs.py

Command form: `python -X faulthandler probes/section_jobs.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `section-job-results.json`. 1000 completed callbacks leave1005 stored IDs; only one Tcl job pending.

### ownership_probe.py

Command form: `python -X faulthandler probes/ownership_probe.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `retention/ownership_probe.py.log`. Ten Geo roots retained until diagnostic removal of210 remaining traces after listener/search controls.

### petro_retention.py

Command form: `python -X faulthandler probes/petro_retention.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `retention/petro_retention.py.log`. Ten Petro roots retained; ten trace removals release all.

### timer_probe.py

Command form: `python -X faulthandler probes/timer_probe.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `timer-probe.log`. Two after timers survive but callback commands are gone.

### scale_probe.py

Command form: `python -X faulthandler probes/scale_probe.py` with the recorded runtime dependency path; GUI probes use their own Xvfb displays242-251, the Tk 8.6 overlay and disposable settings. `compiled_origins.py` explicitly imports from the isolated compiled copy. See scripts and command index for exact path constants.

Evidence: `scale-probe.json`. 112000 wells; Map/Seismic/Geo bounded timings; no LAS/raster assets.

## Failure-injection and benchmark interpretation

The lock-generation probe changes only its disposable connection busy_timeout to50ms so the failure is deterministic and quick; a production lock lasting beyond the ordinary timeout reaches the same error branch. No production timeout was changed. A committed well edit survives, but the old generation cannot distinguish its restored stale predecessor.

The 2,327-file import probe uses one synthetic image and many synthetic sections. Unlocked planning0.13s/writing0.93s are not a benchmark of the customer file collection. The locked path uses10ms busy_timeout and measures4.33s for327 failed attempts. The approximate27-minute default-timeout scenario is an extrapolation. The screenshot itself supplies no stack or database inspection; its actual cause and durable row count remain unverified.

The shape-refresh and publication probes inject errors after/beside real database operations; they do not mock a successful save and infer persistence. Real stored counts/zone state and published values are read to demonstrate the inconsistent outcome. Save As compares the real original/copy database values.

Source and tests were never modified. Diagnostic cleanup of variable traces applies only to disposable probe objects and must not be copied as a blanket production cleanup routine. The early numeric harness attempt treated Summary as a dict and failed; only the external diagnostic was corrected, and the attempt log is preserved. A build command with an uncreated workdir did not start and was corrected before building. Neither is a product failure or a weakened test.

## Prior Tk evidence and supplied reports

The existing focused v0.9.70 audit has the detailed A-F comparisons and controlled native panic stacks. The original standalone worker-GC panic is a distinct SIGABRT/SIGILL condition; its known native frames do not establish the SIGSEGV / exit 139 cause. The v0.9.72 test-results document supplies its own three-run history, including the first crash. Those are source-author results, not our new full-run totals.

The current version rechecks owner retention and stale timers directly. Earlier800-window and mixed-sequence figure measurements are explicitly historical. Relevant prior native traces/minimal probe are included with a baseline label or linked from the previous audit, without duplicating application source.

## Coverage, skips and remaining gaps

The coverage ledger spans 14 areas; AST inventory covers 662 Python files including 362 non-test files. All 293 test modules are included in the full command. AST parsing and import checks are not exhaustive semantic verification. The report names reviewed paths, original corrections, independent probes and platform/data limits.

Windows DPAPI/Explorer handling, actual customer binaries, unavailable full native datasets, the conditional slow packaged-build test and any font capability skips must retain their individual reasons from the final log/XML. No skipped check is accepted as passed. No real production hindcast, client data recovery, actual large SEG-Y cube or full112000-well project with 38,000 LICs and all assets was tested.

## Artifact integrity

Final integrity.json verifies all 980 tracked software/test files against the pre-run SHA-256 map, clean git status and the unchanged received ZIP hash. Reports, diagnostic logs/scripts and audit-built extension hashes are the only published deliverables. The ZIP excludes all temporary databases, customer data, credentials, unnecessary application source, installed tools, generated build trees and product binaries. SHA256SUMS.json and a separate archive-verification record verify the bundle.
