# v0.9.70 — Full combined audit evidence

**Baseline:** `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`, release/1.0.  
**Date:** 22 November 2026. **Application changes:** none.

## Source identity and audit boundary

Input ZIP:11,987,621 bytes, SHA-256 `a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797`. CRC passed;652 Python files match Git after CRLF normalization. All 961 tracked files rehashed unchanged after the full run; git status clean. `final-integrity.json` is the current check. The earlier audit's own baseline/final hashes are preserved as historical records; they are not overwritten.

The report consolidates PI-001–PI-009 once and adds FA-001–FA-008. Severity mapping of earlier P0/P1/P2 is Critical/High/Medium. The raw findings CSV carries each entry's origin and original severity. All client-project/sync incident statements remain bounded by no client access. Source documentation is reference, not authority to modify software or bump a version.

The application checkout, uploaded archive and existing release artifacts were not changed. Reports are separate artifacts. Publication of audit artifacts to Software-reviews follows the user's standing instruction; it does not modify O-G-WorkBench. No app fix/PR/release is part of this work.

## Environment

CPython3.12.14 on Linux x86_64, Tcl/Tk9.0.4, SQLite3.53.1; NumPy2.5.5, SciPy1.18.1, Matplotlib3.11.2 and pytest9.2.0. Python path `/workspace/audit-v0.9.56-windows/tooling/bin/python` is reused tooling, not the audited version. Dependencies `/workspace/audit-v0.9.68-full/deps` likewise supply libraries, not application modules. Source imports resolve into the exact v0.9.70 checkout.

Tests/conftest isolates user-data/cache settings and uses ephemeral synthetic license trust only inside test processes. No customer EXE trust was changed. Four owned Xvfb displays201–204 at 1600×1000×24 isolate suite groups; independent UI probes used205–208 and cleaned up those displays. OPENBLAS/OMP/MKL thread counts were 1 for the full run. This affects timing and is recorded rather than hidden. No native Windows execution occurred.

## Full suite commands and reconciliation

From `/workspace/audit-v0.9.70-full`:

```bash
python run_suite.py
python probes/summarize_suite.py
```

`run_suite.py` explicitly selects every 287 shipped `tests/test_*.py` module and asserts the four partitions' union equals that list exactly. It uses prior durations only to balance execution, never prior pass/fail results as current evidence. Each group executes:

```bash
/workspace/audit-v0.9.56-windows/tooling/bin/python -X faulthandler  -m pytest -q -p no:cacheprovider <exact-module-list>  --tb=short -rs --junitxml=<group>/results.xml
```

All exact argument arrays, environment/display choices and process exit codes are in `suite-plan.json`, `suite-commands.json`, `suite-status.json` and `run_suite.py`. This is all-module execution in four independent processes, **not a single serial run**. No test selection filter excludes a module. Conditional skip decorators remain active and are reported.

| Group | Passed | Failed | Skipped | Passed subtests | Seconds | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 826 | 0 | 0 | 235 | 835.12 | 0 |
| 2 | 696 | 0 | 3 | 275 | 332.97 | 0 |
| 3 | 858 | 2 | 4 | 98 | 590.11 | 1 |
| 4 | 736 | 1 | 2 | 557 | 458.02 | 1 |

**Totals: 3116 passed, 3 failed, 9 skipped, 1165 passed subtests.**

JUnit includes passed subtests as separate cases. The group XML case counts1061+974+962+1296 sum4293, matching3116 passed+3 failed+9 skipped+1165 passed subtests. There are no XML errors or aborted suite processes. The slowest group took835.12 seconds; sums of CPU/test durations are not wall-clock duration for four concurrent groups. Earlier235-pass persistence tests overlap and are not added again. Independent assertion probes also do not inflate pytest totals.

### Unique full-suite failures

- `tests.test_v0969_fonts_audit.RendererFonts::test_tk_only_font`: AssertionError: 'urw gothic l' != 'avant garde gothic'
- urw gothic l
+ avant garde gothic
 : ('avant garde gothic', False, False)
- `tests.test_v0970_tk_lifecycle.LayoutSettles::test_natural_and_resized_manager_settles`: AssertionError: 20000 not less than 20000 : the layout never settled (scaling 1.25)
- `tests.test_correlation.CorrelationAppTests::test_correlation_box_over_digital_logs_never_pans`: AssertionError: 6.296937045548732 != 6.300000000000001 within 6 places (0.0030629544512690288 difference)

### Conditional skips

- `tests.test_cython_build.CompiledBuild::test_a_patched_global_is_still_seen` — the protected modules are not compiled (tools/release/build_cython.py)
- `tests.test_cython_build.CompiledBuild::test_each_module_loads_as_its_extension` — the protected modules are not compiled (tools/release/build_cython.py)
- `tests.test_cython_build.CompiledBuild::test_same_results_as_the_python_source` — the protected modules are not compiled (tools/release/build_cython.py)
- `tests.test_v0958_fixes.ExpiryNotSavedAtOnce::test_dpapi_kept_expiry` — DPAPI is Windows' (a Windows qualification item)
- `tests.test_licensing.Clock::test_dpapi_round_trip` — DPAPI is Windows' (a Windows qualification item)
- `tests.test_pdf_packaging.PackagedBuildTests::test_packaged_pdf_import` — slow packaged build: set OGW_PACKAGING_TEST=1
- `tests.test_v0957_fixes.ExistingState::test_dpapi` — DPAPI is Windows' (a Windows qualification item)
- `tests.test_geo_tabs.GeoTabTests::test_files_dropped_from_explorer_reach_the_las_loader` — Explorer drops are a Windows message
- `tests.test_kingdom_native_full.FullKingdomValidation::test_every_fault_and_horizon_matches_the_export` — full Kingdom files not supplied (OGW_KINGDOM_NATIVE / OGW_KINGDOM_TRUTH)

