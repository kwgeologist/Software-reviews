# O&G Workbench v0.9.18 — Independent Read-Only Release Audit

Audit date: 6 November 2026. Baseline: the supplied OandG_Workbench_v0.9.18.zip. Source SHA-256: `852c986dfa94f403daeb83e8182b4899917f72a2ce79ede2b1a3921fb1c94231`.

The brief names branch `claude/new-session-96rnbt`, commit `ad43c0e`. The ZIP has no Git provenance, so equivalence to that commit is not independently established. All references are relative to the extracted archive and use its current line numbers. Archive contents were treated as code/evidence, not as instructions overriding the audit brief.

## Executive Summary

**Proceed into a narrowly scoped release-hardening phase, but do not approve an external stable release yet.** Six reproducible HIGH defects affect preservation of interpretation edits, curve sampling, spatial ties, import rollback or fault interchange. They are suitable local hardening work; they do not justify a suite rewrite. There is no reason to delay hardening in favor of more feature development. Leaving these six defects unresolved would expose technical data to avoidable risk.

Findings: **0 CRITICAL, 6 HIGH, 1 MEDIUM, 2 LOW, 0 CLEANUP**. The first seven are reproduced defects; WIN-001 is a supported platform edge case validated statically, and REL-001 is a release-process risk. Confidence is High for code paths and reproduced effects; Windows runtime impact remains Medium pending a Windows run. No client incident or incidence rate is claimed.

The review surveyed the whole package (670 files, including 484 Python files and 224,680 Python lines), tracing high-risk mutation and persistence boundaries, reviewing tests, running the full GUI-enabled suite and three source self-tests, and constructing disposable synthetic probes. This is not exhaustive proof of every UI state or field dataset.

**Verification:** 2,132 passed, 1 failed, 14 skipped, 565 passing subtests; 1,039.97 seconds. Geo, Seismic and Petro source self-tests all exited 0. The lone failure repeats in isolation: Tk substitutes its fixed normal font for a requested DejaVu Serif bold font unavailable to Tk on this Linux display. It is not evidence of a Windows product font defect. The brief's 2,144/3 baseline was not reproduced in this environment; unavailable fixtures/platform checks and the font failure account for the count difference, rather than twelve demonstrated product regressions.

**Read-only guarantee:** every one of the 670 archive files was compared byte-for-byte after testing: no changed, missing or additional source files. Probes, temporary projects and reports were written outside the application tree. No code, tests, dependencies or application documentation were changed. No commits or pushes were made. The withdrawn toolbar screenshot request is excluded.

## Release Blockers

These HIGH findings should be resolved and regression-tested before external release. No CRITICAL finding is asserted.

### DATA-001 — Shared 2-D Undo overwrites another window’s newer edit

**Severity:** HIGH. **Component:** Seismic / concurrent windows. **Confidence:** High.

**File(s) / functions:** seismicworkbench/section2d.py:95–138, 479–503; seismicworkbench/ties_ui.py:81–94; seismicworkbench/interp_registry.py:158–177

**Finding:** reload_picks replaces displayed picks but retains whole-array Undo snapshots. Undo restores an old entire object array, then save_line_picks deletes/reinserts that line’s picks.

**Evidence:** The actual Section2DView methods and same-application broadcasts were exercised against SQLite. Starting [100, missing, 200], A edits trace 0 to 110 and B edits trace 2 to 220. A receives the refresh; Undo in A writes [100, missing, 200], erasing B’s 220. See undo-shared-line-evidence.json.

**User impact:** A normal Undo can silently discard another open view’s accepted interpretation.

**Trigger:** Two section windows in one Seismic application edit the same horizon/line, then one uses an older Undo entry. This does not require a second application session.

**Existing test coverage:** test_seismic_2d_interpretation.py covers picking, interval/box operations and single-view Undo; no interleaved two-view Undo preservation case was found.

