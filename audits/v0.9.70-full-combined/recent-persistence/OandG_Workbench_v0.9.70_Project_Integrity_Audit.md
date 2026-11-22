# O&G Workbench v0.9.70 — Project Integrity Audit

**Read-only forensic audit · 22 November 2026 · branch release/1.0**  
**Audited commit:** `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`  
**Comparison:** v0.9.69 `020a48defc83204b8ea28275d44cb7e18fefaa36`

## Executive summary

**Do not treat the current project-close paths or a live Dropbox folder as a reliable cross-computer handoff.** Two reproduced P0 defects discard memory-only work after failed saves: Seismic ignores a failed save before closing/switching; Geosteering treats an existing/project job as safe to discard despite a failed autosave. Geo can report all changes saved while a dirty header remains unsaved, then discard it on window Exit. Opening an existing manifest with a missing database can create an empty replacement. Drawing Finish clears its draft before confirming the write. Other close paths only log failed session saves.

The Galveston Island November 21–22 incident itself is **not diagnosed**: neither computer's actual project, manifest, sidecars, application logs nor Dropbox history was supplied or inspected. The leading working hypothesis is an older/different/incomplete project generation opened on the laptop. That is an investigation priority, not a probability estimate or proof against Workbench/Dropbox. Workbench save failures are a concrete alternative, now independently reproduced. Conditional WAL loss is another possibility only if that particular database actually uses WAL. Missing SEG-Y/repository paths or a different active survey can hide stored interpretation without deleting it.

Normal storage tests also provide positive evidence: fresh-process reads retained representative Geo tops/well data, Petro curves, Seismic horizon/fault, polygon vertices, Correlation layout, Cross Section correlation and Geosteering job in both a local synthetic project and a copied folder. A rollback-journal crash recovered the prior committed 300 rows on a working copy. No committed-data corruption was reproduced in these normal paths.

**Validation:** 235 tests passed, one unique Tk layout test failed, zero skipped, plus 23 passed subtests across two targeted runs. The failed test also failed alone. Six UI scenarios reproduced unchanged on v0.9.69; a seventh polygon-failure scenario reproduced on v0.9.70. These are Linux source tests with isolated synthetic data, not Windows package qualification. No source/test/release edits, user project access, Dropbox access, commits, pushes or release generation were performed.

## Inputs, evidence boundary and method

The supplied ZIP is 11,987,621 bytes, SHA-256 `a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797`. ZIP CRC passed. All 652 Python files matched the verified Git baseline after CRLF normalization. Git checkout contains 961 tracked files. Schema version is 31; the v0.9.70 delta changes ten files, with no database/schema layer change.

Audit combined lifecycle/path tracing, comparison against v0.9.69, targeted existing tests, real Tk UI calls with controlled write failures, process-crash simulations and independent-copy experiments. Failure injection patched only transient objects in disposable test processes; production files/tests were not changed. Synthetic source fixtures and test-only license trust were used, never client data or shipped executable trust. Exact commands, logs, XML, scripts and hashes accompany the evidence bundle.

The persistence paths below were inspected; this is not an exhaustive proof of every broad exception handler or every UI/platform permutation. Complete per-module Windows application restart/termination qualification remains in the test plan. The fresh-interpreter storage checks prove persisted payloads, not full Windows UI reconstruction. No client incident causation can be asserted without preserved originals and separate authorization.

## Ranked findings

| ID | Severity | Finding |
| --- | --- | --- |
| PI-001 | P0 | Seismic discards an unsaved interpretation after a failed save or cancelled conflict |
| PI-002 | P0 | Geosteering treats a failed autosave as permission to discard a saved/project job |
| PI-003 | P1 | Geo Save Project reports all changes saved while dirty header edits remain; window Exit drops them |
| PI-004 | P1 | Opening an existing manifest with a missing database silently creates an empty project |
| PI-005 | P1 | Synced replicas lack a consistent snapshot handoff or stale-generation acceptance check |
| PI-006 | P1 | Drawing Finish clears editable vertices before the database write succeeds |
| PI-007 | P2 | Correlation and Cross Section close after logging failed session/section persistence |
| PI-008 | P2 | Recovery read-only open may create a shared-memory sidecar on the original |
| PI-009 | P2 | The v0.9.70 Drawings layout regression still fails at scaling 1.25 on the audit platform |

