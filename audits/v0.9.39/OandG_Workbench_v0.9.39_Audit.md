# O&G Workbench v0.9.39 — Fresh Whole-Code Audit

12 November 2026. Read-only review for private/internal v1.0 field testing.

## 1. Executive summary

**Recommendation: BLOCK v1.0.** Six new confirmed defects were reproduced: **5 HIGH, 1 MEDIUM, 0 CRITICAL, 0 LOW**. The blockers concern unaccepted scientific results becoming public to other modules, incompatible units being mixed, and valid grid/registration work being overwritten. These are concrete preservation/correctness failures, not requests for architectural elegance or public-release polish.

The previously known **A38-P01 dense-label rendering limitation remains MEDIUM** and is reported separately from the six new defects. Counting that existing limitation gives 7 listed items: 5 HIGH and 2 MEDIUM. It is not promoted to HIGH. No broad renderer merger, UI overhaul, scientific-formula rewrite, dependency update or speculative optimization is recommended.

The authoritative input is the supplied **OandG_Workbench_v0.9.39.zip**, internally version 0.9.39, SHA-256 `b237c93bfe5ba908256789f38fff5090e475ebad365fcc7a1e82c808265dfcb2`. The earlier v0.9.38 upload was not used as the audit baseline. The brief identifies `release/1.0`, commit `030800e`; this ZIP contains no Git metadata, so equivalence to that commit cannot independently be established. The archive hash pins the exact reviewed source.

The entire tree was inventoried: **887 files, 592 Python files, 247,998 Python lines**. Review depth varied: broad static/source and test inspection across the suite, with concentrated call tracing and temporary-project probes at data, scientific-unit, concurrency and publication boundaries. This is a whole-package scope review, not a claim that every possible UI state, input or numerical case has been proven correct.

**Testing:** collection found 2,615 test cases. The ordinary single-process full run crashed in Linux/Tk during automatic raster registration. The serial, fresh-process-per-file rerun completed **243/243 test files**, aggregating **2,596 passed, 4 failed, 15 skipped, 0 errors**, plus **605 passing subtests**. These are isolated-run aggregate results, not a claim that the original full command passed. Details and failure classifications appear below. The brief's 2,611 passed / 4 skipped / 0 failed result was not independently reproduced as one clean run in this environment.

**Source integrity:** all 887 supplied files remain byte-for-byte unchanged; missing=0, added=0, changed=0. No application code, tests, settings files in the supplied tree, dependencies or application documentation were changed. Audit probes and disposable data were created outside it. Publication of report/evidence commits to the separate Software-reviews repository follows the user's later explicit authorization to save to GitHub; it is not an application-source commit.

## 2. Finding table

| ID | Severity | Confirmed finding |
| --- | --- | --- |
| A39-01 | HIGH | Saving an unaccepted Petro preview publishes its zone/pay results |
| A39-02 | HIGH | Mixed-unit zone publication relabels earlier values without converting them |
| A39-03 | HIGH | Seismic Rename still writes an obsolete grid snapshot |
| A39-04 | HIGH | Image opacity and visibility saves can erase a newer registration |
| A39-05 | HIGH | Grid path allocation can overwrite a valid unregistered grid file |
| A39-06 | MEDIUM | Remaining CSV exporters truncate earlier completed outputs before success |
| A38-P01 | MEDIUM | Previously known dense-label rendering limitation; retained, not a new defect |

## 3. Detailed findings

All six new findings below have High confidence. Reproductions use disposable synthetic projects and controlled failures, not client data or evidence of client incident frequency.

### A39-01 — Saving an unaccepted Petro preview publishes its zone/pay results

**Severity:** HIGH. **Confidence:** High.

**File/function:** petroworkbench/geo_link.py:421–523, 993–1034 (GeoLinkMixin._save_geo_workspace, _zone_results)

