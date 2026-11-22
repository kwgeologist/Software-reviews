# O&G Workbench v0.9.70 — Full Suite Audit and Consolidated Findings

**Independent read-only engineering audit · 22 November 2026**  
**Baseline:** `release/1.0`, commit `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`  
**Input:** OandG_Workbench_v0.9.70.zip  
**Disposition:** correctness and save/close defects remain; do not regard the current release as fully qualified for v1.0 or live multi-computer project sharing.

## Executive assessment

This is the expanded **whole-suite audit**, combined with the recent project-integrity findings. Scope includes architecture, geological/numerical correctness, state/cache behavior, persistence, project switching, imports/exports, performance/resource management, tests, security/distribution source, legacy code and suite UI infrastructure. It covers all major workbenches and shared services. It is not limited to persistence, and it does not propose a UI overhaul.

The consolidated register contains **17 entries: 2 Critical, 8 High, 4 Medium, 1 Low and 2 Cleanup**. Nine retain their PI-001–PI-009 identifiers from the recent audit; eight FA entries come from the expanded review. Cleanup entries and unsupported-deployment risks are explicitly distinguished from reproduced defects. They are not 17 equally dangerous application bugs.

The most urgent findings are still Seismic and Geosteering releasing unsaved work after a failed save. The wider review adds a failed-save close path in Raster Digitizer, an incorrect inverse TVD→MD conversion for undulating surveys, inconsistent TVD pay net/gross on those trajectories, and a LAS-run memory budget that does not count its retained arrays. A smaller production metric defect omits EUR per foot when the well has EUR/perforations but no monthly history. No geological formula or workflow was changed.

**Full-suite execution:** 3116 passed, 3 failed, 9 skipped, with 1165 passed subtests across all **287 shipped test modules**. Four isolated test processes/displays were used, with no test modules deliberately excluded. This is whole-suite execution in partitions, not a serial-process or native-Windows qualification. The targeted 235-pass/one-failure persistence runs are retained as earlier evidence and are **not added** to this full-suite total. Independent numerical, cache, Digitizer, scale and map-parity probes are separate assertion-based experiments.

A 112,000-well synthetic metadata project loaded Map data in 0.79 seconds and refreshed Geo's full well list in 0.99 seconds here. The regular/Seismic map coordinate probes agreed in 24 posting/path cases. These results support retaining the compact shared data store and geometry services. They do not certify a 112,000-well client project with 38,000 LIC files, large rasters,200 layers and real SEG-Y volumes. The cache accounting defect is especially relevant to long sessions visiting many LAS runs.

The Galveston Island missing-work incident remains **unproven**: no desktop/laptop client files, matching sidecars, logs or Dropbox history were available or inspected. Older/incomplete/different copies, failed saves and conditional WAL omissions remain separate hypotheses. The audit does not assign fault to Dropbox or claim that all committed interpretations disappear on normal close.

All application code, tests, uploaded source ZIP and release material remain unchanged. No client project/account was accessed; experiments used temporary synthetic projects. No software fix, release or commit to the Workbench repository was produced. Audit-only publication to Software-reviews is separate from software changes, under the user’s standing instruction.

## Baseline and review coverage

The uploaded ZIP is 11,987,621 bytes, SHA-256 `a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797`; CRC passed. All 652 Python files matched the Git checkout after CRLF normalization. The Git tree has 961 tracked files. Its Python inventory is 358 non-test files /183,997 lines, and 294 test/fixture files /87,184 lines. The non-test count includes release/tooling and owner-side code as well as the customer application. There are287 test modules and seven supporting test Python files.

Every Python file received AST/import/risk inventory. Targeted manual path review covered core entry points and calculations in 77 files across all subsystems; subsystem tests and source scans covered the wider tree. This is a risk-based whole-codebase audit, **not a claim that every one of 184,000 source lines was manually reviewed or that all branches executed**. The file-level ledger records this distinction. No line/branch coverage percentage was measured or invented.

Runtime: Linux x86_64, CPython3.12.14, Tcl/Tk9.0.4, SQLite3.53.1, NumPy2.5.5, SciPy1.18.1, Matplotlib3.11.2 and pytest9.2.0. Reused tooling/dependency paths do not change the application baseline. Native Windows behavior, compiled customer extensions and the actual customer EXE were not run. Historical Windows licensing results from other releases are not presented as v0.9.70 package verification.

| Area | Current source paths and review focus | Executed evidence / limits |
| --- | --- | --- |
| Geo / Well Manager | database.py; geoworkbench/main_window.py, well_tab.py; identity, dirty editors, project lifecycle, well-list refresh | All module tests selected; real Save Project/Exit failure;112K metadata scale; fresh-process stored well/top reads. No real client project. |
| Map | ogmap/datastore.py, sources.py, bubbles.py, project.py, grids.py, drawing_tab.py; population/style/data invalidation, anchors, aliases, file publication | Entire Map test family;24 regular/Seismic posting cases; polygon Finish failure; map store incremental refresh.200 real shapefile layers not benchmarked. |
| Petro | calculations.py, depth_entry.py, workspace.py, geo_link.py; formulas, accepted/preview curves, independent axes, save/reopen | Entire Petro test family and shared formula/core/model tests; new inverse/pay probes; prior failed-detach protection tests. No independent petrophysicist calibration on client wells. |
| Seismic | app.py, project.py, interpretation.py, mapping.py, ogcore/segy.py; ownership, revisions, deletes/Undo, 2D/3D, maps, callback cleanup | Entire Seismic/Tk test families; current v0.9.69-fix regressions; close failure; WAL/crash tests. Large native Kingdom inputs unavailable; real customer EXE not run. |
| Geosteering | app.py, model.py, project.py, wells.py/job interfaces; trajectories, inverse behavior, job persistence and publishing | Entire Geosteering test family; failed autosave/close; fresh-process job and cross-engine inverse comparison. No changes to dip/steering models. |
| Correlation | app.py, store.py, table.py; direct picks vs layout state, mouse ownership, raster/curve cache | Entire Correlation test family; failed session close; isolated width assertion failure. Shared-renderer merger not warranted. |
| Cross Section | window.py, store.py/model; section-local vs global geology, state/templates and close | Entire XSection test families; failed section save/close; fresh-process section correlation. Native Windows scaling unqualified. |
| Raster / Digitizer | ograster/calibrate.py, digitize_ui.py, importing.py/pdf_import.py; image/control paths, nodes, accepted output and save failure | Entire raster/digitizer tests; synthetic failed node-save close; staged digitized output tests. No38K-image performance benchmark. |
| Batch / pay / production | ogcore/curve_calc.py, batch_zones.py, zone_destination.py, pay.py, production.py | All batch/pay/production tests; new TVD net/gross and missing EUR/ft probes; explicit units and destination collision regressions. |
| Grids / depth conversion / volumetrics | gridders.py, surface.py, gridding.py, velocity_model.py, ogvol/engine.py | Entire gridding/isopach/velocity/volumetrics families; reviewed unit/datum/blanking contracts; reference tests. Not an independent validation of every interpolation method on field data. |
| Infrastructure / imports / exports | project.py, recovery.py, safeio.py, api.py, curve_store.py, cache.py/lru.py, mapped_import.py, bulk_import.py, export_manager.py | Whole database/import/export/security test families; raw-data/restart/sync probes; actual LAS cache accounting. |
| Distribution / UI / legacy | tools/release/stage.py, check_protected.py, cython_modules.py, installer, theme.py/icons.py/text_style.py | Source/manifest checks, all build/security tests that can run;35 literal action/icon calls checked; dormant icon module scan. Compiled/native tests skipped as recorded. |

## Consolidated findings register

Severity translation preserves the prior intent: PI P0→Critical, P1→High, P2→Medium. The original PI evidence/report is retained unmodified in the bundle. Findings are consolidated here once, not duplicated under each module.

| ID | Severity | Finding |
| --- | --- | --- |
| PI-001 | Critical | Seismic discards an unsaved interpretation after a failed save or cancelled conflict |
| PI-002 | Critical | Geosteering treats a failed autosave as permission to discard a saved/project job |
| FA-001 | High | TVD-to-MD inverse can return a point with a different TVD on an undulating survey |
| FA-002 | High | TVD pay net and gross use incompatible measures on non-monotonic wells |
| FA-003 | High | LAS run cache does not account for its NumPy arrays, defeating its memory budget |
| FA-004 | High | Raster Digitizer permits closing after its node-state save fails |
| PI-003 | High | Geo Save Project reports all changes saved while dirty header edits remain; window Exit drops them |
| PI-004 | High | Opening an existing manifest with a missing database silently creates an empty project |
| PI-005 | High | Synced replicas lack a consistent snapshot handoff or stale-generation acceptance check |
| PI-006 | High | Drawing Finish clears editable vertices before the database write succeeds |
| FA-005 | Medium | Production EUR per foot is omitted when monthly history is absent |
| PI-007 | Medium | Correlation and Cross Section close after logging failed session/section persistence |
| PI-008 | Medium | Recovery read-only open may create a shared-memory sidecar on the original |
| PI-009 | Medium | The v0.9.70 Drawings layout regression still fails at scaling 1.25 on the audit platform |
| FA-006 | Low | Two GUI regression contracts remain dependent on font aliases or exact drag geometry |
| FA-007 | Cleanup | UI palette and ribbon metrics still have parallel definitions despite a shared theme |
| FA-008 | Cleanup | Legacy hand-drawn Map icon module has no tracked runtime callers |