### PI-001 — Seismic discards an unsaved interpretation after a failed save or cancelled conflict

**Severity:** P0  
**Classification:** Confirmed defect; real UI failure injection  
**Confidence:** High  
**Files/lines:** `seismicworkbench/app.py:500–532,674–679,1696–1721,3031–3036`  
**Functions:** `SeismicWorkbench.close_project, select_survey, save_now, on_close`

**Current behavior and problem.** save_now returns False on SQLite/OSError and on conflict Cancel. close_project ignores it, calls close_survey (which clears interp), destroys windows and closes the database. select_survey likewise ignores False. on_close destroys the application in finally even if closing raises. Layout is saved before the interpretation, so a fresh database modification time need not mean picks were saved.

**Reproduction.** Run probes/ui_cases.py. Open the synthetic SEG-Y project, set Horizon 1[6,8]=1000 and save. Change it to 1200; inject sqlite3.OperationalError from store.save_interpretation; close and reopen.

**Expected.** Abort close/survey switch and retain the live interpretation until a successful save or explicit discard.

**Observed.** Project closes despite the save error; reopened pick is 1000, not 1200. Separate status text says work stays in the window, but close removes that window.

**v0.9.69 comparison.** Reproduced identically on 020a48d; the v0.9.70 cleanup is after the same unchecked save.

**Correction concept (not implemented).** Honor a single save outcome before any close, switch, callback cancellation or destruction; preserve state on failure/Cancel. Remove unconditional destroy on failed close. Show an actionable persistent failure.

**Automated regression.** Automate disk-full/I/O/locked-commit failure and conflict Cancel through Close Project, WM close and survey/project switch. Assert dirty objects/window/database remain, then retry and verify fresh-process stored values.

**Recovery implication.** Previously committed picks remain. Never-committed edits are normally recoverable only while the process still holds them; a WAL cannot recover edits never written to SQLite.

### PI-002 — Geosteering treats a failed autosave as permission to discard a saved/project job

**Severity:** P0  
**Classification:** Confirmed defect; real UI failure injection  
**Confidence:** High  
**Files/lines:** `geosteering/app.py:2262–2301,2376–2397,2779–2793`  
**Functions:** `GeosteeringWorkbench._autosave, _confirm_discard, on_close`

**Current behavior and problem.** _confirm_discard flushes a pending autosave, but then returns True whenever job.path is set or in_project is True even if dirty remains True after that save failed. If an earlier autosave has already failed and cleared its timer, the same condition skips a retry. on_close releases resources and destroys the window.

**Reproduction.** Run probes/close_errors.py. Save a synthetic project job named Saved, change its name to Unsaved, mark_dirty, inject SQLite write failure in geosteering.project.save_job, then on_close and reload the job.

**Expected.** Keep the dirty job open after failure or require explicit informed discard.

**Observed.** The project closes and stored job name remains Saved; Unsaved is lost. _autosave only sets a status message before closing.

**v0.9.69 comparison.** Reproduced identically on 020a48d; file unchanged in v0.9.70.

**Correction concept (not implemented).** Make autosave report success and require dirty=False or explicit discard before releasing a job. Saved-path/project membership must not imply dirty work is durable.

**Automated regression.** Test pending autosave failure and already-failed autosave with no pending timer; test standalone .ogsteer and project jobs, lateral/job switch and close; verify segments/faults/targets as well as name.

**Recovery implication.** Older saved job/track survives; the failed newer interpretation may exist only in process memory. Preserve any still-running session before further actions.