**Exact failure:** The curve-save branch correctly substitutes accepted values under previews, but then calls _zone_results with the live working well. That function evaluates cutoffs and summaries from well.curves and well.units, including preview values, and publish_zone_values durably writes the result.

**Realistic trigger:** A pay definition uses a curve that is temporarily replaced by a formula preview; save the workspace/project without accepting that preview.

**Consequence:** Map, Bubble Map and other readers can consume technical results that contradict the accepted stored curve. The result remains published until a later operation recomputes it.

**Reproduction/evidence:** The real Petro application and formula path were exercised on a temporary project. Accepted X=1 and X>0.5 gave net=5 ft. Preview X=X*0, then Save, kept canonical X=1 but changed persisted net to 0 ft and N:G to 0. Discard plus another Save restored 5 ft. See preview-zone-evidence.json.

**Existing coverage and gap:** test_v0939_fixes.py verifies accepted curve values/metadata and discard, not the separately published zone_values. Existing pay and zone-publication tests do not combine this preview/save boundary.

**Recommended fix:** Compute published summaries from a complete accepted-state snapshot on canonical axes, including accepted units/metadata; never pass the live preview well into durable publication. Keep preview rendering separate.

**Regression tests:** Preview replacing an accepted cutoff input: save, read zone results through a second connection, discard, save/reopen. Repeat with an externally edited/deleted accepted input and a preview of the manual flag itself.

**Change risk:** Moderate: publication must share the accepted-state rule while preserving existing pay equations.

**Probe:** `evidence/probes/preview_zone.py`.

### A39-02 — Mixed-unit zone publication relabels earlier values without converting them

**Severity:** HIGH. **Confidence:** High.

**File/function:** database.py:2718–2751 (ProjectDatabase.publish_zone_values); petroworkbench/geo_link.py:993–1034 (_zone_results); ogmap/sources.py:193–207 and zone_attribute collection

**Exact failure:** Zone attributes have one shared units field. Each publication updates that field to the incoming unit while keeping other wells' numeric values untouched. Petro produces length-valued pay summaries in each well's own depth unit; Map reads all rows using the single shared attribute unit.

**Realistic trigger:** Equivalent pay definitions in feet and metre wells publish into the same zone and attribute names. Both well-depth units are supported elsewhere in the suite.

**Consequence:** Previously correct technical values acquire the wrong physical meaning. Grids, bubbles, posting and exports can mix unlike lengths while labeling them uniformly.

**Reproduction/evidence:** Actual _zone_results and publish_zone_values produced 100 ft and 30.48 m for physically equivalent all-pay zones. After the metric publication, both rows were labeled m, but their values remained 100 and 30.48. sources.collect returned those same unequal values with unit m. See zone-units-evidence.json.

**Existing coverage and gap:** test_regional_depth_units.py covers mixed-unit top/isopach geometry and stable grid units; test_bubbles.py covers publication on a common unit. Neither exercises per-well mixed-unit publication into one attribute.

**Recommended fix:** Establish and retain an attribute's canonical unit and convert compatible incoming values before writing, or retain per-value units and normalize at consumption. Refuse incompatible units explicitly. Do not silently relabel old numbers.

**Regression tests:** Publish equivalent feet/metre results in both orders, read through Map/Bubbles and reopen, and assert equal physical values with a stable unit. Include blank and incompatible units plus phi-h/HCPT and producer ownership.

**Change risk:** Moderate: existing inconsistent attributes require explicit diagnosis/recovery; do not guess how old values were authored.

**Probe:** `evidence/probes/zone_units.py`.

### A39-03 — Seismic Rename still writes an obsolete grid snapshot

**Severity:** HIGH. **Confidence:** High.

**File/function:** seismicworkbench/grids_ui.py:176–190 (GridsMixin.rename_project_grid); ogmap/grids.py:293–381 (save versus rename)

**Exact failure:** Seismic loads a complete grid before displaying the rename dialog, changes its name after the dialog returns, and calls grids.save on that old object. It bypasses grids.rename, the new name-only operation that reloads under the write lock.