### PI-001 — Seismic discards an unsaved interpretation after a failed save or cancelled conflict

**Severity:** Critical. **Classification:** Confirmed defect; real UI failure injection. **Confidence:** High.

**Files/lines:** `seismicworkbench/app.py:500–532,674–679,1696–1721,3031–3036`.

**Function/class:** `SeismicWorkbench.close_project, select_survey, save_now, on_close`.

**Current behavior and why it matters.** save_now returns False on SQLite/OSError and on conflict Cancel. close_project ignores it, calls close_survey (which clears interp), destroys windows and closes the database. select_survey likewise ignores False. on_close destroys the application in finally even if closing raises. Layout is saved before the interpretation, so a fresh database modification time need not mean picks were saved.

**Realistic failure / reproduction.** Run probes/ui_cases.py. Open the synthetic SEG-Y project, set Horizon 1[6,8]=1000 and save. Change it to 1200; inject sqlite3.OperationalError from store.save_interpretation; close and reopen.

**Expected.** Abort close/survey switch and retain the live interpretation until a successful save or explicit discard.

**Observed.** Project closes despite the save error; reopened pick is 1000, not 1200. Separate status text says work stays in the window, but close removes that window.

**Version comparison.** Reproduced identically on 020a48d; the v0.9.70 cleanup is after the same unchecked save.

**Recommended correction — not implemented.** Honor a single save outcome before any close, switch, callback cancellation or destruction; preserve state on failure/Cancel. Remove unconditional destroy on failed close. Show an actionable persistent failure.

**Regression tests.** Automate disk-full/I/O/locked-commit failure and conflict Cancel through Close Project, WM close and survey/project switch. Assert dirty objects/window/database remain, then retry and verify fresh-process stored values.

**Data/recovery implications.** Previously committed picks remain. Never-committed edits are normally recoverable only while the process still holds them; a WAL cannot recover edits never written to SQLite.

### PI-002 — Geosteering treats a failed autosave as permission to discard a saved/project job

**Severity:** Critical. **Classification:** Confirmed defect; real UI failure injection. **Confidence:** High.

**Files/lines:** `geosteering/app.py:2262–2301,2376–2397,2779–2793`.

**Function/class:** `GeosteeringWorkbench._autosave, _confirm_discard, on_close`.

**Current behavior and why it matters.** _confirm_discard flushes a pending autosave, but then returns True whenever job.path is set or in_project is True even if dirty remains True after that save failed. If an earlier autosave has already failed and cleared its timer, the same condition skips a retry. on_close releases resources and destroys the window.

**Realistic failure / reproduction.** Run probes/close_errors.py. Save a synthetic project job named Saved, change its name to Unsaved, mark_dirty, inject SQLite write failure in geosteering.project.save_job, then on_close and reload the job.

**Expected.** Keep the dirty job open after failure or require explicit informed discard.

**Observed.** The project closes and stored job name remains Saved; Unsaved is lost. _autosave only sets a status message before closing.

**Version comparison.** Reproduced identically on 020a48d; file unchanged in v0.9.70.

**Recommended correction — not implemented.** Make autosave report success and require dirty=False or explicit discard before releasing a job. Saved-path/project membership must not imply dirty work is durable.

**Regression tests.** Test pending autosave failure and already-failed autosave with no pending timer; test standalone .ogsteer and project jobs, lateral/job switch and close; verify segments/faults/targets as well as name.

**Data/recovery implications.** Older saved job/track survives; the failed newer interpretation may exist only in process memory. Preserve any still-running session before further actions.

### FA-001 — TVD-to-MD inverse can return a point with a different TVD on an undulating survey

**Severity:** High. **Classification:** Confirmed numerical defect; synthetic independent round-trip/reference check. **Confidence:** High.

**Files/lines:** `ogcore/depth.py:26–44,65–110,126–145; petroworkbench/depth_entry.py:95–107; database.py:4900–4928`.

**Function/class:** `linear_interpolate; complete_depth_triplet; DepthConverter.to_md; DepthReference.to_md; ProjectDatabase._time_depth_rows`.

**Current behavior and why it matters.** Inverse conversion swaps MD/TVD pairs and sorts by TVD, then connects neighbors in that sorted order. For a survey whose TVD falls and rises, those neighbors can belong to unrelated MD segments. The returned MD can fail the forward conversion even when the requested TVD has exactly one valid crossing. Petro typed depth fields and database time-depth/core conversion use this helper; Geosteering has a separate first-crossing implementation.

**Realistic failure / reproduction.** Run probes/numerical_edges.py with (MD,TVD) [(0,0),(1000,1000),(2000,900),(3000,1100)] and request TVD 1050.

**Expected.** Find an actual crossing in MD order, or refuse/ask for a branch if the inverse is not uniquely supported. A returned MD must map back to TVD 1050.

**Observed.** The shared converter returns MD 2000, whose forward TVD is 900. The unique crossing is MD 2750, which Geosteering independently returns as2750.0000000000005. This is not merely a choice among two valid roots.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Validate inverse monotonicity/branch conditions before accepting edits. Intersect the original MD-ordered segments and use an explicit, documented branch policy; do not silently sort TVD and interpolate unrelated segments. Obtain geological workflow approval for ambiguity handling.

**Regression tests.** Monotonic, plateau, reversed/upward and multiple-turn surveys; unique/multiple/no crossings; MD→TVD→MD where unique; Petro edited TVD/TVDSS fields and stored time-depth/core values. Include datum/unit conversion.

**Data/recovery implications.** Review TVD/TVDSS-entered depths for affected non-monotonic wells; retain original entered values and surveys. Normal forward MD→TVD and monotonic-well results were not shown wrong.

### FA-002 — TVD pay net and gross use incompatible measures on non-monotonic wells

**Severity:** High. **Classification:** Confirmed numerical/internal-invariant defect; geological treatment of re-crossings needs a decision. **Confidence:** High.

**Files/lines:** `ogcore/pay.py:146–167,175–215; ogcore/batch_zones.py (shared pay engine); petroworkbench/pay_picking.py`.

**Function/class:** `sample_support; summarize; PaySummary.ratio`.

**Current behavior and why it matters.** Gross TVD is max(0,TVD(base)-TVD(top)), but net sums absolute TVD differences of sample cells. An undulating interval can therefore have net greater than gross even when every sample is pay. The midpoint cell scheme can also straddle a turn, making the absolute sum depend on sampling. This contradicts the engine documentation that all-pay net equals gross and gives an invalid net/gross quantity for these intervals.

**Realistic failure / reproduction.** Run probes/numerical_edges.py on the FA-001 survey, MD 1000–3000 at 250-unit sample spacing with every sample pay, PHIE 0.2 and SW 0.3.

**Expected.** A clearly defined supported vertical-thickness measure, or explicit refusal/warning for the unsupported re-crossing geometry; do not silently publish an ordinary N:G above1.

**Observed.** Gross TVD 100; net TVD 275; N:G 2.75, while gross/net MD are both2000. Finer sampling can change the accumulated absolute TVD net. No new geological thickness convention was implemented.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Detect non-monotonic TVD within the interval and define supported behavior with geological input. Keep numerator/denominator consistent under that policy; do not hide the issue by clamping N:G to 1 or changing formulas broadly.

**Regression tests.** All-pay and subset-pay vertical/monotonic wells preserve existing values; undulating/upward/flat intervals explicitly handled; sample-phase refinement tests; batch and Petro produce the same documented outcome.

**Data/recovery implications.** Existing zone/pay outputs for these trajectories may need recalculation after an approved correction. Preserve raw curves, criteria, intervals and survey so results can be reproduced.

### FA-003 — LAS run cache does not account for its NumPy arrays, defeating its memory budget

**Severity:** High. **Classification:** Confirmed resource/scalability defect; measured accounting mismatch. **Confidence:** High.

**Files/lines:** `ogcore/lru.py:12–23,28–83; ogcore/curve_store.py:35–36,311–328`.

**Function/class:** `nbytes_of; BudgetCache; curve_store.run`.

**Current behavior and why it matters.** BudgetCache measures arrays and built-in containers, but assigns arbitrary objects64 bytes. curve_store.run caches a LasFile dataclass containing decoded arrays under the default size function. max_items is None. Thus the nominal256 MB budget does not bound the retained LAS-run arrays; visiting many runs can retain gigabytes, even though the individual-curve cache branch is measured properly.

**Realistic failure / reproduction.** Run probes/cache_and_sources.py: import8 independent synthetic LAS runs of 10001 samples, decode them through the real curve_store.run API, then compare cache.bytes with unique NumPy array bytes reachable from entries.

**Expected.** Cache accounting includes all retained run arrays and evicts old runs according to the advertised budget, with the documented allowance for one oversized current item.

**Observed.** 8 entries report512 bytes but retain3,840,384 unique NumPy bytes; no evictions, max_bytes268,435,456, max_items=None. No reduced budget or fake LasFile was used. Growth to thousands of visited runs is a source-supported extrapolation, not a measured38,000-file load.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Provide explicit retained-byte sizing for LasFile/other cached dataclasses or a safe per-cache size function; add an item cap if appropriate. Keep lazy loading and existing curve identity/immutability safeguards.

**Regression tests.** Use actual LasFile cache entries with many curves and raw matrices; force a small budget in tests, verify measured eviction and alias/shared-array accounting; exercise repeated wells/projects and check close cleanup without invalidating displayed data.

