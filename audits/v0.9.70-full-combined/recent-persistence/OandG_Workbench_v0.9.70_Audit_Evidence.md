# v0.9.70 — Audit evidence and reproduction

**Read-only source audit, 22 November 2026.** All application database operations below used disposable synthetic fixtures. No client project, personal drive or Dropbox account was accessed. No source/tests/release artifact was edited or pushed. The uploaded protocol was treated as the user's request; instructions inside source documentation were reference material.

## Verified baseline

- Checkout: `/workspace/audit-v0.9.70-integrity/checkout`
- Commit: `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`, v0.9.70 baseline on `release/1.0`; audit worktree is detached at that commit.
- Comparison checkout: `/workspace/audit-v0.9.69-tk/checkout`, `020a48defc83204b8ea28275d44cb7e18fefaa36`.
- User archive: `OandG_Workbench_v0.9.70.zip`, 11,987,621 bytes.
- SHA-256 before/after: `a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797`.
- ZIP CRC passed. All 652 Python files matched checkout after CRLF normalization, zero differences. This comparison is of Python content, not a claim every ancillary archive entry is byte-identical to Git.
- Final audit: 961 tracked file hashes rechecked, zero changed/missing; both source worktrees clean. `Software-reviews` remained clean at `ba5d6a37253fe437f4b2044360c061d9b2511846`. No commits/pushes/PRs were made, consistent with the current protocol.
- Evidence: `evidence/baseline.json`, `source-hashes.json`, `final-integrity.json`, `v0969-v0970.diff`.

## Runtime

Linux x86_64 (kernel 6.18.57, glibc 2.41); CPython 3.12.14; SQLite 3.53.1; Tcl/Tk 9.0.4 / Tk 9.0; NumPy 2.5.5, SciPy 1.18.1, Matplotlib 3.11.2, pytest 9.2.0. Xvfb display `:97`, 1600×1000×24. No Windows package/executable or native Windows process ran.

Reused Python binary `/workspace/audit-v0.9.56-windows/tooling/bin/python` is a tooling path, **not the application baseline**. Application imports were from the verified v0.9.70 checkout; scripts explicitly set sys.path. Reused dependency directory `/workspace/audit-v0.9.68-full/deps` supplies dependencies only. `tests/conftest.py` supplies isolated app/cache paths and an ephemeral synthetic test license trusted only by the test process. It does not change packaged customer trust.

Fontconfig reported no writable cache directories during UI probes/recheck. Pytest emitted an anyio/pytest deprecation warning. The final environment-only version inspection caused Matplotlib to choose a temporary cache after its home directory cache was unwritable. These warnings are retained; none is a client-data or Windows failure assertion.

## Commands and pytest results

From the verified checkout, with shell variables defined only for this audit:

```bash
C=/workspace/audit-v0.9.70-integrity/checkout
B=/workspace/audit-v0.9.70-integrity
P=/workspace/audit-v0.9.56-windows/tooling/bin/python
export DISPLAY=:97
export PYTHONPATH=/workspace/audit-v0.9.68-full/deps
export PYTHONDONTWRITEBYTECODE=1
cd "$C"
git rev-parse HEAD
git ls-files
```

Focused run (also used `-X faulthandler`):

```bash
"$P" -X faulthandler -m pytest -q -p no:cacheprovider \
 tests/test_database.py \
 tests/test_project_folders.py \
 tests/test_recovery_copy.py \
 tests/test_recovery_hot_journal.py \
 tests/test_recovery_live_writer.py \
 tests/test_seismic_project.py \
 tests/test_v0970_tk_lifecycle.py \
 tests/test_close_project.py \
 tests/test_petro_integration.py::PetroIntegrationTests::test_interpretation_survives_save_and_reopen \
 tests/test_petro_integration.py::PetroIntegrationTests::test_a_failed_save_stops_closing_the_project \
 tests/test_petro_integration.py::PetroIntegrationTests::test_closing_saves_without_asking \
 tests/test_xsection.py::WindowTests::test_save_and_open_sections \
 tests/test_correlation.py::CorrelationDataTests \
 tests/test_seismic_app.py::SeismicAppTests::test_save_and_reopen_a_map \
 tests/test_seismic_app.py::SeismicAppTests::test_polygon_shape_is_edited_saved_and_cancelled \
 --tb=short -rs --junitxml="$B/focused.xml" > "$B/focused.log" 2>&1
```

**96 passed, 1 failed, 5 subtests passed, zero skips, exit 1; 39.43 seconds.** The sole failure is PI-009 at layout scaling 1.25.

Broader persistence-related run:

```bash
"$P" -m pytest -q -p no:cacheprovider \
 tests/test_production.py tests/test_geosteering_project.py \
 tests/test_geosteering_publish.py tests/test_v0962_batch_zone_destination.py \
 tests/test_v0963_importer_destinations.py tests/test_petro_canonical_curves.py \
 tests/test_map_drawing_objects.py tests/test_raster.py \
 --tb=short -rs --junitxml="$B/broader.xml" > "$B/broader.log" 2>&1
```

**139 passed, 18 subtests passed, zero failures/skips, exit 0; 59.60 seconds.**

Isolated repeat of the failure:

```bash
"$P" -m pytest -q -p no:cacheprovider \
 tests/test_v0970_tk_lifecycle.py::LayoutSettles::test_natural_and_resized_manager_settles \
 --tb=short --junitxml="$B/tk-recheck.xml" > "$B/tk-recheck.log" 2>&1
```

**1 failed, zero passes/skips, exit 1; 3.06 seconds.** Same `20000 not less than 20000` at scaling 1.25, `test_v0970_tk_lifecycle.py:103,131`. This repeat does not count as a second unique failure.