**Realistic trigger:** Another window/module regrids or changes scientific grid metadata while Seismic's Rename dialog is open; complete Rename afterward.

**Consequence:** A presentation-only name edit can overwrite newer values, unit, notes and control/settings state with the older snapshot.

**Reproduction/evidence:** While the real rename method's dialog callback was active, a second connection changed the first grid value from 7000 to 7500, unit ft to m and notes to a new interpretation. Completing Rename retained the new name but stored 7000, ft and empty notes. The probe mocks only the dialog/render notifications; actual storage and grid files are used. See seismic-rename-evidence.json.

**Existing coverage and gap:** The v0.9.39 name-only tests cover the grids service and Geo MapWindow, not GridsMixin.rename_project_grid in Seismic.

**Recommended fix:** Route Seismic Rename through grids.rename and use its returned current object; handle a deleted grid without recreating it. No storage rewrite is necessary.

**Regression tests:** Exercise the Seismic entry point with an intervening save and deletion while the dialog is open; reopen and compare all scientific content. Keep the existing Geo Map rename regressions.

**Change risk:** Low: use the existing tested name-only service at the remaining caller.

**Probe:** `evidence/probes/seismic_rename.py`.

### A39-04 — Image opacity and visibility saves can erase a newer registration

**Severity:** HIGH. **Confidence:** High.

**File/function:** ogmap/window.py:2931–2963 and 3358–3365 (save_image_layer, set_image_opacity, ask_image_opacity, image visibility); ogmap/georef.py:331–344 (save)

**Exact failure:** Image display commands mutate the cached ImageLayer and save the whole object, including georef. The name-only rename fix does not protect these display-only writes.

**Realistic trigger:** Keep the Opacity dialog open while another connection saves an image registration; then accept the opacity value. A stale cached layer can likewise be used by the visibility path.

**Consequence:** A style edit can replace valid control points/transform/lock state with an older registration, moving the image or making it unregistered.

**Reproduction/evidence:** The actual MapWindow opacity-to-save methods were bound with rendering callbacks omitted. During the opacity dialog callback, another SQLite connection saved a valid three-point affine registration. Accepting 50% opacity wrote opacity=0.5 but removed all three points and stored an unregistered image. See image-opacity-evidence.json. The opacity failure is reproduced; the visibility path shares the same whole-object save.

**Existing coverage and gap:** test_map_images.py covers registration/display behavior, and test_v0939_fixes.py covers image rename preservation. No concurrent registration-plus-opacity/visibility preservation test was found.

**Recommended fix:** Add field-only persistence for opacity/visibility and call it from display commands; reserve georef.save for explicit registration edits with appropriate stale-edit checks.

**Regression tests:** Opacity and visibility changes after a concurrent registration/rename must preserve all current registration data. Include deletion while a display dialog is open and reopen-based assertions.

**Change risk:** Low to Moderate: separate a few display-field updates from registration persistence without altering transforms.

**Probe:** `evidence/probes/image_opacity.py`.

### A39-05 — Grid path allocation can overwrite a valid unregistered grid file

**Severity:** HIGH. **Confidence:** High.

**File/function:** ogmap/grids.py:276–324 (_grid_path, save), 451–480 (register_folder); ogmap/window.py:1552–1575 (new_grid)

**Exact failure:** _grid_path reserves paths listed in map_grids but does not reserve existing filesystem entries absent from that table. A new grid can therefore be published over a valid file already in the Grids folder.

**Realistic trigger:** Copy a grid into an already-open project's Grids folder, a supported register_folder workflow, then create/rename a grid to that filename before the copied grid has been registered/refreshed. Sanitized-name collisions also need preservation.

**Consequence:** The copied grid's scientific content is replaced with no conflict prompt; a later folder scan cannot recover its original bytes.