**Data/recovery implications.** No stored curve corruption was demonstrated. Memory exhaustion can terminate a session and expose pending unsaved work; prioritize after close/save protection.

### FA-004 — Raster Digitizer permits closing after its node-state save fails

**Severity:** High. **Classification:** Confirmed UI failure injection using a synthetic image/project. **Confidence:** High.

**Files/lines:** `ograster/digitize_ui.py:754–798; ograster/calibrate.py:1341–1366; database.py:3922–3931`.

**Function/class:** `DigitizeMixin._dig_finish/_dig_store; CalibrationWindow.close/save_and_close; set_raster_digitizing`.

**Current behavior and why it matters.** _dig_store(now=True) catches storage errors and only sets a status message; it returns no failure signal. _dig_finish continues and returns True when there are no already-exported edited curves needing re-export. In particular newly traced unsaved curves rely on node autosave, yet a failed node write does not veto close. The user is told nodes are kept as they go, but closing destroys the only newer draft.

**Realistic failure / reproduction.** Run probes/digitizer_failure.py. Open Digitizer on a synthetic raster, add a new2-node curve, inject sqlite3.OperationalError in DigitizeLink.store, call finish/close and query raster_digitizing.

**Expected.** Keep the editor and its nodes on a failed node-state save; allow retry or explicit informed discard before closure.

**Observed.** _dig_finish=True; calibration window destroyed; curve.saved=False;2 draft nodes; database digitizing string remains empty. The error exists only in status before the window disappears.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Return and propagate node-state save success, retain dirty nodes and refuse close on failure unless discard is explicit. Distinguish node persistence from publishing sampled LAS output.

**Regression tests.** New and exported edited curves, manual/auto-traced segments, edges, tracks and overlays; fail node persistence during timer, close, raster Save and Geo project-close. Assert exact JSON survives retry and cancellation retains the draft.

**Data/recovery implications.** An older digitizing JSON or accepted LAS may survive, but never-committed nodes generally do not after destruction. Do not present re-exporting old sampled curves as recovering the missing trace.

### PI-003 — Geo Save Project reports all changes saved while dirty header edits remain; window Exit drops them

**Severity:** High. **Classification:** Confirmed defect; real UI reproduction. **Confidence:** High.

**Files/lines:** `geoworkbench/main_window.py:868–875,2519–2577,2579–2587,2625–2635; geoworkbench/well_tab.py:194–203`.

**Function/class:** `WellDataManagerApp.save_project, on_close, close_project, _resolve_unsaved_edits; WellTab.dirty`.

**Current behavior and why it matters.** Save Project commits the connection but does not save dirty tabs, then reports All changes are saved as you work. Close Project invokes the dirty resolver, but window Exit/on_close bypasses it and closes the database.

**Realistic failure / reproduction.** Run probes/ui_cases.py. Load Tab Well, change the header well_name StringVar to Edited Draft, verify dirty(), invoke save_project and then on_close. Query wells from a new connection.

**Expected.** Save Project writes pending edits or states what remains unsaved; Exit invokes the same dirty resolver as Close Project.

**Observed.** Stored name is Tab Well after Save Project and after Exit; dirty-dialog call count is zero. Source emits the all-saved message.

**Version comparison.** Reproduced identically on 020a48d; relevant files unchanged.

**Recommended correction — not implemented.** Use one dirty-save/close coordinator for the main tabs and owned windows; only report all-saved when all relevant writers succeeded.

**Regression tests.** Exercise header/location/manual-data tabs through Save Project, menu Exit, WM close, Close Project and project switch. Test Save/Discard/Cancel and invalid fields; read database after process restart.

**Data/recovery implications.** The old well row is preserved. Unsaved form contents generally have no database/WAL copy after destruction.

### PI-004 — Opening an existing manifest with a missing database silently creates an empty project

**Severity:** High. **Classification:** Confirmed defect; real UI reproduction. **Confidence:** High.

**Files/lines:** `ogcore/project.py:180–203,307–319; database.py:1184–1203; seismicworkbench/app.py:454–500`.

**Function/class:** `Project.load, open_target, database_for; ProjectDatabase.__init__; SeismicWorkbench.open_project`.

**Current behavior and why it matters.** Manifest resolution supplies its database path without checking that the existing project target exists. sqlite3.connect uses create-if-missing behavior. When DB/ exists but its database has not synced, opening the manifest creates a new valid empty schema instead of reporting an incomplete project.

**Realistic failure / reproduction.** Run probes/ui_cases.py. Create only the normal manifest/folders in a disposable location (never remove an existing database), then open that manifest through SeismicWorkbench.

**Expected.** Open Existing refuses a missing manifest target and leaves the directory unchanged; explicit New Project can create it.

**Observed.** A new database is created and opened with zero wells. This is not overwrite of an existing database, but creates a competing empty artifact in a sync directory.

**Version comparison.** Reproduced identically on 020a48d; path/database layer unchanged.

**Recommended correction — not implemented.** Separate explicit create from open-existing, validate resolved manifest target, and open-existing with no-create SQLite semantics. Show the exact manifest and resolved database path.

**Regression tests.** Open a manifest with absent DB file, unavailable repository/drive, partial folder transfer and database path outside root. Assert no new DB/sidecars and a clear missing-target error; retain New Project creation tests.

**Data/recovery implications.** An empty replacement does not prove original data was deleted. Preserve it separately; locate the desktop DB, older versions, conflicted/alternate paths and matching sidecars without overwriting anything.

### PI-005 — Synced replicas lack a consistent snapshot handoff or stale-generation acceptance check

**Severity:** High. **Classification:** Confirmed architectural safeguard gap; conditional WAL and independent-replica risks reproduced; Dropbox incident unproven. **Confidence:** High.

**Files/lines:** `ogcore/safeio.py:201–270; seismicworkbench/app.py:454–500; ogcore/project.py:307–319,365–476; database.py:1184–1245,1796–1810; ogcore/handoff.py:278–312`.

**Function/class:** `SessionLock.holder/acquire; open_project; write_project_copy; ProjectDatabase connection/change_stamps; watch_close`.

**Current behavior and why it matters.** SQLite protects connections to one local database, not independent replicated files. Advisory per-module lock markers can lag synchronization and can be overridden; acquire itself overwrites the marker. No sync-complete/snapshot manifest, conflicted-copy reconciliation or last-accepted remote generation check was found in these project-open/save paths. change_stamps protects derived caches, not cross-computer handoff. App does not explicitly enable WAL; an inherited WAL remains possible.

**Realistic failure / reproduction.** Run probes/sqlite_scenarios.py: independent copies retain values 30 and 40; selecting a preserved older generation opens value 2 without warning. In explicit WAL mode, committed 99 is missing from a main-only copy (30); abrupt exit with committed 123 leaves main-only at 99; a disposable main+WAL pair recovers 123. Foreign marker is detected but acquire overwrites it.

**Expected.** A supported handoff delivers a verified consistent committed snapshot and rejects incomplete/missing targets; simultaneous editing is explicitly unsupported or coordinated independently of file sync.

**Observed.** Stale/incomplete copies can be accepted. Default DELETE committed-idle main-only copy retained value 2; do not generalize the conditional WAL failure to the default mode or claim Dropbox actually chose a stale file.

**Version comparison.** Same storage/project/lock paths in 020a48d. v0.9.70 only cancels the handoff polling callback when a window is destroyed.

**Recommended correction — not implemented.** Define single-writer snapshot handoff using SQLite backup plus a versioned manifest/checksums and explicit success acknowledgement. Validate completeness/identity at destination, make concurrent-use policy explicit, and never auto-merge SQLite replicas or checkpoint a live synced original.

**Regression tests.** Automate A–E in both DELETE/WAL, WAL without SHM, delayed sidecars/manifest/assets, independent replicas, split generation, stale/conflicted names and concurrent marker acquisition. Validate target hash/interpretation payload, not mtime alone.

**Data/recovery implications.** Newest committed data may remain on desktop, in matching WAL, versions or conflicted copies. Preserve each generation intact; do not copy arbitrary sidecars from another generation or choose winners by timestamps.

### PI-006 — Drawing Finish clears editable vertices before the database write succeeds

**Severity:** High. **Classification:** Confirmed defect; real UI failure injection for new polygon; same ordering in edited shape. **Confidence:** High.

**Files/lines:** `ogmap/drawing_tab.py:411–462,577–594; ogmap/drawings.py:156–178`.

**Function/class:** `DrawingsTab.finish, finish_edit; drawings.save`.

**Current behavior and why it matters.** finish captures nodes and calls cancel before validation/dialog/write. finish_edit similarly cancels before drawings.save. A database error propagates after the editor has already discarded its draft. Normal successful Finish commits through db.execute before tree/grid refresh.

**Realistic failure / reproduction.** Run probes/drawing_failure.py. Digitize three polygon vertices in a disposable regular Map, inject OperationalError in drawings.save, invoke Finish.

**Expected.** Keep the draft and editing mode on write failure, allowing retry or explicit discard.

**Observed.** Write error propagates, persisted row count is zero, nodes becomes [] and state becomes None. Test did not simulate a user Cancel or unfinished draft close.

**Version comparison.** finish/finish_edit bodies unchanged from 020a48d; the new disposal logic is not the source of this ordering.