### PI-003 — Geo Save Project reports all changes saved while dirty header edits remain; window Exit drops them

**Severity:** P1  
**Classification:** Confirmed defect; real UI reproduction  
**Confidence:** High  
**Files/lines:** `geoworkbench/main_window.py:868–875,2519–2577,2579–2587,2625–2635; geoworkbench/well_tab.py:194–203`  
**Functions:** `WellDataManagerApp.save_project, on_close, close_project, _resolve_unsaved_edits; WellTab.dirty`

**Current behavior and problem.** Save Project commits the connection but does not save dirty tabs, then reports All changes are saved as you work. Close Project invokes the dirty resolver, but window Exit/on_close bypasses it and closes the database.

**Reproduction.** Run probes/ui_cases.py. Load Tab Well, change the header well_name StringVar to Edited Draft, verify dirty(), invoke save_project and then on_close. Query wells from a new connection.

**Expected.** Save Project writes pending edits or states what remains unsaved; Exit invokes the same dirty resolver as Close Project.

**Observed.** Stored name is Tab Well after Save Project and after Exit; dirty-dialog call count is zero. Source emits the all-saved message.

**v0.9.69 comparison.** Reproduced identically on 020a48d; relevant files unchanged.

**Correction concept (not implemented).** Use one dirty-save/close coordinator for the main tabs and owned windows; only report all-saved when all relevant writers succeeded.

**Automated regression.** Exercise header/location/manual-data tabs through Save Project, menu Exit, WM close, Close Project and project switch. Test Save/Discard/Cancel and invalid fields; read database after process restart.

**Recovery implication.** The old well row is preserved. Unsaved form contents generally have no database/WAL copy after destruction.

### PI-004 — Opening an existing manifest with a missing database silently creates an empty project

**Severity:** P1  
**Classification:** Confirmed defect; real UI reproduction  
**Confidence:** High  
**Files/lines:** `ogcore/project.py:180–203,307–319; database.py:1184–1203; seismicworkbench/app.py:454–500`  
**Functions:** `Project.load, open_target, database_for; ProjectDatabase.__init__; SeismicWorkbench.open_project`

**Current behavior and problem.** Manifest resolution supplies its database path without checking that the existing project target exists. sqlite3.connect uses create-if-missing behavior. When DB/ exists but its database has not synced, opening the manifest creates a new valid empty schema instead of reporting an incomplete project.

**Reproduction.** Run probes/ui_cases.py. Create only the normal manifest/folders in a disposable location (never remove an existing database), then open that manifest through SeismicWorkbench.

**Expected.** Open Existing refuses a missing manifest target and leaves the directory unchanged; explicit New Project can create it.

**Observed.** A new database is created and opened with zero wells. This is not overwrite of an existing database, but creates a competing empty artifact in a sync directory.

**v0.9.69 comparison.** Reproduced identically on 020a48d; path/database layer unchanged.

**Correction concept (not implemented).** Separate explicit create from open-existing, validate resolved manifest target, and open-existing with no-create SQLite semantics. Show the exact manifest and resolved database path.

**Automated regression.** Open a manifest with absent DB file, unavailable repository/drive, partial folder transfer and database path outside root. Assert no new DB/sidecars and a clear missing-target error; retain New Project creation tests.

**Recovery implication.** An empty replacement does not prove original data was deleted. Preserve it separately; locate the desktop DB, older versions, conflicted/alternate paths and matching sidecars without overwriting anything.

### PI-005 — Synced replicas lack a consistent snapshot handoff or stale-generation acceptance check

**Severity:** P1  
**Classification:** Confirmed architectural safeguard gap; conditional WAL and independent-replica risks reproduced; Dropbox incident unproven  
**Confidence:** High  
**Files/lines:** `ogcore/safeio.py:201–270; seismicworkbench/app.py:454–500; ogcore/project.py:307–319,365–476; database.py:1184–1245,1796–1810; ogcore/handoff.py:278–312`  
**Functions:** `SessionLock.holder/acquire; open_project; write_project_copy; ProjectDatabase connection/change_stamps; watch_close`