**Reproduction/evidence:** A valid unlisted Imported.ogwgrid with first value 9000 was created in a temporary project's Grids folder. Saving a new Imported grid with first value 1000 reused that exact filename and destroyed the earlier bytes. See grid-unlisted-evidence.json. This is a file collision, not a database-corruption claim.

**Existing coverage and gap:** test_project_assets.py and test_audit_assets.py cover managed files, registered-grid collisions and failed-save rollback, not an existing unlisted destination.

**Recommended fix:** Reserve all existing entries except the exact current grid's verified owned path; allocate a fresh collision-safe name under the save's lock/publication boundary. Keep current legitimate same-object replacement and rename behavior.

**Regression tests:** Preserve valid unlisted grids and unrelated files across create/rename, including case/sanitized collisions; confirm an existing grid can still update itself and failed publication preserves both files and rows.

**Change risk:** Moderate: path allocation must distinguish ownership from name coincidence and remain compatible with managed-file renaming.

**Probe:** `evidence/probes/grid_unlisted.py`.

### A39-06 — Remaining CSV exporters truncate earlier completed outputs before success

**Severity:** MEDIUM. **Confidence:** High.

**File/function:** geoworkbench/spreadsheet.py:524–531 (export_csv); ogvol/report.py:228 onward (write_csv); ogvol/app.py:660–682 (export_report)

**Exact failure:** Both CSV writers open the chosen destination directly in write mode, then stream rows. The old file is gone if a subsequent write fails.

**Realistic trigger:** Overwrite a previously reviewed spreadsheet/volumetrics CSV and encounter an output error or interruption after opening it.

**Consequence:** A useful prior export is replaced by an incomplete report despite the operation failing. Project data remains intact and the export can generally be regenerated.

**Reproduction/evidence:** With existing reviewed files, an injected OSError on the second writerow propagated but left only 8 bytes for the spreadsheet CSV and 19 bytes for volumetrics. Old bytes were not preserved. See output-failure-evidence.json.

**Existing coverage and gap:** Existing atomic grid, seismic, shapefile and workbook export tests show the right pattern elsewhere; the two reproduced CSV paths lack equivalent failed-overwrite preservation coverage.

**Recommended fix:** Use the existing safeio.atomic_write helper and publish the completed file only. Keep current formatting and scientific values unchanged.

**Regression tests:** Fail after the header and during data rows, assert original destination bytes survive and temporary files are removed; also test successful replacement.

**Change risk:** Low: localized file-publication changes.

**Probe:** `evidence/probes/output_failures.py`.

## 4. Performance findings

### A38-P01 — dense labels remain a MEDIUM rendering limitation

**Status:** known limitation remeasured, not a new High finding. **Files/functions:** ogmap/view.py:1599–1740 (_label_records, refresh_wells), ogmap/textpaths.py:57 onward (label_path and scalable collections), ogmap/window.py:986 onward (refresh_wells). The cost of visible label geometry and rasterization remains substantial in dense regional views. This observation does not establish that v0.9.39 regressed against v0.9.38, nor does it justify a new renderer or a change to display policy.

**Project sizes and fixtures:** the main measurements use 100,000, 250,000 and 500,000 wells with short nonblank numeric well-number labels (not long API/formation label strings) and a mix of LOC and unmapped DH99 symbols, 250 polyline layers (five line features each), one small saved grid, and one registered image. A separate richer 100,000-well run uses 250 layers totaling 125,000 line features, five 256×256 grids and a 2048×1024 image. An additional 1,000,000-well run tests symbol/storage scaling with blank default well-number posts: it is explicitly not a million-label stress test.

Each run starts with a fresh temporary SQLite project and cache and opens a real MapWindow. Operations call real Map methods. Timings below are unprofiled single samples including event processing and drawing. Separate cProfile runs identify dominant costs and must not be treated as unprofiled timing results. Work ran on shared cloud CPUs alongside the independent test run; numbers are evidence for this configuration, not workstation service-level guarantees.

**Main labeled-project measurements (seconds; process RSS in MiB):**