**Recommended correction — not implemented.** Validate and persist first; only clear the active editing state after confirmed success. Restore or retain draft on all save errors and Cancel from subsidiary destination dialogs.

**Regression tests.** New/edit polygon, fault polygon, contour and external shape destination: inject validation/write/publication failure; assert original and draft vertices survive and retry writes once.

**Data/recovery implications.** Original persisted geometry survives a failed edit; a never-written new polygon normally has no recoverable DB record. Do not confuse post-commit UI hangs with this pre-commit failure.

### FA-005 — Production EUR per foot is omitted when monthly history is absent

**Severity:** Medium. **Classification:** Confirmed output omission; metadata-derived metric. **Confidence:** High.

**Files/lines:** `ogcore/production.py:349–356,396–398,488–501`.

**Function/class:** `summarize; _with_eur; _all_summaries`.

**Current behavior and why it matters.** summarize sets EUR and gross_span, then immediately returns for an empty chosen history before _with_eur computes eur_per_ft. _all_summaries explicitly includes wells with EUR/perforations but no production, so such wells are listed yet this metric remains missing. Bubbles or maps requesting the production EUR-per-foot metric omit them despite both inputs being available.

**Realistic failure / reproduction.** Run probes/numerical_edges.py: summarize([],eur=100000,gross_span=1000), compare a one-month control with the same metadata.

**Expected.** EUR/perforation span 100 per foot is available independently of monthly cumulative production, or a deliberate history requirement is explained consistently.

**Observed.** EUR 100000 and span 1000 are present, eur_per_ft=None; with one synthetic month the same metric is 100. Normal BOE/GOR/water-cut reference checks also pass.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Compute metadata-only derived values before the early return, keeping monthly-history metrics and geological/unit conventions unchanged.

**Regression tests.** No rows with EUR+span, missing EUR, missing/zero span, metric_values/all_summaries and Bubble source path. Verify month-dependent quantities remain absent when unavailable.

**Data/recovery implications.** No history is overwritten. Existing well attributes can support correct display after a narrow correction; a user-selected explicit EUR/span ratio is a separate source path.

### PI-007 — Correlation and Cross Section close after logging failed session/section persistence

**Severity:** Medium. **Classification:** Confirmed Correlation/Cross Section UI failures; additional Map line error-reporting path static. **Confidence:** High.

**Files/lines:** `correlationworkbench/app.py:522–546; correlationworkbench/store.py:403–407; xsection/window.py:2636–2649,2708–2720; ogmap/window.py:2569–2576`.

**Function/class:** `CorrelationWorkbench.close_project/quit_app; CrossSectionWindow._autosave/close; MapWindow._save_section_lines`.

**Current behavior and why it matters.** Correlation catches session-save exceptions and logs, then closes. Cross Section autosave catches all exceptions and close destroys regardless. Named and Last section saves are separate transactions. Map section-line save similarly logs a failure while keeping the in-memory visual change. No user retry/discard decision is required.

**Realistic failure / reproduction.** Run probes/close_errors.py. Save Correlation spacing 1.25, change to 7.25 and fail save_session during close: stored 1.25. Save named section view.top=111, change to 222 and fail save_section during close: stored 111, window destroyed.

**Expected.** Keep the unsaved session/section open or clearly offer retry/discard; save coupled named/Last state consistently.

**Observed.** Older session/section reappears after reopen with warning only in logs. Cross Section section-local correlations/faults/fills can also be inside this JSON; project top/fault picks already committed through shared APIs are a separate store.

**Version comparison.** Both UI failures reproduced identically on 020a48d; cited files/functions unchanged.

**Recommended correction — not implemented.** Return and honor save outcomes; preserve state and notify users. Wrap coupled section saves in one transaction. Apply the same outcome contract to Map line/settings saves.

**Regression tests.** Test close, new/open section, named/Last second-write failure, and Map line-save failure. Verify JSON payloads on fresh reopen plus visible error and retained dirty state.

**Data/recovery implications.** Old committed layouts remain; never-saved section-local annotations may be memory-only. A logged error is useful evidence but does not restore the discarded data.

### PI-008 — Recovery read-only open may create a shared-memory sidecar on the original

**Severity:** Medium. **Classification:** Confirmed synthetic filesystem side effect; no user file opened. **Confidence:** High.

**Files/lines:** `ogcore/recovery.py:139–181,183–213; database.py:1217–1245`.

**Function/class:** `ReadOnlyProject._open/_recovered_copy; ProjectDatabase.reader`.

**Current behavior and why it matters.** mode=ro prevents SQL updates to the main DB, but SQLite can create/write WAL shared memory when the directory is writable. Recovery first tries that connection on the supplied path; its private-copy recovery fallback is reached only after an error. Therefore read-only is not a guarantee of zero filesystem side effects.

**Realistic failure / reproduction.** Run probes/sqlite_scenarios.py. On a disposable committed WAL pair with no SHM, instantiate ReadOnlyProject and inspect directory entries before/while open.

**Expected.** A forensic zero-touch mode performs all SQLite work on a working copy and preserves original files byte-for-byte.

**Observed.** probe.ogwdb-shm is created on the supplied synthetic path; the WAL value 123 is readable. No main-file SQL write was alleged. Existing recovery tests do not cover this absent-SHM/writable-directory combination.

**Version comparison.** Identical recovery/reader code in 020a48d.

**Recommended correction — not implemented.** Offer explicit copy-first forensic inspection and document normal read-only reader side effects. Do not use immutable=1 as a blanket solution: ignoring WAL can omit committed data.

**Regression tests.** Hash/list main, WAL, SHM and journal before/after on writable/read-only directories, missing SHM and hot journal, with a writer present. Assert the original is never opened by SQLite for forensic inspection.

**Data/recovery implications.** Use preserved raw evidence plus a separate disposable working copy. Existing private-copy recovery/backup can be useful there; never checkpoint, repair or open the live original merely to inspect it.

### PI-009 — The v0.9.70 Drawings layout regression still fails at scaling 1.25 on the audit platform

**Severity:** Medium. **Classification:** Confirmed Linux/Tk test failure; Windows impact and exact remaining geometry cause unverified. **Confidence:** High for test failure; Medium for operational exposure.

**Files/lines:** `tests/test_v0970_tk_lifecycle.py:100–131; ogcore/scrollframe.py:85–109,117–172; ogmap/drawing_tab.py:151–165`.

**Function/class:** `LayoutSettles.test_natural_and_resized_manager_settles; ScrollFrame.update_layout/_schedule; DrawingsTab._wrap_hints`.

**Current behavior and why it matters.** The shipped bounded event-drain test reaches 20,000 events instead of settling at scaling 1.25. It fails in the combined run and alone. This prevents accepting the Tk fix as fully verified on this platform; it is not evidence that persisted interpretation rows disappeared.

**Realistic failure / reproduction.** Run the exact isolated Tk recheck in Audit_Evidence.md using Xvfb, Tcl/Tk 9.0.4 and the recorded dependencies.

**Expected.** The manager settles within the bounded drain at all tested scalings, without geometry feedback starving useful UI work.

**Observed.** Assertion 20000 not less than 20000 at scaling 1.25; 1 failed in 3.06s. Fontconfig cache warning also present. No Windows/customer-EXE reproduction was performed.

**Version comparison.** Related geometry-loop exposure existed in v0.9.69; this new test is absent there. Do not call the exact failure a proven new v0.9.70 regression.

**Recommended correction — not implemented.** Investigate the remaining geometry feedback under the recorded environment; fix only after tracing it. Keep bounded tests; do not infer a persistence fix from UI responsiveness alone.

**Regression tests.** Repeat on packaged Windows/Tk and Linux at 100–200% scaling, with actual event/geometry traces; verify Finish commits before refresh and remains responsive.

**Data/recovery implications.** A UI stall after Finish can occur after commit. Inspect preserved copies for the polygon record before assuming loss or re-digitizing; force-killing can discard other pending memory edits.

### FA-006 — Two GUI regression contracts remain dependent on font aliases or exact drag geometry

**Severity:** Low. **Classification:** Confirmed test failures on Linux; not established as numerical/data-loss defects. **Confidence:** High for failures; Medium for exact cause of Correlation width difference.

**Files/lines:** `tests/test_v0969_fonts_audit.py:35–48,63–69; tests/test_correlation.py:291–303,601–635; correlationworkbench/table.py:1199–1215`.

**Function/class:** `RendererFonts.pick/check/test_tk_only_font; CorrelationAppTests.test_correlation_box_over_digital_logs_never_pans; mouse; _clamped`.

**Current behavior and why it matters.** Font tests require the actual family string equal an enumerated Tk alias, although Tk can canonicalize a family alias. The Correlation test requires a six-decimal physical width from a real MouseEvent/capture/viewport path. The latter still fails after the v0.9.69 edge-aware fixture change. These failures need narrower diagnosis and platform-aware assertions, not automatic dismissal or silent tolerance widening.

**Realistic failure / reproduction.** Review the full-suite XML/logs and isolated-rechecks.log. Repeat the Correlation case and the native-font case on the recorded environment.

**Expected.** Tests distinguish accepted font alias/canonicalization and viewport/pixel behavior from true wrong-font or drag defects; unexpected GUI callbacks are captured.

**Observed.** Font expected avant garde gothic, actual urw gothic l; Correlation expected6.300000000000001, actual6.296937045548732. Correlation repeats alone; native-font isolated result recorded separately. Some logs also contain an invalid-command idle_draw callback warning, which is not treated as proof of a leak without ownership tracing.