**Current behavior and problem.** SQLite protects connections to one local database, not independent replicated files. Advisory per-module lock markers can lag synchronization and can be overridden; acquire itself overwrites the marker. No sync-complete/snapshot manifest, conflicted-copy reconciliation or last-accepted remote generation check was found in these project-open/save paths. change_stamps protects derived caches, not cross-computer handoff. App does not explicitly enable WAL; an inherited WAL remains possible.

**Reproduction.** Run probes/sqlite_scenarios.py: independent copies retain values 30 and 40; selecting a preserved older generation opens value 2 without warning. In explicit WAL mode, committed 99 is missing from a main-only copy (30); abrupt exit with committed 123 leaves main-only at 99; a disposable main+WAL pair recovers 123. Foreign marker is detected but acquire overwrites it.

**Expected.** A supported handoff delivers a verified consistent committed snapshot and rejects incomplete/missing targets; simultaneous editing is explicitly unsupported or coordinated independently of file sync.

**Observed.** Stale/incomplete copies can be accepted. Default DELETE committed-idle main-only copy retained value 2; do not generalize the conditional WAL failure to the default mode or claim Dropbox actually chose a stale file.

**v0.9.69 comparison.** Same storage/project/lock paths in 020a48d. v0.9.70 only cancels the handoff polling callback when a window is destroyed.

**Correction concept (not implemented).** Define single-writer snapshot handoff using SQLite backup plus a versioned manifest/checksums and explicit success acknowledgement. Validate completeness/identity at destination, make concurrent-use policy explicit, and never auto-merge SQLite replicas or checkpoint a live synced original.

**Automated regression.** Automate A–E in both DELETE/WAL, WAL without SHM, delayed sidecars/manifest/assets, independent replicas, split generation, stale/conflicted names and concurrent marker acquisition. Validate target hash/interpretation payload, not mtime alone.

**Recovery implication.** Newest committed data may remain on desktop, in matching WAL, versions or conflicted copies. Preserve each generation intact; do not copy arbitrary sidecars from another generation or choose winners by timestamps.

### PI-006 — Drawing Finish clears editable vertices before the database write succeeds

**Severity:** P1  
**Classification:** Confirmed defect; real UI failure injection for new polygon; same ordering in edited shape  
**Confidence:** High  
**Files/lines:** `ogmap/drawing_tab.py:411–462,577–594; ogmap/drawings.py:156–178`  
**Functions:** `DrawingsTab.finish, finish_edit; drawings.save`

**Current behavior and problem.** finish captures nodes and calls cancel before validation/dialog/write. finish_edit similarly cancels before drawings.save. A database error propagates after the editor has already discarded its draft. Normal successful Finish commits through db.execute before tree/grid refresh.

**Reproduction.** Run probes/drawing_failure.py. Digitize three polygon vertices in a disposable regular Map, inject OperationalError in drawings.save, invoke Finish.

**Expected.** Keep the draft and editing mode on write failure, allowing retry or explicit discard.

**Observed.** Write error propagates, persisted row count is zero, nodes becomes [] and state becomes None. Test did not simulate a user Cancel or unfinished draft close.

**v0.9.69 comparison.** finish/finish_edit bodies unchanged from 020a48d; the new disposal logic is not the source of this ordering.

**Correction concept (not implemented).** Validate and persist first; only clear the active editing state after confirmed success. Restore or retain draft on all save errors and Cancel from subsidiary destination dialogs.

**Automated regression.** New/edit polygon, fault polygon, contour and external shape destination: inject validation/write/publication failure; assert original and draft vertices survive and retry writes once.