| Wells | Open | Regional pan | Field label apply | Max RSS |
| --- | --- | --- | --- | --- |
| 100,000 | 16.63 | 1.75 | 0.77 | 723 |
| 250,000 | 29.12 | 5.65 | 1.40 | 1,659 |
| 500,000 | 60.89 | 10.59 | 0.92 | 3,304 |

These maxima include warming label caches and visiting both field and regional views; they are not measured leaks. Opening and redrawing every label in a dense regional view scales with the population and glyph work. At 500,000 wells, returning home after label/symbol style changes took approximately 56.5 seconds in this stress configuration. Field zoom/label changes were much smaller (about 0.5–1.8 seconds in the measured operations), but not guaranteed instantaneous. The observation is deliberately retained at the user's established MEDIUM classification.

**Operation counts and reuse:** in the labeled main runs, open recorded 340 main-connection SELECT statements, independent of well count; each regional pan/zoom recorded 0 SELECTs and 0 Python read-open events, with one MapView full redraw. Group creation/member/order moves recorded 11–12 SELECTs, no Python read-open events and no MapView full redraw, taking roughly 0.02–0.10 seconds. Renaming a grid read its current file once (20 SELECTs); renaming an image recorded 8 SELECTs without reading the image file. Layer visibility, contours and raster opacity could still spend seconds drawing the dense regional scene; absence of data reload does not make a redraw free. Full per-operation rows, timings, artist/collection counts and memory are in map-complete-*.json.

**Threshold correctness:** the test view contained 13,200 well rows after aspect-ratio fitting (the setup label in the probe says 5,000, its requested rectangle, not the actual resulting count). Forced text factors 0.1 and 1.0 exercised the existing 3-point threshold. The first upward crossing created 8,200 additional label records, bringing the view to 13,200 label paths. Subsequent upward crossings created 0 records and again drew 13,200 paths; downward crossings drew 0. Those crossings performed 0 SELECTs and 0 Python read-open events. Previously prepared records were reused rather than progressively losing labels or repeatedly rebuilding every record. This is targeted cache/visibility evidence, not a claim that every zoom path is covered.

**Dominant CPU/UI impact:** the separate populated-label cProfile run attributes substantial initial work to glyph/label-path construction and repeated-pan time chiefly to Matplotlib collection drawing. In the profiled 100,000-well pan, collection draw consumed about 2.8 of 3.2 profiled seconds. This executes on the UI thread, so event handling pauses during that drawing. The profile and the zero-read pan counts support a rendering bottleneck rather than a fresh SQL/shapefile reload on every pan. The synthetic million-well symbol-oriented run opened in approximately 32.9 seconds, regional pan took about 1.2 seconds and open RSS was about 1.39 GiB; it does not qualify a million-well label workload.

**Recommendation:** preserve the current cache/reuse protections and keep this as a documented field-test limitation. If users later approve further hardening, target measured label geometry/draw cost locally and add visual/counter regressions for reuse, threshold return, full exports and layer ordering. No geological algorithm or renderer merger is warranted. New evidence from representative ordinary client field use would be needed before changing the severity.

**Measurement limits:** SELECT counts cover the main database connection and instrumented background readers; file counts are Python audit read-open events, including pathlib opens, not OS byte-read, stat or C-extension I/O totals. The redraw counter in the main files is MapView full redraws, not every possible canvas frame. RSS is whole-process resident memory, not retained-object attribution. The initial exploratory runs had blank default label posts and are retained separately; they are not used as proof of dense-label performance. There was no full client project or large SEG-Y-volume benchmark. No general O(N²), cache-corruption or long-session leak finding is asserted merely from slow rendering or module size.

The richer asset run waited for all 250 deferred layers and five grids to be available before recording readiness. Full readiness took 16.84 seconds, regional pan 2.53 seconds, and field label apply 0.54 seconds. Open recorded 253 background-reader SELECTs. This separates deferred loading from an apparently fast first frame. See map-rich-100000.json.