**Version comparison.** Related display-dependent tests existed in v0.9.68; current Correlation fixture and Tk font test are v0.9.69 changes. Source inspection supports residual portability issues rather than a new v0.9.70 storage regression.

**Recommended correction — not implemented.** Diagnose event coordinates and alias mapping, then make assertions reflect the real contract without concealing visible regressions. Do not change renderer or geological workflows to satisfy a fixture.

**Regression tests.** Use known equivalence/capability checks for font aliases, record event data/canvas geometry and assert the documented clamp/drag policy at physical-pixel resolution; test no-pan separately; run Windows DPI/font matrix.

**Data/recovery implications.** These failures alone do not show corrupted geological data. The separate PI-009 geometry non-settling failure remains a Medium operational issue, not merged into this Low test finding.

### FA-007 — UI palette and ribbon metrics still have parallel definitions despite a shared theme

**Severity:** Cleanup. **Classification:** Architectural concern for a later consistency pass; stylistic differences are not defects. **Confidence:** High.

**Files/lines:** `ogcore/theme.py:14–35,65–143; ogcore/icons.py:105–119,204–248; petroworkbench/constants.py:5–25; correlationworkbench/app.py:30,94–103; xsection/window.py:286–298`.

**Function/class:** `theme.apply; icons.icon_style; module ribbon styles and Petro constants`.

**Current behavior and why it matters.** Shared theme/icons already centralize most common controls. Petro repeats several palette literals; Correlation and Cross Section define separate ribbon colors/font sizes/padding under safely separate style namespaces. This permits drift but is not evidence a full UI rewrite is needed. The consistency requirement can be met by sharing semantic tokens while keeping layouts/renderers independent.

**Realistic failure / reproduction.** Compare palette/ribbon definitions and icon-consistency.json;35 statically literal icon_button calls were checked against the canonical action map, with zero mismatches in that subset.

**Expected.** A later approved consistency pass uses shared dimensions/palette roles and the same canonical icon for the same action while preserving module-specific layout behavior.

**Observed.** Duplicate colors and varying ribbon metrics exist. No universal icon mismatch was established; dynamic/wrapper calls and every visual state were not exhaustively compared.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Later consolidate duplicated chrome tokens and reusable ribbon/dropdown treatment incrementally. Keep existing namespaced styles, layouts and independent renderers. No redesign now.

**Regression tests.** Action-to-icon registry assertions plus representative toolbar/dropdown/tab/header/status snapshots at multiple DPI and module-open orders; keep semantic plot colors separate from chrome.

**Data/recovery implications.** No data-recovery consequence; avoid spending release-risk budget on cosmetic changes before the correctness/save failures.

### FA-008 — Legacy hand-drawn Map icon module has no tracked runtime callers

**Severity:** Cleanup. **Classification:** Confirmed no tracked import/reference found; external integrations not supplied. **Confidence:** Medium.

**Files/lines:** `ogmap/icons.py:1–79; ogcore/icons.py:1–119`.

**Function/class:** `ogmap.icons._draw/image`.

**Current behavior and why it matters.** ogmap/icons.py implements the older20-pixel hand-drawn navigation icons. Current suite controls use the canonical ogcore icon sheet. Whole-tree import/reference scans found no tracked caller/import of the legacy module. This is a contained superseded implementation, not a reason to merge renderers or remove compatibility code generally.

**Realistic failure / reproduction.** Inspect static-inventory.json import graph and legacy-icons-reference-scan.json. Search tracked source/scripts/build declarations for ogmap.icons, from ogmap import icons, relative icon imports and literal module loading.

**Expected.** Keep only one supported icon implementation in active use, with explicit compatibility policy if an external caller still needs the old API.

**Observed.** No tracked runtime reference found; only the legacy module itself defines this implementation. The scan cannot rule out an external consumer importing it.

**Version comparison.** Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.

**Recommended correction — not implemented.** Document it as dormant/superseded. Remove only after confirming no external API commitment; do not delete it during this audit. Leave other legacy migrations that still have readers/tests alone.

**Regression tests.** Import/launch/package smoke tests and canonical navigation icon checks after any future removal; verify no external integration contract first.

**Data/recovery implications.** None; the original file remains unchanged.

## Persistence and durability map

“Committed” below means SQLite accepted the commit under its configured journal/synchronous behavior; it does not mean Dropbox has copied the database or all external files. Close does not itself commit arbitrary unfinished SQL transactions. Normal helper methods own their transaction and commit; unsaved UI forms/drafts exist outside those transactions.

| Data / owner | Durable location and write boundary | Error, close and reopen behavior |
| --- | --- | --- |
| Project identity / DB | `.ogwproject` JSON selects `DB/<name>.ogwdb`; legacy `.ogwdb` supported. `ogcore/project.py:180–234,307–319`; database ctor `database.py:1184–1245`. | Manifest save uses temp+replace. Relative DB path normally portable; absolute targets accepted. Open may create/migrate/normalize and must not be used on forensic originals. Missing target defect PI-004. |
| Shared project database | `ProjectDatabase.transaction/atomic/execute`, `database.py:1723–1789`; `project_meta` via `1868`. Per-module connections to resolved path; worker `reader` uses mode=ro. | Outer atomic controls commit/rollback, helper nesting uses savepoints; failed commit rolls back. Local concurrent connections serialize writes; not independent replicas. No explicit production WAL enable/checkpoint. |
| Geo wells, locations, surveys | `wells`, `locations`, `deviation_points`, etc.; row/import helpers commit, `store_survey` at `database.py:4697`. Header/location forms have dirty UI state until tab Save/resolver. | File Close Project honors dirty Cancel; window Exit differs (PI-003). Refresh/revisions detect other local connection changes. A well ID is project-local, not a cross-project identity. |
| FM definitions, aliases, picks, sources | `top_definitions`, `top_aliases`, `formation_tops`, faults/picks; Global Manager uses database API. `delete_top_definition:3338–3344` deletes linked picks, aliases and definition in one transaction. | Global delete is intentional durable removal. Saved layouts may retain historical style references; distinguish styles from actual picks. No blanket top deletion/migration explanation for missing seismic interpretation was found. Existing canonical-definition/source filtering must be preserved. |
| Seismic 3D horizon/fault interpretation | `seismic_horizons` compressed float grids and `seismic_faults` JSON by survey; registry in `seismic_interpretations`. `seismicworkbench/project.py:375–483`. Edits in memory → 1500 ms autosave or Save now. | One write transaction checks baselines under write lock and writes changed/deleted objects; absence from partial load is not deletion. Errors return False. Close/survey switch ignores False (PI-001). Reopen reads selected survey ID/geometry, not arbitrary current external names. |
| Seismic 2D / ties / map views | `seismic_2d_picks` tied to interpretation/line IDs; survey maps, display and layout JSON via Seismic stores/layout. Data and view state have separate write boundaries. | A successfully saved layout or footprint can change DB timestamps even if interpretation save fails. Confirm actual pick blobs/JSON/IDs, not mtime or a refreshed tree. Direct SQL inspection should include all survey/line identities on a working copy. |
| Map polygons / fault polygons / contours / vertices | `map_drawings` stores points, style, visibility; `ogmap/drawings.py:156–178`; Finish/Finish edit `drawing_tab.py:411–462,577–594`. Some destinations can publish to shape layers instead. | Normal Finish commits before refresh/fault-grid callbacks. Unfinished Cancel/close intentionally drops a draft; global project Save does not imply Finish. Failed Finish clears draft before commit (PI-006). Post-commit GUI stall does not prove row loss. |
| Map configuration / selections / layers | Database JSON/meta plus layer tables; `ogmap/project.py` marker/label settings `970–978`, `ogmap/window.py:2569` section lines, project-owned Shapes/Map Images, external layer paths. | Many setters persist immediately; some settings/line errors only log (PI-007 static extension). Close cancels background/read/draw callbacks, not a universal deferred settings-save barrier. Active previews/drafts are not durable until applied. |
| Petro | Canonical LAS/calculated curve records, `petro_states`, accepted intervals/settings and arrays. `database.py:5048–5091`; `petroworkbench/geo_link.py:1175–1212`. Accepted curves differ from preview. | save_geo_project visits loaded workspaces. Failed detach asks whether to discard, default No keeps work; focused failure/normal reopen tests passed. State/accepted-curve transactions are not proof every separate zone/batch publication shares one global transaction. |
| Correlation | Shared top/fault picks committed through shared APIs; session/layout JSON in `project_meta['correlation:session']`, styles separately. `store.py:403–407`, app close `522–546`. | Session flush failure is only logged and project closes (PI-007). Do not equate losing layout with deleting already committed project picks. |
| Cross Section | Shared project picks; named sections and Last section/template JSON in `xsection_items`, `database.py:3738`, `xsection/store.py:443`. JSON can contain local correlations/faults/fills. Autosave 1500 ms and close. | Named/Last writes separately committed; `_autosave` logs failures, close destroys (PI-007). Reopening filters source/state according to current code; raw JSON is needed to distinguish hidden from absent. |
| Geosteering | `geosteer_jobs` JSON and map zone-track by lateral well; `geosteering/project.py:283–305`; standalone `.ogsteer` file path alternative. Source curves/surveys from shared DB. | mark_dirty schedules 1500 ms autosave. Successful project save uses committed db.execute. Failed autosave leaves dirty; close incorrectly accepts it (PI-002). Publishing results/tops is separate from saving the job. |
| Grids / control points / generated surfaces | Grid records/settings plus grid files, project Grids/Control Points roles and external paths. `ogmap/grids.py:592–723`. | File publication is staged with database atomic/revision ownership safeguards; not a distributed DB+file transaction for Dropbox. Recomputable cache differs from interpreted control data; preserve both during evidence capture. |
| LAS / rasters / registration / digitizer | Canonical accepted curve samples in DB; source LAS references; LIC/raster image and registration references, project LIC/Digitized roles or external repositories. | Source images/control files may be required for display even if database rows exist. Digitizer publication uses staged files/database writes; targeted raster/import tests passed. Missing external file is not automatically lost DB interpretation. |
| Production / batch / pay / zones | Production and calculated attributes/curve samples/zone/pay/definition tables in same DB, with batch selection/destination guards and per-operation transactions. | Targeted production, canonical curve, destination/import/publish tests passed. Long-running unaccepted previews or uncommitted jobs are not protected by copying the DB. Full power-failure/large-project/per-platform matrix remains unrun. |
| Settings / repositories / backup | Project settings mostly DB/manifest; named `@repository/...` roots resolved from per-machine config; external absolute paths also allowed. `ogcore/repositories.py:155,268–294`; `database.py:2486`. | Repository root can differ between PCs; matching names need not mean matching file contents. A Backup folder role exists, but no automatic versioned project backup/handoff writer was found in the audited save/close paths. Explicit SQLite backup copies exist. |