**Recovery implication.** Original persisted geometry survives a failed edit; a never-written new polygon normally has no recoverable DB record. Do not confuse post-commit UI hangs with this pre-commit failure.

### PI-007 — Correlation and Cross Section close after logging failed session/section persistence

**Severity:** P2  
**Classification:** Confirmed Correlation/Cross Section UI failures; additional Map line error-reporting path static  
**Confidence:** High  
**Files/lines:** `correlationworkbench/app.py:522–546; correlationworkbench/store.py:403–407; xsection/window.py:2636–2649,2708–2720; ogmap/window.py:2569–2576`  
**Functions:** `CorrelationWorkbench.close_project/quit_app; CrossSectionWindow._autosave/close; MapWindow._save_section_lines`

**Current behavior and problem.** Correlation catches session-save exceptions and logs, then closes. Cross Section autosave catches all exceptions and close destroys regardless. Named and Last section saves are separate transactions. Map section-line save similarly logs a failure while keeping the in-memory visual change. No user retry/discard decision is required.

**Reproduction.** Run probes/close_errors.py. Save Correlation spacing 1.25, change to 7.25 and fail save_session during close: stored 1.25. Save named section view.top=111, change to 222 and fail save_section during close: stored 111, window destroyed.

**Expected.** Keep the unsaved session/section open or clearly offer retry/discard; save coupled named/Last state consistently.

**Observed.** Older session/section reappears after reopen with warning only in logs. Cross Section section-local correlations/faults/fills can also be inside this JSON; project top/fault picks already committed through shared APIs are a separate store.

**v0.9.69 comparison.** Both UI failures reproduced identically on 020a48d; cited files/functions unchanged.

**Correction concept (not implemented).** Return and honor save outcomes; preserve state and notify users. Wrap coupled section saves in one transaction. Apply the same outcome contract to Map line/settings saves.

**Automated regression.** Test close, new/open section, named/Last second-write failure, and Map line-save failure. Verify JSON payloads on fresh reopen plus visible error and retained dirty state.

**Recovery implication.** Old committed layouts remain; never-saved section-local annotations may be memory-only. A logged error is useful evidence but does not restore the discarded data.

### PI-008 — Recovery read-only open may create a shared-memory sidecar on the original

**Severity:** P2  
**Classification:** Confirmed synthetic filesystem side effect; no user file opened  
**Confidence:** High  
**Files/lines:** `ogcore/recovery.py:139–181,183–213; database.py:1217–1245`  
**Functions:** `ReadOnlyProject._open/_recovered_copy; ProjectDatabase.reader`

**Current behavior and problem.** mode=ro prevents SQL updates to the main DB, but SQLite can create/write WAL shared memory when the directory is writable. Recovery first tries that connection on the supplied path; its private-copy recovery fallback is reached only after an error. Therefore read-only is not a guarantee of zero filesystem side effects.

**Reproduction.** Run probes/sqlite_scenarios.py. On a disposable committed WAL pair with no SHM, instantiate ReadOnlyProject and inspect directory entries before/while open.

**Expected.** A forensic zero-touch mode performs all SQLite work on a working copy and preserves original files byte-for-byte.

**Observed.** probe.ogwdb-shm is created on the supplied synthetic path; the WAL value 123 is readable. No main-file SQL write was alleged. Existing recovery tests do not cover this absent-SHM/writable-directory combination.

**v0.9.69 comparison.** Identical recovery/reader code in 020a48d.

**Correction concept (not implemented).** Offer explicit copy-first forensic inspection and document normal read-only reader side effects. Do not use immutable=1 as a blanket solution: ignoring WAL can omit committed data.

**Automated regression.** Hash/list main, WAL, SHM and journal before/after on writable/read-only directories, missing SHM and hot journal, with a writer present. Assert the original is never opened by SQLite for forensic inspection.

**Recovery implication.** Use preserved raw evidence plus a separate disposable working copy. Existing private-copy recovery/backup can be useful there; never checkpoint, repair or open the live original merely to inspect it.