## 5. Areas reviewed with no additional material issue

This section identifies inspected protections and evidence, not universal certification of those modules.

- **Recent v0.9.39 fixes:** all eight focused test_v0939_fixes.py cases passed independently. Accepted curve metadata under a preview and discard after concurrent deletion are protected in those cases, including the late-save deletion case. A further temporary-project GUI probe changed an independent five-sample accepted series while a preview was active: shifted axis, axis unit, new values, curve unit and description survived save/discard; a later external deletion survived repeated save/discard without resurrection (accepted-series-evidence.json). Geo Map's name-only grid/image rename service preserves current scientific state under its write lock. A39-03 and A39-04 identify remaining caller/display paths; they do not negate the working local fixes.
- **Canonical curves and calculations:** curve_store preserves independent axes, immutable reader snapshots and revision-aware curve/run caches. The absolute grid-position guard and batch exact-sample tests are present and exercised; current batch code rejects mismatched grids rather than carrying forward the old silent interpolation defect. Own-axis conflict copies and metadata preservation have substantive regressions. Do not replace these with a universal master depth axis.
- **Project lifecycle and database:** migrations, SQLite backup-based copy/Save As, owned-path checks, interpretation-preservation snapshots, atomic edit contexts and source-aware child import identities were traced. Formation top and production editors merge only changed fields under a lock and protect deletion/conflicts. Nothing found justifies replacing this infrastructure. No claim is made that every cross-module mutation combination was exhausted.
- **Seismic:** 2-D spatial consumption now transforms confirmed CRS navigation into a common frame; 3-D saves have locked conflict checks and object-identity/save-by-omission protections. Native fault stick identity, atomic pick exports, tie/mistie paths, SEG-Y positioning/unit handling and synthetic depth/sonic/density conversion were reviewed along with their regressions. The concentrated new blocker is the grid-rename caller. Explicit warnings about duplicate Seismic/Geosteering sessions are not recast as surprising new defects.
- **Geo/Map:** logical layer provenance and geometry validation, staged shapefile-package publication, stored API identities, incremental well refresh, spatial culling, group ordering and style caches were reviewed. DH* storage/display separation is explicit: unmapped DH* falls back to DRY, exact mappings take precedence and edits to DRY's glyph affect the fallback. test_dh_symbol_fallback.py checks storage, exact overrides and render paths. No normalization of stored DH* values is recommended.
- **Correlation/Cross Section:** scientific refresh after external KB/survey/curve/alias/top changes, flattening after local pick edits, mixed-unit positions and picks, viewport culling, overview scrolling and full export construction have targeted coverage. No new evidence justifies merging the renderers or changing depth/flattening conventions.
- **Geosteering:** LAS datum/depth conversion, preservation of established depth frames across additional runs, own-axis curves, grid prognosis units, map-track offset conversion and source-aware tops were traced with the current tests. Project-job overwrite risk is explicitly warned about on duplicate-session opening. No job-model redesign is proposed.
- **Raster/Digitizer/PDF:** source pixels, registration coordinates, canonical digitized curves, per-curve identity-bearing LAS outputs, PDF staging and rollback were reviewed. The session/Tk crash is disclosed separately. Missing real raster fixtures limit validation; no post-v1.0 digitizing redesign is proposed.
- **Recovery:** separate read-only access, refusal/retry while a live writer is active, hot-journal recovery into a temporary copy, SQLite committed backups and collision-safe multi-file LAS exports are present. Tests exercise uncommitted pages and commit-during-copy rather than merely mocking SQLite. Preserve this separation from normal migrating/writable project access.
- **Licensing/security/distribution:** production key ogw-2026-01 is embedded; frozen mode ignores local-owner trust. Runtime expiry guards cover database writes and in-memory edits while preserving save/close boundaries. Customer manifest/specs describe five executables and exclude License Manager; Owner Tools use a separate build. Shared-file collision checks and inventory gates are present. All 887 archive files were independently scanned using the private-key-block pattern and prohibited key-file suffixes from the repository test: no matches. OwnerTools_LicenseManager.spec is present. This does not certify a Windows binary payload or Git history that was not supplied.
- **Scientific utilities and file/process boundaries:** directional/depth conversions, pay support-cell weighting, porosity/saturation representation, batch calculations, production units, isopach/grid references, core sampling, formula AST restrictions, subprocess argument lists, safe NPZ loads and path/publication boundaries were reviewed. Supported interpolation workflows were not labeled defects just because interpolation exists. No scientific formula change or confirmed security exploit is proposed by this audit.