## SQLite scenarios A–E: observed results

Fresh synthetic Workbench database: **journal_mode=DELETE**, **synchronous=2 (FULL)**, wal_autocheckpoint=1000 (irrelevant until WAL). The application does not explicitly set WAL or enforce a journal policy. SQLite journal mode persists in an existing database; the client's actual mode is unknown. These results are from local filesystem experiments, not a Dropbox provider emulator.

| Scenario | Result | Interpretation |
| --- | --- | --- |
| A: commit, keep connection open, main-only copy, default DELETE | Pick value 2 retained. | An idle open connection alone did not keep a successful DELETE-mode commit outside the main file. Copying while an actual transaction modifies pages is still unsafe. |
| B: clean close then copy, DELETE | Value 2 retained. | Successful commit plus all connections closed worked for this fixture. |
| A: explicitly inherited WAL, commit and main-only copy | Committed 99; copied main showed prior 30; WAL 12,392 bytes. | Conditional committed-data omission reproduced. Do not assert user database was WAL. |
| B: all connections cleanly closed, WAL | Main-only copy showed 99. | SQLite's normal final-close checkpoint succeeded in this synthetic case. Do not rely on this after crashes or with another connection still open. |
| C: process exits abruptly after WAL commit | Main-only showed 99; committed 123 recovered from a separate complete main+WAL working pair. | Missing main-file changes can be recoverable from the matching WAL. Never delete it. |
| C: DELETE uncommitted page-spilling transaction, abrupt exit | Hot journal preserved; working-copy recovery restored all 300 prior committed rows, integrity_check=ok. | Uncommitted NEW rows are not expected to survive; SQLite recovery is necessary before interpreting raw pages. |
| D: independent desktop/laptop copies | Desktop 30, laptop 40, each locally valid. | Local SQLite locks do not serialize independent replicas. No automatic merge is safe. |
| E: provider-selection simulation into a new destination | Older 2 accepted; newer 30 preserved separately. | Simulated stale selection reproduces missing-newer-interpretation appearance. Workbench did not perform the file replacement; no actual Dropbox behavior was exercised. |

A raw copy of a live database and separately copied sidecars can mix generations even if every filename arrives. Consistent DB snapshot plus a stable external-asset set is the relevant unit. SQLite backup supplies a transaction-consistent database image; copying an entire project while assets change does not make those assets atomic with that image.

## v0.9.70 regression interaction

The v0.9.69→v0.9.70 delta changes Tk lifecycle/geometry, handoff polling cleanup, drawing key binding ownership, deferred tree scrolling and callback/trace disposal. It does not change database schema/transaction code, interpretation save algorithm, manifest resolution or Geosteering/Geo close logic.

Seismic still calls save_now before closing the survey and before the newly added map/app cancellation. The added cancel_jobs cancels tree-scroll/well-filter and map redraw/poll jobs, not an interpretation writer ahead of its save attempt. Drawing disposal intentionally cancels an unfinished editor; successful Finish still commits before grid/tree refresh. No additional v0.9.70-specific committed-data deletion path was demonstrated. PI-001 survives because a failed save result is ignored, not because the new cleanup moved ahead of it. Destroy called directly is lifecycle cleanup, not a durable save API.

The new layout test nevertheless fails at 125% scaling here (PI-009). The old synchronous tree update_idletasks was removed; therefore the old precise post-commit hang chain cannot simply be declared unchanged. Remaining geometry responsiveness and actual Windows behavior require their own traces/tests. No conclusion about the client's screenshot or November incident follows from this Linux failure alone.

## Whole-suite architecture and shared geological models

**The suite already has substantial shared infrastructure.** Keep that investment and the independent renderers. Wells/UID/API live in the shared database and ogcore.api; canonical FM definitions/aliases/picks are database services; curve identity/precedence/arrays use ogcore.curve_store and curve_aliases; accepted curves are distinct from previews; pay calculations are shared by Petro and batch; common depth/unit/repository/geometry services exist; Map uses compact column arrays and revision-domain invalidation; theme/icons provide common chrome.

The concrete architectural weakness is **inconsistent save outcome ownership**, demonstrated by PI-001/002/003/006/007 and FA-004. Each UI has its own dirty/autosave/close policy; some preserve state and some destroy it after errors. A small consistent success/failed/cancelled/discard contract and close coordinator is justified. Replacing frameworks, merging renderers or decomposing large modules for elegance is not justified by this evidence.

| Shared concept | Current authority / coupling | Assessment |
| --- | --- | --- |
| Wells / API / UWI | database well_uid/project-local id; ogcore.api.api14 and matching helpers; import-target guards | Full14-digit sidetrack/completion identity is preserved by the shared matcher; mapped spreadsheet reader normalizes integral numeric cells before matching. Production has a documented, ambiguity-checked short-API fallback. Do not unify these by truncating all APIs to 10 digits. Non-US identifiers need their supported path, not automatic API coercion. |
| Tops / aliases / sources / faults | Canonical definition IDs, aliases and source-normalized picks; per-module display state separate | Definitions/picks/styles are different things. Rename/merge retargeting and alias resolution exist, including map sources. A stale style name alone does not prove a pick survived deletion. Intentional global deletion is transactional; client LO/BMB/source contents were not available here. |
| Curves / units / sampling | Shared canonical samples/axes and origin precedence; per-view display models | This is a useful separation. Independent-axis statistics were corrected in v0.9.69. Actual sample-position compatibility is checked before multi-curve calculations. Preserve explicit resampling and raw percent/decimal semantics. FA-003 is a cache sizing failure, not a need for a new curve model. |
| Directional surveys / coordinates / depth | Shared well geometry and depth helpers; Geosteering has a minimum-curvature Trajectory plus explicit first-crossing inverse | Different interpolation/rendering contexts are legitimate, but FA-001 shows an actual inconsistent inverse. Fix the unsupported mathematical condition narrowly; do not merge all independent path/rendering implementations. |
| Horizons / faults / grids | Stable interpretation registry and per-survey picks; grid row/file publication and derived caches | Seismic has object conflict checks under its write lock and fixed deletion tombstones. DB/file publication is locally coordinated, not a distributed snapshot. PI-005 remains the relevant sync concern. |
| Selections / handoffs | ogcore.well_selection and handoff requests in project settings; UI polling | Shared selection is not a global synchronous save barrier. Destination-lock/frozen-target tests exist for imports/batch. A close request is not proof all modules saved successfully. |
| Paths / external assets | Project roles, relative paths and repository tokens; per-machine repository roots | Preserve deliberate external references and missing-source diagnostics. Make exact resolved paths/identity visible at handoff. A source folder and a client package are separate artifacts. |
| Colors / styles | Shared theme/icons/TextStyle plus renderer-specific plot styles | Namespace separation avoids opening one module changing another. Share chrome tokens later (FA-007); keep scientific color maps/styles and renderers independently configurable. |

The database and application controllers are large, but line count alone is not a finding. Lazy imports connect project/database/domain services; broad AST dependency edges include imports intentionally inside functions and do not prove an import-time circular failure. No new startup circular-import defect was established in this run. Targeted whole-object last-writer paths remain a maintenance/sharing risk, not evidence the app is broken for every single-user workflow.

## Numerical correctness: confirmed defects versus preserved contracts

FA-001 and FA-002 are material correctness findings with explicit reference values; do not dismiss them as presentation issues. For the undulating survey, the TVD 1050 inverse has a unique true crossing atMD2750, yet the shared converter returnsMD2000/TVD 900. For the pay interval, all-pay MD thickness2000 maps to endpoint grossTVD100 and reported netTVD275/N:G 2.75. The correct handling of re-crossed beds needs a geological decision; silently clipping results would conceal the defect.

Other inspected contracts did not justify algorithm changes:

- Minimum curvature uses standard dogleg/ratio-factor geometry with clipped cosine and the zero-dogleg limit. Geosteering retains explicit path/frame/dip conventions and separate units. Negative-below-sea-level TVDSS is documented; velocity-model “TVD” below seismic datum is explicitly distinguished from well TVD below KB.
- Time/depth conversion uses TWT/2, explicit seconds/milliseconds and ft/metres factors. Isopach checks domains and brings depth references/units together; it does not claim true stratigraphic thickness without dip. Do not add a dip correction under the guise of cleanup.
- Pay cells clip midpoint support to zone boundaries and reuse weights for net/averages on supported trajectories. Percent/decimal values and cutoffs are explicit, not inferred from magnitude. Raw petrophysical outputs are intentionally not automatically clamped.
- Formula evaluation has an AST allowlist, restricted NumPy numeric functions and empty builtins. Seeing eval in a scan is not proof of arbitrary code execution. The multi-curve engine checks actual depth positions, including origins, rather than only sample intervals.
- Multimineral inversion includes closure, measurement uncertainty and rank/ambiguity QC; multivariate fitting distinguishes sample masks and target transforms. Tests provide useful synthetic reference coverage. They are not proof a chosen endpoint set/model is geologically appropriate for every client's formation.
- Production BOE, gas/liquid conversion, GOR and water-cut references matched the independent simple control:100 bbl oil +600 Mcf gas yields200 BOE, GOR 6000 scf/bbl and water-cut1/3 for 50 bbl water. FA-005 concerns an omitted metadata metric, not these arithmetic formulas.
- Volume calculations separate geometry mode, physical units, fractions and positive FVF validation. This audit did not find evidence warranting changes to the established7758 oil volumetric coefficient or the documented area/datum conventions.

Tests used synthetic fixtures for the new numerical probes. Existing suites also use bundled real raster/navigation examples; no client's mature production history, interpreted survey or geological calibration dataset was supplied. No field-data accuracy certification is claimed.

## Performance, scalability, memory and resource assessment

### Measured checks

The independent scale probe created112,000 synthetic wells/locations, without LAS/raster/seismic payloads. On this Linux machine while other test processes competed for CPU: seed1.23s; Map store load0.787s; refresh one changed well0.161s (returned only well1); Seismic well loading0.600s; Geo project load including list1.270s; subsequent full list refresh0.985s. Peak process RSS was380,192 KiB. These are one-run diagnostic measurements, not SLAs or an end-user Windows benchmark. No thresholds were encoded to bless all large projects.

The shared map data store and batch Tcl tree insertion avoid the previous per-well object/query/insert cost. Revision domains distinguish DATA, POPULATION and STYLE changes. Those are concrete reasons to leave working architecture alone. Initial full lists and whole-project metadata can still be substantial; do not add redraw/reload optimizations without measuring the actual problematic workflow.

FA-003 is independently confirmed: eight decoded LAS runs account for 512 bytes in a256 MiB cache while retaining3.84 MB of NumPy arrays. An individual current oversized entry is intentionally allowed by BudgetCache; **that is not this defect**. The defect is measuring every LasFile as64 bytes and having no item cap. A long session visiting thousands of runs can grow far beyond the budget.

Other caches have useful limits: curve-array entries are sized as tuples of arrays; Correlation/XSection have curve budgets and capped raster readers; SEG-Y uses memory mapping and bounded section caching; v0.9.69 adds bounded per-map horizon surfaces; disk cache has a byte limit and dependency stamps. Do not report all caches as unbounded because one object type is undercounted. Repeated project/window lifecycle tests provide evidence for specific owners, not proof no allocation can grow in a day-long Windows session.

### Remaining scale/resource gaps

No test here loads38,000 actual LIC files,200 large shapefile layers, multiple full-size SEG-Y volumes, or every LAS run from the client's112K-well project. Large rasters and derived surfaces are separate from well metadata. Native memory-mapped Windows file handles, multi-volume bandwidth, Tk DPI/font behavior, long sessions and simultaneous asset synchronization remain qualification work. No actual orphaned Matplotlib artist accumulation was proven from the idle_draw diagnostic alone; ownership tracing is needed before calling it a leak.

## Import/export and data-integrity review

The checked pathways distinguish durable project data, imported external sources, previews and regenerated display products. Bulk/mapped headers use logical transactions, while LAS parsing/publication is deliberately per-file after successful header import; a bad LAS does not imply good headers should roll back. Raster LIC import reports per-file failures/skips and avoids guessing ambiguous well matches. Production reports duplicates and explicit units; same-source rows are updated according to the selected policy. Multi-source production selection is a documented derivation rule, not a request to merge/delete FM pick sources.

API/UWI text matching, ambiguity checks, filename/destination collision handling, staged digitized output, paired grid/file publication, malformed input tests and cancelled imports all appear in the shipped suite. Workbook export chunks well IDs, splits Excel row limits, uses atomic replacement and forces leading-equals strings to text. This is positive evidence; do not flag its use of openpyxl as inherently unsafe or claim every export format has identical safeguards.

Project Save As uses SQLite backup and path rewriting/checks, including appended shapefile sources fixed in v0.9.69. This is stronger than copying an active main DB. It is not an atomic cloud transfer of every asset. PI-004/005/008 address incomplete targets/snapshots and forensic side effects, while PI-006 and FA-004 identify drafts discarded after failed writes. No client recovery, reimport, migration or conflict resolution was attempted.

## Error handling and UI state

AST inventory found461 broad Exception/BaseException handlers in non-test code and 77 whose AST body is only pass. These are triage counts, not461 defects. Harmless examples include optional cache writes (recompute on miss), callbacks for an already-destroyed widget and diagnostics that must not fail a user operation. Dangerous cases are those that release unique editable state or claim success without durable storage; those were reproduced and have individual findings.

The critical distinction is whether the live state remains retryable after an error. Petro's failed-detach default-No behavior is a good existing model. A console/log/status message that disappears when the window is destroyed is inadequate for unique unsaved interpretation. The fix should preserve state and offer retry/explicit discard without adding approval dialogs to every successful autosave.

Do not treat a status update, a refreshed tree, a DB mtime or a clean shutdown message as proof that every writer saved. Conversely, a hang after polygon Finish can occur after commit. Inspect preserved payloads before concluding either loss or success.

## Tests: strengths, gaps and failures

The full run executed every shipped test module; numerical, database, import/export, selection, cache, renderer, licensing and release checks are represented. Meaningful examples include two independent database sessions with object/payload checksums, foreign-key/integrity checks, failed-commit rollback, staged publication ownership, own-axis curve tests, underlying stored values after reopen and repeated window disposal checks. These are stronger than a startup-only smoke test.

The new independent probes still found defects despite thousands of passing tests. The suite lacks the specific invariants demonstrated by FA-001/002 (inverse round-trip and all-pay N:G on undulating paths), FA-003 (LasFile retained bytes), FA-004 (node-store failure vetoes close), and FA-005 (EUR/ft without months). The recent PI failures likewise show that happy-path persistence and a mocked dirty Cancel test do not cover every real Exit/switch route.

Static/source-inspection tests for launchers/manifests/protected modules are useful distribution guardrails, but cannot establish GUI behavior, numerical correctness or native package completeness. They must supplement, not replace, executable tests. Test-only license trust is isolated; it does not verify the customer EXE's embedded trust.

Three unique full-suite failures were observed: the Drawings manager non-settling at scaling 1.25 (PI-009), Correlation box width6.296937 versus6.300000 (FA-006), and Tk family urw gothic l versus expected avant garde gothic (FA-006). These were also investigated with isolated repeats. The precise Correlation width difference and font alias behavior need platform-aware diagnosis; they are not counted as new geological data corruption. Native Windows/DPAPI, a slow package build, compiled-extension checks, Explorer drops and unavailable full native Kingdom input explain skips, as listed in the evidence document.

The run used four independent processes, not one serial process. This improves isolation/turnaround but may conceal order-dependent or very late interpreter lifecycle failures. A serial Windows customer/source qualification and long-session run remain needed. No application crash was observed in these four processes; that is not a guarantee against the prior late serial Tk abort.

## Security and distribution readiness

This was a source/build-configuration security review plus available tests, **not a re-audit of an actual v0.9.70 Windows customer package**. Source ZIPs intentionally contain reviewable source and owner tooling; their contents are not the allowed customer staging payload.

Inspected protections include restricted expression AST/eval, allow_pickle=False on NumPy workspace/cache reads, parameterized value writes with controlled schema identifiers, explicit allowed customer staging, proprietary-source/bytecode and archive checks, owner-tool exclusion, signature-based licensing, absolute user-data folder selection, and Poppler fallback avoidance of the current directory. The release tooling and installer distinguish installation files from per-user/project writes and include notice/signing checks. No newly confirmed embedded production secret or arbitrary-code-execution path was established by this audit. That statement is bounded to this reviewed baseline and is not a penetration-test certificate.

Unverified distribution risks remain: actual package inventories/hashes, all compiled protected modules, current embedded trust, native DPAPI/locking, code signing/installer permissions, third-party notice completeness in the final bundle and source/runtime dependency compatibility on the packaged interpreter. The historical B56-W05 Windows evidence belongs to its exact earlier artifact; it is not automatically a v0.9.70 packaged test. Do not redesign licensing here or advertise a newly closed packaged finding based only on Linux source tests.

No external account/network scan or user-data inspection was performed. Existing release/security scan records were treated as historical evidence, not rerun current-baseline results. A broad scanner match such as SQL execute, eval or a private-key serialization API is not itself a vulnerability; call context and artifact boundaries matter.