The three failures are accounted for by PI-009 and FA-006. Repeated isolated executions are in `isolated-rechecks.xml/log` (Correlation+layout:2 failed, exit1,5.44s) and `font-recheck.xml/log` (Tk font:1 failed, exit1,1.31s). These are repeats, not additional unique failures. Their exact commands are in the adjacent command JSON files. Fontconfig no-writable-cache and some Matplotlib invalid-command idle_draw diagnostics were captured; they are not silently removed or declared geological corruption. Font alias/drag-coordinate causes remain appropriately qualified.

## Independent probes (synthetic data only)

Use the verified checkout and these environment variables:

```bash
export PYTHONPATH=/workspace/audit-v0.9.68-full/deps
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
P=/workspace/audit-v0.9.56-windows/tooling/bin/python
B=/workspace/audit-v0.9.70-full
"$P" "$B/probes/numerical_edges.py"
"$P" "$B/probes/cache_and_sources.py"
"$P" "$B/probes/digitizer_failure.py"
"$P" "$B/probes/scale_probe.py"
"$P" "$B/probes/map_parity.py"
```

Final executions all exited0 with their embedded assertions satisfied. Scripts and JSON/log outputs are included. Root paths are explicit for this workspace; adapt harness-only roots in a separate copy if reproducing elsewhere. Do not replace any synthetic target with a user project. The new UI probe uses a generated image, not client data. Existing suite raster tests also use a bundled real log fixture; that is not a field-data geological validation.

| Probe | Independent measured result |
| --- | --- |
| numerical_edges | TVD 1050→MD 2000→TVD 900 on an undulating survey; unique reference crossingMD2750; Geosteering first-crossing returns2750.0000000000005. All-pay TVD gross100/net275/N:G 2.75. EUR 100000/span 1000 without months returns no EUR/ft; one-month control returns100. BOE 200/GOR 6000/water-cut1/3 control passes. |
| cache_and_sources | Real imported/decode API,8 LasFile entries, default256 MiB budget, no item cap. Retained NumPy bytes3,840,384 versus accounting512 bytes,8 entries each64 bytes, no eviction. Arrays frozen as separate copies by production _freeze_run; no fabricated cache entries or lowered budget used. |
| digitizer_failure | Generated raster/project,2 new nodes, curve not yet exported. Injected node-store write error→finish True→window destroyed→database digitizing empty; prior status captured. |
| scale_probe |112,000 synthetic wells/locations; seed1.23s, Map load0.787s, changed-well refresh0.161s returning exactly[1], Seismic well load0.600s, Geo project/list load1.270s, list refresh0.985s,112K displayed rows, peakRSS380,192 KiB. No LAS/LIC/SEG-Y payloads. CPU competition and Linux runtime limit extrapolation. |
| map_parity |24 regular/Seismic data-path posting cases across metre/feet CRS, surface/BHL/survey fallback/invalid BHL; zero mismatches. Changed survey endpoint refresh/reopen also agrees. Data/coordinate checks, not a visual Windows screenshot certification. |

Initial harness attempts are retained where material: scale fixture first omitted required timestamps and then had a quoting syntax error; numerical pay assertion initially assumed300 instead of measured275 because a clipped cell straddles the turn. Those harness errors were corrected outside source. The final invariant remains net>gross, with exact observed275 recorded. They are not application failures or extra passing tests.

## Prior persistence evidence incorporated

`recent-persistence/` retains all five original deliverables, its untouched findings/report, logs/XML/probes, baseline/final hashes and the v0.9.69 comparison. It records six UI scenarios repeated on020a48d, the polygon draft failure, fresh-interpreter raw payload checks, defaultDELETE/FULL measurements, conditionalWAL/crash recovery, independent replicas/stale selection, read-only SHM side effect and advisory lock behavior. No client files were touched. The combined report carries those findings and their detailed persistence/scenario tables, without claiming the earlier targeted run was full-suite execution.

The new finding paths are byte-identical to v0.9.69 as recorded in `new-findings-v0969-comparison.json`; new findings were dynamically reproduced on v0.9.70, not dynamically re-run on v0.9.69 unless the earlier evidence explicitly says so. Prior v0.9.68 findings were reviewed against current corrections and current test modules, not automatically carried as open defects.

## Whole-tree review artifacts

- `static-inventory.json` and `static-inventory-summary.json`: AST/import inventory of 652 files,183,997 non-test lines/87,184 test lines; broad-exception counts are triage data, not bug counts. Sensitive-call matches use exact call names, not every SQL execute as an eval/exec alarm.
- `review-coverage.csv`:77 files with targeted manual path review versus wider automated inventory. It does not assert every line of those files was manually reviewed. No line/branch coverage percentage was collected.
- `icon-consistency.json`:35 statically literal icon_button calls checked against semantic ACTIONS, zero mismatches in that subset. Dynamic helpers/wrappers are a remaining visual-test boundary.
- `legacy-icons-reference-scan.json`: no tracked runtime import of ogmap.icons; two archived security-record path references are not callers. External consumers remain unknown.
- `new-findings-v0969-comparison.json`: byte comparisons for relevant unchanged paths.
- `final-integrity.json`: all 961 source hashes and supplied archive unchanged after testing.

The evidence ZIP contains audit materials, test logs/XML and reproducible harnesses, not an application release, customer package, private license key or client project backup. SHA256SUMS.json inventories bundled artifact bytes. Review PDF/Markdown/CSV were read back and validated; the immutable software hash checks remain separate from audit-publication Git commits.