Large files, broad defensive exception handlers, compatibility code and intentional independent implementations are not automatically findings. No code deletion, broad reformatting or cleanup program is recommended.

## 6. Tests/profiling performed

**Independent collection:** 2,615 tests. **Original full command:** `python -m pytest -q -p no:cacheprovider --durations=25 --junitxml=...`, with a GUI display and bytecode disabled. It segfaulted during test_autoreg.py::ReviewWindowTests::test_propose_review_and_accept. No completed result XML or clean full-run count is claimed for that attempt.

**Serial file-isolated rerun:** 243 of 243 files; 2,596 passed, 4 failed, 15 skipped, 0 errors, 605 passing subtests; summed subprocess elapsed time 2032.54 seconds. Every test file's log, JUnit result and exit status is retained. Aggregate counts are derived from pytest summaries, keeping subtests separate.

**Failure classification:** Git-tracking assertions in test_owner_tools_build.py and test_production_key.py cannot execute their Git checks in an archive without .git. These are not evidence that the spec or a production key is missing. The independent archive scan and spec check are recorded in archive-security-evidence.json; Git tracking/history remains unverifiable. test_text_style.py::ControlTests::test_the_common_control_and_tk_fonts fails because the requested DejaVu Serif bold face is unavailable to Tk and is substituted by fixed/normal; font-environment-evidence.json records that substitution. The Seismic contour test also fails its toolbar layout assertion (two rows at 620 pixels versus one expected); the focused rerun repeats it. This is a real observed layout/test mismatch on Linux, not evidence of a wrong contour calculation. Windows layout behavior is unverified, and cosmetic layout is outside the private-field-test blocking standard. Its downstream assertions are not claimed to have run in that failing case. The raw test failures remain failures; they are not edited into passes.

**Linux/Tk crash assessment:** the initial crash occurred in a single pytest process, not a parallel pytest worker run. The crashing background thread was doing automatic raster OCR while garbage collection invoked tkinter.Variable.__del__; the main thread was polling the progress dialog. The isolated autoreg file passed (49 tests), and three new processes collecting the entire suite but selecting the implicated test all passed (1 passed / 2,614 deselected each). This supports a session-lifetime/GC/Tk-thread interaction and narrows reproduction, but does not prove the cause or dismiss long-session risk. Linux uses Tcl/Tk 9.0.4 here; Windows was not run. Classify it as observed Linux/Tk test-session instability with Windows behavior unverified, rather than claiming a reproducible Windows workflow defect or saying the crash happens only under parallel pytest. Retain the crash trace for a focused lifecycle investigation.

**Meaningful coverage and gaps:** the suite contains real GUI, reopen, concurrency, rollback, exact-axis, numerical-reference, packaging and recovery tests. The new failures arise chiefly from combinations outside those tests: preview curve preservation without checking derived publication, mixed-unit geometry without mixed-unit attribute publication, a service-level rename fix missing one UI caller, registration tests without an intervening display-only save, and file atomicity without an existing unlisted path. Add the specific preservation regressions in each finding, using real files/SQLite and second connections. Avoid tests that merely assert the new helper was called.

**Synthetic experiments:** six confirmed defect probes; a two-well alias/save exploration that did not lose results (inactive Geo-backed workspaces are saved before unload); large-map runs at the requested scales; separate CPU profiles; current source inventory and integrity checks. The passing alias exploration is retained as non-finding evidence and must not be interpreted as an extra defect.