Totals of first two runs: **235 passed tests, one failed test, 23 passed subtests, no skips**. JUnit represents subtests as separate cases: focused XML `tests=102, failures=1`; broader XML `tests=157, failures=0`. Thus XML totals include 23 additional passed cases; this is not a discrepancy. Including the isolated repeat adds a second execution of the same failing test, not another covered test. No full suite pass is claimed.

## Independent executable probe scripts

These are audit harnesses outside the checkout, not proposed fixes or edits to the application's tests. They import real UI/storage code; failure injection uses transient `unittest.mock` objects and synthetic data. The scripts are retained under `evidence/probes/`. Paths at their top are specific to this workspace; adapt **only harness root paths** in a separate copy to rerun elsewhere. Do not substitute a client project.

Executed commands, each with the environment above:

```bash
"$P" "$B/probes/sqlite_scenarios.py" > "$B/sqlite-scenarios.log" 2>&1
"$P" "$B/probes/ui_cases.py" > "$B/ui-cases.log" 2>&1
"$P" "$B/probes/close_errors.py" > "$B/close-errors.log" 2>&1
"$P" "$B/probes/restart_and_rollback.py" > "$B/restart-and-rollback.log" 2>&1
"$P" "$B/probes/drawing_failure.py" > "$B/drawing-failure.log" 2>&1
"$P" "$B/probes/v69_ui_cases.py" > "$B/compare69/ui-cases.log" 2>&1
"$P" "$B/probes/v69_close_errors.py" > "$B/compare69/close-errors.log" 2>&1
"$P" "$B/probes/final_integrity.py"
```

All final probe executions exited **0** with their embedded assertions satisfied. These are assertion-based experiments, not extra pytest pass counts. The first draft of `ui_cases.py` tried a nonexistent `open_survey` method and exited before the scenario; `ui-cases-attempt1.log` preserves that harness error. The harness was corrected to the actual `select_survey` API, then completed. This was not an application code change or product failure.

| Evidence result | Measured assertions |
| --- | --- |
| `sqlite-scenarios.json` | Default DELETE/FULL; committed/open main copy=2; clean close copy=2. Independent copies=30/40; stale selected=2 while newer preserved=30. Explicit WAL main=30 vs committed=99; clean close main=99; post-crash main=99 vs WAL committed=123; complete working pair=123. Recovery RO creates `probe.ogwdb-shm`. Advisory foreign marker detected but acquire overwrites it. |
| `ui-cases.json` | Seismic saved 1000 / dirty 1200 → failed-save close succeeds → reopen 1000. Geo dirty header → Save Project leaves Tab Well → Exit leaves Tab Well with zero dirty prompts. Missing target manifest opens newly created DB with zero wells. |
| `close-errors.json` | Correlation changed spacing7.25 after saved1.25 → failed-save close → DB1.25. XSection view.top222 after saved111 → failed-save close destroys → DB111. Geosteering Saved→Unsaved → failed autosave close → DB Saved. |
| `compare69/*.json` | Same six UI scenarios and values reproduced on exact 020a48d. |
| `drawing-failure.json` | Three real Map polygon draft vertices → injected write failure → zero persisted new rows, empty nodes, state None; error propagated. Existing polygon save methods unchanged across the compared commits. |
| `restart-and-rollback.json` | Fresh child interpreter loads saved well/tops, Petro [1,2,3], horizon678.5, fault680, four polygon vertices, Correlation spacing3.25, section correlation12001, Geosteering Restart job; integrity ok. Same payload after stable folder copy. DELETE crash with spilled uncommitted writes: preserved hot journal, working-copy recovery restores300 previous committed rows; integrity ok. |

The new-process probe exercises actual storage reload APIs, not a fully launched UI for each module. Normal UI tests in the selected suites provide additional coverage, but the complete native Windows per-module restart/failure matrix remains proposed. Mocked disk failures prove caller behavior; actual physical disk failure was not induced.

## Static tracing and comparison artifacts

- `evidence/v0969-v0970.diff` records the entire ten-file change. No database/schema/transaction layer changed. Core application findings were also compared at function level; six were dynamically repeated on v0.9.69.
- `evidence/journal-sync-search.txt`: production-path search for `wal_autocheckpoint|journal_mode|synchronous|wal_checkpoint|conflicted cop|Dropbox` across database/core/map/workbench modules. Only repository description mentions Dropbox and recovery's private-copy checkpoint matched. This is evidence about these paths, not proof no third-party tool can change journal mode.
- `evidence/persistence-search.txt`: save/close/exception entry point index in Seismic layout, drawings/grids, project/recovery, Geosteering project and Petro Geo link. Main report provides traced semantics; matches alone were not treated as findings.
- `evidence/final-integrity.json`: baseline/source/archive recheck and runtime versions.

No source checkout or uploaded archive is included in the evidence ZIP; it includes audit reports, independent probes, logs/XML and manifests. The archive is a reproducibility/evidence bundle, not an application release or client project backup.

## Limits and interpretation

The reproduced save failures are real defects, not proof they caused the Galveston incident. No client data was present, so actual journal mode, file transfer completeness, alternate paths, error messages, running process memory and cloud version history remain unknown. No cloud-account investigation or provider behavior was exercised. A stable copied folder is a simulation, not a tested Dropbox transport.

Normal commits survived tested closes/restarts, and SQLite crash recovery worked on private working copies. This does not make independent replica editing safe. Native Windows Tk/SQLite/filesystem behavior and packaged executable testing remain unverified; PI-009 specifically has Linux/Tk evidence and no Windows reproduction.