## Suite UI consistency and legacy-code assessment

A total UI overhaul is not justified by the inspected code. The suite already has shared theme, icon, text-style, dropdown/toolbar, scrollframe and project/data services. The later consistency pass should centralize duplicated chrome tokens and reusable treatment while keeping each workbench's layout and renderer. FA-007 is Cleanup, not a release correctness blocker.

| UI concern | Existing authority | Safe later consolidation |
| --- | --- | --- |
| Same function, exact same icon | ogcore.icons.ACTIONS, action_key/action_icon; shared PNG sheet | Use semantic action keys at all static/dynamic wrappers; add registry/snapshot tests.35 statically literal calls had zero canonical mismatches; that is a subset, not universal visual verification. |
| Icon size, padding, active state | icons.SIZE/CUBE_SIZE/PAD/GAP/FONT/on_style/icon_style | Preserve shared icon frames and one-/two-line sizing; add DPI/dropdown alignment checks, not a toolbar redesign. |
| Fonts, tabs, selections, borders, status/header | ogcore.theme/TextStyle shared roles | Replace duplicate chrome literals with semantic tokens; preserve renderer-specific scientific text/color styles. |
| Ribbon/group/dropdown layouts | Correlation and XSection namespaced styles/group helpers | Share metrics/roles incrementally; keep local workflow order and module namespaces. |
| Panels and scrollers | ogcore.scrollframe and common header/side-panel helpers | Resolve PI-009 under real Windows scaling before broad visual work. |

FA-008 identifies the hand-drawn ogmap.icons implementation with no tracked runtime import/reference; archived security reports mention its path but are not callers. This is a bounded dormant-code candidate. External consumers were not supplied, so removal needs an API check. Other compatibility paths are still active and **safe to leave**: bare legacy .ogwdb projects, schema migrations, old LAS storage fallback, BubbleMap migration into unified sets, older templates/project state and source normalization. Do not delete them simply because they refer to old versions.

## Earlier audit corrections: current status

The v0.9.68 report was used as a checklist, not copied as current findings. Source comparison and the v0.9.69 regression modules show substantive corrections to stale-delete identity, atomic horizon/polygon delete, typed rename/Undo, appended shapefile paths, nested transactions, destination collision checks, independent-axis statistics, source Python minimum and bounded Seismic grid cache. Those old defects are not repeated as open current findings merely because they once existed.

| Earlier issue | v0.9.70 review disposition |
| --- | --- |
| AUD-001/009 Seismic stale delete and partial horizon/polygon deletion | Corrections present; current two-session/rollback tests check identities and stored payload. Keep them. |
| AUD-002 rename/Undo | Typed/nested reference handling corrected; current regression module included. |
| AUD-003 appended shapefiles | PATH_COLUMNS/copy validation includes appended sources; current conversion/move tests included. |
| AUD-004/005 destination collisions and nested commits | Checks/outer transaction ownership corrected; current transaction/destination tests included. |
| AUD-006 documented Python minimum | README/launchers/support guard now require3.12 to match SciPy floor; current source setup tests included. Native packaged interpreter remains a separate qualification. |
| AUD-008 unbounded per-map gridded horizons | New bounded Seismic grid-cache implementation/tests present. FA-003 is a different shared LAS-run cache, not a claim this grid-cache fix failed. |
| AUD-010 own-axis statistics | Helper reads own depth/value samples; current numerical-reference test included. |
| AUD-011/012 GUI fixtures/fonts | Improvements present, but residual Correlation width/font-name test failures remain (FA-006). Do not conflate them with the previous distinct Tk crash or call all UI tests fixed. |
| Tk lifecycle v0.9.70 | Deferred tree scroll and binding/trace cleanup present; PI-009 still fails on the audit platform. No newly introduced committed-row deletion was demonstrated. |

## Incident, recovery and supported project sharing

The most plausible working hypothesis for Galveston is an older/different/incomplete laptop project generation, but this is **not proven or probabilistically ranked from client evidence**. The save-loss defects are a real Workbench alternative; a matching WAL may hold newer committed data if that database uses WAL. Broken external SEG-Y/repository or active survey/source/visibility can hide stored objects. A new empty database from a missing manifest target can make an incomplete transfer look like a valid project. No client files were available to discriminate these.

Recovery may be possible from the desktop DB, a matching WAL, cloud versions/conflicts, alternate folders or backups. Memory edits never committed normally have no DB/WAL record after process destruction. Preserve both computers' originals, whole folder trees and matching sidecars before closing/changing a still-running session, copying a winner back, reimporting or “repairing.” Never open forensic originals through normal Workbench or a mode=ro connection that can create SHM. Use an untouched evidence master and separate disposable working copies; recover/inspect/export only those. The full copy-first recovery procedure is included in the bundle unchanged.

Sequential use is not automatically safe because a window closed or the provider says synced. First resolve save failures, then use a verified single-writer snapshot/handoff discipline with resolved paths, completeness/hash/payload checks and required external assets. SQLite backup is stronger than main-file copying but does not make changing external assets atomic. Simultaneous editing of independently synced SQLite replicas is unsafe as a shared transactional project model; advisory markers do not provide distributed serialization. No Dropbox account was accessed and no provider blame was established.

## Top 10 issues to fix before v1.0

1. **PI-001:** Seismic save/close/survey-switch failure veto; retain unique interpretation and honor conflict Cancel.
2. **PI-002:** Geosteering failed autosave cannot authorize discard/close.
3. **FA-004:** Digitizer node-save failure must retain traces and veto close.
4. **FA-001:** Prevent incorrect inverse TVD/TVDSS→MD results on non-monotonic surveys.
5. **FA-002:** Define and guard unsupported TVD pay net/gross behavior; stop silently publishing invalid ratios.
6. **PI-003/006:** Truthful Geo Save/Exit and retained drawing drafts until commit, tested separately.
7. **PI-004:** Open Existing must not create a missing manifest DB.
8. **FA-003:** Make the LAS-run budget count retained arrays and exercise long-session eviction.
9. **PI-005/007/008:** Complete supported snapshot/error/recovery boundaries: visible session failures, no-touch forensics and explicit single-writer handoff. These are separate corrections with separate tests, grouped here as a release gate.
10. **PI-009:** Verify geometry settling and successful Finish on native Windows/DPI; resolve remaining GUI test portability (FA-006) without masking actual UI defects.

FA-005 is a small contained metric fix that can follow these release-critical paths. FA-007/008 are cleanup priorities, not reasons to delay protecting current interpretation data. The grouping above ranks work packages and does not collapse or inflate the17-entry register.

## Safe to leave alone

- Independent Map/Petro/Correlation/Cross Section/Geosteering renderers and current geological workflows.
- Explicit units/percent semantics, NaN-preserving resampling, actual depth-axis compatibility checks and normal monotonic depth calculations.
- Canonical curve/pick services, stable project-local identity, full completion/sidetrack APIs and ambiguity checks.
- Existing atomic helper ownership, baseline conflict checks, selective writes, grid-file staging and backup-based copies; strengthen the caller/handoff contracts around them.
- Compact Map store, incremental revision refresh, batched Geo lists, SEG-Y memory mapping and correctly budgeted caches.
- Petro's retained-state failed-detach behavior and accepted/preview separation.
- Versioned compatibility readers/migrations that still have call paths and tests.
- Working shared theme/icons/namespaced styles; defer cosmetic centralization until after the data-safety work.

## Recommended fix order and regression gates

**First preserve client evidence and unique live drafts.** No automated repair or project change is authorized by this audit.

1. Add failure-injection regressions for every close/switch path before implementation; fix PI-001/002 and FA-004 with narrow outcome propagation. Exercise retry, Cancel and explicit discard from fresh processes.
2. Lock down FA-001/002 with numerical reference/round-trip/support invariants and agree how ambiguous or re-crossed intervals should be handled. Preserve existing supported-well results; do not silently change all formulas.
3. Correct PI-003/006 and PI-007 using the proven retained-state contract. Keep module layouts/workflows intact; test named/Last section transaction failure and raw persisted payloads.
4. Separate open-existing/create, fix cache sizing and make forensic inspection copy-first. Confirm migrations/assets remain intact and normal project creation works.
5. Qualify single-writer snapshot handoff under DELETE and inherited WAL, then native Windows licensing/filesystem/compiled modules and the actual customer EXE. Continue to reject a promise of simultaneous independent-replica editing.
6. Resolve Tk/GUI failures with real DPI/font/event traces; run the serial long-session test that partitioned execution does not replace.
7. Fix the contained production metric, then schedule UI-token/dormant-icon cleanup as separate, low-risk changes only if approved.

The included prior Persistence Test Plan remains applicable; add the FA-001–FA-005 cases and GUI/cache requirements above. A passing suite alone is not release acceptance: required numerical/storage invariants, failure retention, restart behavior, package identity and realistic resource tests must also pass.

## Remaining verification limits

No actual client Galveston project or Dropbox history, v0.9.70 customer Windows archive, signed EXE execution, native DPAPI/locking,100K-well full asset library or external plugin inventory was supplied for this expanded run. No serial full-suite run was performed; all shipped test modules were run in four partitions. No line coverage percentage or whole-code mathematical proof is claimed. Native Kingdom truth files and compiled/package-only conditions skipped exactly as logged. Recommendations are unimplemented; the software and client data remain unchanged.