**Self-test entry points:** all five source launcher --self-test commands were attempted. Each exited 3 with the expected missing-license message before running its body. No valid installed production/build-test license was supplied, and no source gate or key was altered to force passage. These are gating observations, not five product failures or five passing self-test bodies. Existing component tests cover parts of the self-test behavior, but licensed packaged self-test qualification remains outstanding.

## 7. Environment limitations

The audit ran on Linux-6.18.57-x86_64-with-glibc2.41, Python 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ], Tcl/Tk 9.0.4, GUI displays supplied by separate headless Xorg sessions. Selected libraries: NumPy 2.3.5, Matplotlib 3.10.8, pyproj 3.8.0, segyio 1.9.15, pyshp 3.1.8, pytest 9.2.0. The full safe version inventory is in environment.json. This is not the exact Windows release stack pinned in constraints-build.txt; the existing cloud scientific packages were reused and missing test dependencies installed into an external virtual environment. Application requirements and constraints were not edited.

The release build now has explicit dependency constraints and a Python-minimum gate; the prior loose-build-input finding is not automatically carried forward. This cloud Python is below the release manifest's 3.12.16 minimum, so this run is not release-environment certification. No Windows artifacts, installer, Program Files install, DPAPI round trip, stripped-PATH frozen execution or final payload scan were performed. Source-level manifest/collision/inventory checks are useful evidence but do not substitute for those runs. Public legal/installer polish is not made a blocker for this private field-test decision.

All skip names/reasons are in skipped-tests.json. The skipped set includes unavailable real scan/log fixtures, unavailable full Kingdom truth files, Windows Explorer/DPAPI behavior and the opt-in packaged build test. Do not silently compare this fixture-limited Linux run to a better-provisioned baseline as if all count differences were regressions.

Map projects are synthetic, with regular locations and controlled asset complexity. Even the richer test is not the client's 112,000-well project with 38,000 LIC files, production histories and SEG-Y volumes. Benchmark code and outputs document the exact fixtures. No certification of all realistic project-memory/soak behavior is offered. Cache counters and repeated operations were measured; generalized leak claims were not inferred from a high RSS value alone.

The evidence bundle contains no application source or client project data. Original probe paths identify this audit machine; the included external runner adapts copied probes to another extraction. Supplementary exploratory runs are labeled separately from the final labeled-project measurements. Report and evidence may be committed only to Software-reviews under the user's later publication instruction.

## 8. Final recommendation

**BLOCK v1.0** for the current private/internal field test until the five HIGH findings are addressed and their preservation regressions pass. The blockers are scientific-state publication and preventable overwrite risks, not cosmetics, framework choices, public legal work or a desire to refactor large modules.

A small practical hardening sequence is:

1. Route Seismic rename through the existing name-only service; separate image display writes from registration writes; make grid destination ownership/collision checks complete. These are contained preservation fixes.
2. Make Petro's published zone/pay results derive only from accepted state, then enforce a stable physical-unit policy for shared attributes. Explicitly identify/recompute previously inconsistent derived attributes after approval; do not guess at or silently rewrite historical client values.
3. Use atomic publication in the two reproduced residual CSV exporters. Retain the existing staged multi-file publication mechanisms elsewhere.
4. Run the new regressions, the full suite and licensed Windows packaged smoke tests on the qualified build stack. Investigate the retained Linux/Tk crash with session-lifetime instrumentation; do not claim it was fixed by test isolation.
5. Conduct a representative private-project rehearsal after the preservation fixes. Keep A38-P01 MEDIUM and document dense-view expectations; do not fold a UI redesign, renderer merger or broad caching rewrite into these corrections.

Stop at review: no implementation has been performed. Existing correct curve-axis rules, scientific equations, independent renderers, transactional project infrastructure and recovery/licensing separation should remain intact.