**Recommended action:** Use edit deltas or revision-aware shared Undo; at minimum invalidate stale history on external reload with clear behavior. Do not replace the interpretation architecture.

**Regression tests:** Interleave edits in two real views, Undo each, reopen SQLite, and assert unrelated edits survive. Include redo if supported.

**Change risk:** Moderate — touches edit history, persistence and view broadcasts.

**Audit probe:** `evidence/probes/undo_shared_line.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

### SEIS-001 — 2-D tie calculations compare coordinates from different CRSs directly

**Severity:** HIGH. **Component:** Seismic positioning / ties. **Confidence:** High.

**File(s) / functions:** seismicworkbench/nav_import.py:132–160; seismicworkbench/lines2d.py:143–146, 284–378; seismicworkbench/ties_ui.py:216–225, 295–378

**Finding:** Navigation retains raw coordinates and source CRS metadata. Geometry retrieval and tie intersection calculations consume those raw coordinates without transforming or rejecting incompatible CRSs.

**Evidence:** Two physically crossing lines were stored in EPSG:32613 and EPSG:4326. ties_of_line returned zero ties between them; transforming both to the common projected CRS gives one intersection. See seismic-boundaries-evidence.json, mixed_crs_tie. Raw source storage itself is not the defect.

**User impact:** Valid intersections are missed, making ties and subsequent mistie review incomplete or misleading. The map path also consumes raw line geometry and needs the same boundary check.

**Trigger:** Import line navigation in different explicitly identified CRSs into one project and calculate ties.

**Existing test coverage:** 2-D navigation tests retain CRS metadata, and tie tests cover common-coordinate cases. No mixed-CRS intersection reference test was found. Vertical ft/m tests do not cover this condition.

**Recommended action:** Transform geometry into a confirmed common/project CRS at the spatial-consumer boundary, preserving source coordinates and metadata; reject known incompatibility if transformation is unavailable.

**Regression tests:** Crossing and noncrossing mixed-CRS lines, equivalent projected/geographic inputs, unknown CRS handling, and 2-D/3-D tie consistency.

**Change risk:** Moderate — common geometry consumers need consistent CRS and unit reference cases.

**Audit probe:** `evidence/probes/seismic_boundaries.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

### DATA-002 — Petro preview and discard lose an existing curve’s independent depth axis

**Severity:** HIGH. **Component:** Petro calculations / persistence. **Confidence:** High.

**File(s) / functions:** petroworkbench/calculations.py:722–755, 821–927, 947–960; petroworkbench/well_data.py:34–44; petroworkbench/geo_link.py:418–466

**Finding:** Preview backup retains aligned curve values and metadata but not the independent series depth vector. Replacement changes array identity, allowing sync_series to drop the original series. Preview persistence writes the backup against the master depth vector; discard restores only the aligned values.

**Evidence:** A saved five-sample OWN curve at 1010–1012 was used in the real formula-preview path OWN = OWN * 2. Saving the workspace during preview stored 9,361 samples; discard and save still stored 9,361, and has_own_depth became false. See petro-preview-evidence.json. This establishes axis/extent/null-sample mutation, not loss of every original finite value.

**User impact:** An unaccepted calculation changes the canonical curve sampling and a subsequent discard does not restore it. This violates the explicit per-curve real-depth contract.

**Trigger:** Preview a formula replacing an existing curve with an independent axis, then save the workspace and/or discard.

**Existing test coverage:** Own-axis editor/resampling and common-grid preview persistence have coverage in test_curve_editor_v096.py and test_petro_canonical_curves.py. Their combination with preview, workspace save and discard is missing.

**Recommended action:** Snapshot and restore the complete depth/value/metadata series. Preview persistence must use that original axis rather than promoting an aligned display array.

**Regression tests:** Independent-axis curve: preview, workspace save, discard, close/reopen, compare exact depth/value arrays; separately accept and verify intended new data.