### PI-009 — The v0.9.70 Drawings layout regression still fails at scaling 1.25 on the audit platform

**Severity:** P2  
**Classification:** Confirmed Linux/Tk test failure; Windows impact and exact remaining geometry cause unverified  
**Confidence:** High for test failure; Medium for operational exposure  
**Files/lines:** `tests/test_v0970_tk_lifecycle.py:100–131; ogcore/scrollframe.py:85–109,117–172; ogmap/drawing_tab.py:151–165`  
**Functions:** `LayoutSettles.test_natural_and_resized_manager_settles; ScrollFrame.update_layout/_schedule; DrawingsTab._wrap_hints`

**Current behavior and problem.** The shipped bounded event-drain test reaches 20,000 events instead of settling at scaling 1.25. It fails in the combined run and alone. This prevents accepting the Tk fix as fully verified on this platform; it is not evidence that persisted interpretation rows disappeared.

**Reproduction.** Run the exact isolated Tk recheck in Audit_Evidence.md using Xvfb, Tcl/Tk 9.0.4 and the recorded dependencies.

**Expected.** The manager settles within the bounded drain at all tested scalings, without geometry feedback starving useful UI work.

**Observed.** Assertion 20000 not less than 20000 at scaling 1.25; 1 failed in 3.06s. Fontconfig cache warning also present. No Windows/customer-EXE reproduction was performed.

**v0.9.69 comparison.** Related geometry-loop exposure existed in v0.9.69; this new test is absent there. Do not call the exact failure a proven new v0.9.70 regression.

**Correction concept (not implemented).** Investigate the remaining geometry feedback under the recorded environment; fix only after tracing it. Keep bounded tests; do not infer a persistence fix from UI responsiveness alone.

**Automated regression.** Repeat on packaged Windows/Tk and Linux at 100–200% scaling, with actual event/geometry traces; verify Finish commits before refresh and remains responsive.

**Recovery implication.** A UI stall after Finish can occur after commit. Inspect preserved copies for the polygon record before assuming loss or re-digitizing; force-killing can discard other pending memory edits.

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

## Galveston Island incident: hypotheses and discriminating evidence

| Hypothesis | Why plausible / what would distinguish it |
| --- | --- |
| Older/different project generation on laptop (first investigation priority) | D/E show valid stale copies open normally; absolute manifest targets/recent paths can differ. Compare exact resolved paths, DB hashes, project/well/survey IDs, object counts and pick payloads between preserved desktop/laptop copies. Newer DB mtime alone is insufficient. |
| Failed or never-triggered save on desktop | PI-001/002 show close can lose edits following write failures. Preserve running memory if present; inspect error logs for NOT saved/disk/locking failures and determine whether Finish/Save was completed. No client log was provided. |
| Incomplete WAL/sidecar transfer | A/C reproduce it only in WAL. Determine mode and coherent sidecar content on working copies. Actual user's journal mode and transfer history are unknown. |
| Missing/different external SEG-Y/repository root or active survey | Stored seismic picks are keyed by survey/line/interpretation identity. Inspect all stored objects on copies, resolve asset paths/geometry/fingerprints before inferring deletion. SEG-Y fingerprint mismatch checks exist (`seismicworkbench/project.py:124–165`), so do not assume arbitrary geometry silently remaps. |
| Conflicted copy/older cloud revision selected | Inspect provider versions/conflicts only with separate authorization. Preserve them as independent candidates, never overwrite current copies. No provider account was inspected. |
| Migration, schema loss or cache issue | v0.9.70 schema unchanged; normal reopen/fresh-process tests retained payloads. This lowers support for a blanket new-schema explanation, but cannot rule out client-specific older schema, filters or cached state. Compare raw stored rows before changing display settings. |

**Recovery may be possible**, especially if committed edits exist on desktop, in a matching WAL, a conflicted/versioned DB or alternate folder. Never-written memory edits usually do not exist in SQLite. Recoverability cannot be promised without preserved evidence. Use the separate recovery procedure; no recovery was attempted on user files.

## Operational disposition and immediate safeguards

**Sequential desktop/laptop use:** not currently qualified as safe merely because Dropbox says synced or the first window closed. Failed-save close and partial/stale copy acceptance remain. A controlled single-writer handoff can reduce exposure: verify save success, independently confirm persisted objects, close all suite processes/connections, preserve a consistent snapshot and required assets, allow a complete transfer, then verify manifest/path/hash/content at the destination before further editing. This is a proposed operating discipline, not a validated Dropbox integration guarantee. Do not perform these steps on potential incident evidence until preservation is complete.

**Simultaneous multi-computer use:** unsafe as a shared transactional project model. Advisory synced lock files and local SQLite locks do not provide a distributed lock, generation ordering or merge of separate SQLite histories. Concurrent same-machine access to one local database has meaningful transaction/conflict safeguards; that is a different deployment.

**Immediate actions:** preserve both computers' evidence first; do not keep writing through a suspicious replica; do not delete sidecars or resolve conflicts; avoid alternating/simultaneous editing of the live sync directory. After evidence preservation, prefer a verified local working copy with deliberate versioned snapshots/handoffs. Do not interpret the presence of a Backup directory or a recent timestamp as proof of backup/save completeness.

## Recommended correction order and release gates

1. PI-001/002: veto every destructive close/switch after failed save or conflict Cancel; retain memory and retry. Test all entry points before further UI cleanup.
2. PI-003/006: make Save/Exit behavior truthful and retain drawing drafts until commit; verify normal behavior stays unchanged.
3. PI-004: separate create vs open-existing; never generate an empty DB during incomplete transfer.
4. PI-007: apply the shared success/failure/discard outcome contract to sessions, sections and settings; make named/Last saves atomic.
5. PI-008: provide a copy-first forensic route before instructing users to inspect originals.
6. PI-005: define and validate supported single-writer snapshot/handoff behavior and incomplete/stale-generation warnings. Do not bolt a pretend distributed lock onto Dropbox or auto-merge replicas.
7. PI-009: finish platform-specific geometry verification without changing geological workflows or storage algorithms.

Before v1.0, require the automated tests in Persistence_Test_Plan.md, native Windows source/package runs, and controlled failure/restart/handoff exercises. This audit does not qualify the release as safe against all data-loss scenarios.

## Safe to leave alone / strengths to preserve

- Keep independent renderers and geological calculations; no evidence here justifies a UI rewrite or renderer merger.
- Preserve existing atomic helper ownership, rollback on failed commit and nested transaction protections; they passed targeted tests.
- Preserve Seismic object-baseline conflict checks under the write transaction, selective updates and the rule that absence from a partial load is not deletion.
- Preserve Petro's default-No failed-save detach decision and canonical accepted-curve/preview separation.
- Preserve staged grid/file publication and explicit SQLite backup-based project copies; strengthen handoff boundaries around them rather than raw-copying active databases.
- Keep repository tokens, relative project paths and survey fingerprint checks; expose resolved identity and completeness rather than replacing the entire project model.
- Keep recovery fallback working on private copies. The initial read-only open's side effects need a narrow forensic correction, not removal of journal-aware recovery.

## Remaining verification gaps

No actual Galveston desktop/laptop files, cloud versions/conflicts, Windows executable, network sync process, Windows filesystem/locking behavior, failing physical disk or 100,000-well project was examined in this audit. No whole-suite serial test run was claimed. The selected suites and storage restart probes do not cover every application's full independent OS-process UI restart/error sequence. Large asset synchronization, live sync during writes, all legacy migrations, every logging-only error path and hard power loss remain unqualified. Recommended fixes are concepts only; no implementation or release was produced.