**Change risk:** Moderate — preserve accepted versus working-state behavior across calculation and save paths.

**Audit probe:** `evidence/probes/petro_preview.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

### IMPORT-001 — Cancelled PPF re-import rolls back SQLite but leaves an existing generated LAS overwritten

**Severity:** HIGH. **Component:** Petra PPF / filesystem transaction. **Confidence:** High.

**File(s) / functions:** ogcore/petra_ppf.py:905–932, 1159–1170, 1521–1566

**Finding:** Generated LAS names are deterministic. _write_las opens an existing destination for replacement, but tracks only previously nonexistent files in p.written. The outer failure handler removes newly written files without restoring overwritten files.

**Evidence:** A first import saved GR [10,20,30]. Re-import changed the first well to [99,88,77], then cancellation occurred at the second well. Database GR rolled back to [10,20,30], while the existing LAS contained the new samples and its old bytes were lost. See ppf-rollback-evidence.json.

**User impact:** The database and project-owned generated LAS disagree after an operation reported cancelled. Original generated-file contents are not restored. This is not a claim that the database rollback failed.

**Trigger:** Re-import the same PPF/group to an existing generated LAS path, allow value replacement, then cancel or fail after that write.

**Existing test coverage:** test_petra_ppf.py:365–383 checks cancellation into an empty project and cleanup of newly created files, not restoration of pre-existing outputs.

**Recommended action:** Stage/backup both new and existing LAS outputs and coordinate publication/rollback with the outer database transaction, using the existing safe-file service.

**Regression tests:** Re-import changed samples, cancel after the first overwritten file, and compare original file bytes plus database values; repeat with injected write/import failure.

**Change risk:** Moderate — filesystem publication must remain coordinated with SQLite rollback.

**Audit probe:** `evidence/probes/ppf_rollback.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

### EXPORT-001 — Native fault interchange collapses distinct sticks with the same display/native ID

**Severity:** HIGH. **Component:** Seismic fault import/export. **Confidence:** High.

**File(s) / functions:** seismicworkbench/interpretation.py:118–137; seismicworkbench/project.py:52; seismicworkbench/picks_io.py:681–728, 815–830

**Finding:** The internal model distinguishes stick_key from stick_id. Export writes Stick from stick_id or section and omits stable stick_key. Re-import groups by the exported field and constructs nodes without the original stable key.

**Evidence:** Two three-node sticks with distinct stable keys, both native ID 7 and section ARB, exported as Stick=7. Re-import reported six nodes written without conflict, but yielded one stick with sequence [1,1,2,2,3,3]. See fault-export-evidence.json.

**User impact:** A native round trip changes fault topology and can connect independent sticks. The current internal merge fix is present; this finding concerns the interchange boundary.

**Trigger:** Export a fault containing distinct source sticks sharing a native/display ID, then import the native output.

**Existing test coverage:** test_seismic_picks_io.py:90–137 covers a unique-ID round trip. test_audit_v095.py protects merged identities internally, without this export collision case.

**Recommended action:** Preserve stable stick identity separately from the native/display identifier in the interchange format; retain backward-compatible reading of existing files.

**Regression tests:** Merge or construct two same-ID source sticks, native export/import, reopen project, assert groups, node order, coordinates, units and identifiers are preserved.

**Change risk:** Moderate — format evolution requires backward compatibility and topology checks.

**Audit probe:** `evidence/probes/fault_export.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

### BATCH-001 — Batch curve calculations silently resample inputs and reject saved own-axis curves

**Severity:** HIGH. **Component:** Batch curves / shared geological model. **Confidence:** High.

**File(s) / functions:** ogcore/batch_curves.py:195–259; ogcore/batch_zones.py:451–531; database.py:3293–3311

**Finding:** Batch calculate_well chooses petro_depth or an initial axis and resamples other inputs without an explicit common-sample check. Its calculated-curve reader uses the legacy calculated_curves view, which intentionally excludes own-axis curves.

**Evidence:** A=[10,20,30] at [1000,1001,1002], B=[100,200] at [1000.5,1001.5]: OUT=A+B writes 170 at 1001 although B has no sample there, with no resampling warning. A valid saved own-axis OWN curve is readable canonically but COPY=OWN*2 is skipped as having no saved values. See batch-grids-evidence.json.

**User impact:** The same formula has different sampling rules between Petro and batch; derived geological values may contain silently invented input samples, and valid curves are unavailable to batch.

**Trigger:** Batch formulas use mismatched real depth vectors or an accepted calculated curve on its own axis.

**Existing test coverage:** test_batch_curves.py exercises formulas on common sampling. Petro grid-guard tests cover UI rejection, not this batch entry point. No corresponding mixed-axis or own-axis batch case was found.

**Recommended action:** Read canonical per-curve depth/value arrays and apply the same explicit exact-common-sample policy as Petro. Diagnose mismatches or require an explicit resampling workflow. Do not change intentional zone aggregation/interpolation semantics merely by association.

**Regression tests:** Batch and Petro parity for exact, offset and irregular grids; independently sampled calculated inputs; missing samples and no silent interpolation.

**Change risk:** Moderate — existing batch jobs may depend on implicit behavior and need explicit migration/diagnostics.

**Audit probe:** `evidence/probes/batch_grids.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

## Medium Findings

### FILE-001 — Failed native CSV export can destroy a previous completed export

**Severity:** MEDIUM. **Component:** Seismic file output. **Confidence:** High.

**File(s) / functions:** seismicworkbench/picks_io.py:881–888

**Finding:** The exporter opens the destination directly with mode w, writes headers, then writes records. It does not publish a completed temporary file atomically.

**Evidence:** An existing reviewed export was replaced by headers when an OSError was injected into DictWriter.writerows. The exception propagated, but old bytes were not preserved. See output-boundaries-evidence.json, failed_export.

**User impact:** A disk-full or interrupted export can replace a useful existing export with partial output. The source database is not changed.

**Trigger:** Overwrite an existing export and fail after truncation but before all records are written.

**Existing test coverage:** Successful export/round-trip tests exist; no failed-write preservation test was found.

**Recommended action:** Use the existing atomic_write helper to publish only a fully completed CSV.

**Regression tests:** Inject failure during header and row writes; compare destination bytes and check temporary-file cleanup, then verify successful replacement.

**Change risk:** Low — localized output publication change.

**Audit probe:** `evidence/probes/output_boundaries.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

## Low Findings

### WIN-001 — Filename sanitizers accept Windows reserved device basenames

**Severity:** LOW. **Component:** Windows project/grid paths. **Confidence:** Medium for Windows runtime impact; High for the validation gap.

**File(s) / functions:** ogcore/project.py:100–105 (_safe_name); ogmap/grids.py:265–282 (_file_name)

**Finding:** Helpers strip forbidden characters and trailing punctuation but retain CON, NUL and AUX as basenames, including grid filenames such as CON.oggrid.

**Evidence:** Calling the actual helpers retained these names; PureWindowsPath classified them as reserved. See output-boundaries-evidence.json. This is static Windows-path validation, not a Windows I/O reproduction.

**User impact:** An edge-case project/grid name can fail on Windows despite passing local sanitization; choosing another name is a workaround. No data loss was demonstrated.

**Trigger:** User names a project or grid after a reserved Windows device.

**Existing test coverage:** Filename normalization tests exist; reserved device-name coverage was not found.

**Recommended action:** Reject or safely suffix reserved basenames through a shared small validator. Do not rename existing projects automatically.

**Regression tests:** CON/NUL/AUX/COM1/LPT1 with extensions, case variations, ordinary Unicode names and trailing dots/spaces.

**Change risk:** Low — contained validation with backward compatibility for existing paths.

**Audit probe:** `evidence/probes/output_boundaries.py`. Synthetic or controlled-failure reproduction; not a claim of observed client corruption.

### REL-001 — Release build inputs drift because dependencies are not locked

**Severity:** LOW. **Component:** Build/distribution reproducibility. **Confidence:** High.

**File(s) / functions:** requirements.txt; requirements-dev.txt; Build_Windows_EXE.bat:8; .github/workflows/windows.yml

**Finding:** Runtime requirements use lower bounds; development tools such as pytest/PyInstaller also float. The Windows build upgrades from these specifications, and CI uses windows-latest rather than a recorded qualified build environment.

**Evidence:** The supplied build inputs contain no exact qualified dependency lock or wheel/hash manifest. Rebuilding later can resolve different versions without a source change. This is a confirmed reproducibility risk, not evidence that the present executable is broken.

**User impact:** A later release rebuild may differ from the tested dependency stack and be harder to diagnose or reproduce.

**Trigger:** Fresh build after package releases or CI image changes.

**Existing test coverage:** Windows CI builds executables and exercises packaged behavior, but that does not freeze or prove repeatability of the resolved build inputs.

**Recommended action:** Record a qualified release dependency/wheel/hash manifest, Python and build-OS versions; broad development specifications can remain. No dependency update is requested by this audit.

**Regression tests:** Build twice from the qualified manifest in clean environments and record dependency and resource inventories; smoke-test every executable.

**Change risk:** Low — release procedure/input capture, without changing scientific code.

## Cleanup Opportunities

No standalone cleanup finding is recommended for this hardening scope. Apparent duplication, compatibility paths, broad exception handlers and older modules are not sufficient evidence of dead code. No deletion is proposed without a demonstrated unused/superseded path. The independent rendering implementations should remain independent.

## Test Coverage Assessment

The suite has meaningful coverage: current regression cases exercise migration/save preservation, shared interpretation identities, 3-D conflict handling, native import edge cases, Map layer compatibility/provenance, canonical curves, explicit Petro grid guards, scientific reference cases, raster workflows and packaging helpers. Existing tests were searched before marking gaps. Current v0.9.5-era regression tests were run; old audit findings were not automatically carried forward.

The principal weakness is composition across boundaries. Single-window Undo tests miss interleaved shared-view edits; internal stick-identity tests miss interchange; common-grid preview tests miss own-axis persistence; empty-project cancellation misses overwritten files. Add the focused tests specified for the six HIGH findings first, using actual persistence and reopening rather than mocking away the boundary.

The 14 skips comprise eleven unavailable real raster/log fixture cases, one Windows Explorer-drop case, one unavailable full Kingdom reference-data case, and one opt-in frozen-package test. The complete names/reasons are in evidence/skipped-tests.json. These are material limits on real-input and distribution confidence, not proof those workflows fail. The font failure and diagnostics are retained separately. No suite crash was observed in this run.

Performance coverage does not certify the user's entire 100,000+ well project, 200-layer maps or full SEG-Y volumes. No representative client-scale soak test was performed. A 2-D section read materializes a full trace matrix (section2d.py:81–94 and the underlying line read); 25,000 × 6,000 float32 samples alone would be about 572 MiB per view. That is an arithmetic capacity estimate, not a measured leak or new release blocker. Qualify representative large projects with repeated open/change/close, memory high-water and retained-memory measurements before making scale guarantees. Do not introduce speculative caching or renderer rewrites from this observation.

Numerical checks and source review do not justify changing established pay, petrophysical, production, directional or interpolation algorithms. The confirmed numerical concerns here are input-axis consistency and CRS comparison boundaries. Tests passing on reference examples are not universal geological certification.

## Packaging / Clean-Machine Risks

Windows build scripts, PyInstaller configuration and CI were inspected. CI has executable-build and stripped-environment/package smoke coverage, including PDF behavior. Source self-test success is not equivalent to that packaged evidence: no frozen Windows binaries were supplied or executed in this audit. Clean Windows installation under Program Files, normal user-data locations, executable relationships, PDFium/SEG-Y loading and all executable self-tests remain qualification gates. The reserved-name and reproducibility findings are WIN-001 and REL-001; no unsupported missing-DLL claim is made.

No confirmed active developer-machine absolute-path dependency, installation-directory write defect, credential leak, arbitrary project pickle execution or shell-injection path was established in the reviewed boundaries. Array loads use safe pickle settings, formulas have restricted parsing, and inspected subprocess paths use argument lists. This is a desktop-appropriate review, not a penetration-test certification. Keep malformed-file and path-containment tests; do not add a licensing/security redesign to this scope.

## Recommended Release-Hardening Scope

1. Repair DATA-001 and DATA-002 first: interpretation Undo preservation and accepted curve state are direct normal-workflow risks. Add reopen-based regressions before touching implementation.
2. Repair IMPORT-001 and EXPORT-001: transactionally preserve existing generated outputs and retain fault topology through interchange.
3. Repair SEIS-001 and BATCH-001: enforce common spatial/sample coordinates at the existing consumer boundaries, without changing geological formulas.
4. Include FILE-001 as a small output-preservation change. Keep unrelated UI or architectural work out of these patches.
5. Qualify the resulting build on a clean Windows machine and representative large projects. Record exact release build inputs; address reserved-name validation locally when preparing distribution.

Use separate focused changes, rerun each new regression and its component suite, then run the full suite and packaged smoke tests once the fixes are integrated. No broad modernization or new feature is required to make this plan reviewable. The two LOW items do not independently justify delaying the six HIGH fixes.

## Do Not Touch

- Preserve independent Map, Petro, Correlation, Cross Section and Geosteering renderers. No evidenced defect requires merging them or redesigning their UI.
- Preserve current 3-D object identity, save-by-omission protection and conflict detection. These are substantive protections; do not replace them with blanket snapshot saves.
- Preserve SQLite backup/conversion safeguards, owned-path containment and interpretation snapshot checks. The PPF defect needs filesystem rollback at one boundary, not a project-storage rewrite.
- Preserve staged logical Map-layer append, geometry compatibility, per-feature provenance and existing shared styles. No broad replacement is justified by this audit.
- Preserve canonical per-curve depth vectors and Petro's explicit common-sample policy. Align the identified preview and batch boundaries to them; do not weaken the rule for convenience.
- Preserve established scientific engines and intentional interpolation workflows. Sampling/CRS defects do not establish that the equations themselves are wrong.
- Preserve background-task connection/thread ownership and lifecycle generation checks unless a specific failing workflow is demonstrated. No general memory-leak finding is supported here.
- Do not resurrect prior findings merely because a historical note mentions them. Separate Seismic-session overwrites are explicitly warned about before opening a second session; exploratory duplicate-session probes are not reported here as unqualified new defects. DATA-001 reproduces within one application and is distinct.

## Evidence and Reproducibility

The companion bundle contains this one report in Markdown/PDF/HTML, synthetic probe scripts, JSON observations, full test log/JUnit results, skipped-test and font diagnostics, source self-test results, scope brief and source-integrity result. No application source or client dataset is bundled. Original probe paths document this audit machine; adapting them to another extraction requires changing only the external probe copies. GUI probes need a working Tk display and the application/test dependencies. All probes use disposable synthetic projects. Some JSON observations contain missing numerical samples; the packaged copies normalize those to null.

Exploratory evidence is broader than the findings: seismic-boundaries-evidence.json also contains duplicate-session and stale-delete experiments, and petro-preview-evidence.json includes a tolerance observation. These are retained for transparency and are not promoted to extra defects without the supported workflow/effect needed for this report. The nine findings above are the reviewed conclusions.
