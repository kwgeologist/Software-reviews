# O&G Workbench v0.9.52 — Independent Full Pre-Release Audit

16 November 2026 · Read-only review · Authoritative input: supplied v0.9.52 ZIP

## 1. Executive Result

**Not ready for Windows validation.** One release blocker and five material defects/risks were independently reproduced against the current source. Address geological alias ownership first. No numerical difference attributable to Cython was demonstrated.

This is a fresh whole-package release-candidate review, not a delta approval against v0.9.45. The supplied ZIP’s internal version is 0.9.52; SHA-256 is `e0b5d48346d1e7d3af1feed7b16302b5e409d438acbc57821c721a55b6ff5ecb`. The requested `release/1.0` / `e0255cb` identity cannot be attested from an archive without Git history. All 904 supplied files remain byte-identical, with none missing or added. Builds and audit probes used external/disposable copies and synthetic temporary projects.

Coverage combined the entire collected test suite, package/AST inventory, targeted source tracing, actual Tk workflows, importer calls, two-connection persistence probes, independent numerical references, all 15 compiled modules and both actual Linux PyInstaller specs. This is not a claim that every line or every client-data combination was exhaustively exercised. No real client projects, mature production datasets or Windows runtime were supplied/executed. Historical scripts were re-run against this version; historical results were not accepted as current proof.

## 2. Release Blockers

### A52-01 — Renaming into another top’s alias silently changes geological identity

**Classification:** A. Release Blocker. **Severity:** Critical. **Confidence:** High.

**Files / functions:** database.py:3073, 3090, 3098; geoworkbench/interpretation_dialogs.py:194, 312; ogmap/sources.py. add_top_alias / _record_alias / rename_top_definition; GlobalTopsManager.rename.

**Confirmed behavior:** The rename path checks existing canonical names but deletes a matching alias without checking its owner. Adding an alias uses ON CONFLICT(alias) DO UPDATE and can transfer another definition’s alias. The manager checks only canonical-name clashes, so this can happen without a merge confirmation.

**Evidence:** top-ui-batch-evidence.json: using the actual Global FM Tops Manager, A at MD 100 and B at MD 1000, with B alias “B old”, renaming A to “B old” changes the same untouched Map source from 1000 to 100. merge_confirmation_calls = 0. top-identity-evidence.json independently demonstrates alias transfer through add_top_alias.

**Why it matters:** A legacy name can silently identify a different geological horizon. A Map/grid source or import referencing that alias then selects a different top despite no user-controlled geological merge. This is demonstrated material geological misidentification, not a numerical-equation discrepancy.

**Realistic scenario:** A project contains a legacy vendor name for one formation. A user gives a different formation that name in the manager; subsequent top-based mapping uses the other pick. The evidence is synthetic; no client incident is alleged.

**Smallest safe fix:** Resolve both canonical-name and alias ownership before changing either. Reject a different owner or route through the existing explicit merge confirmation. Never delete/reassign another definition’s alias as a side effect of rename.

**Regression tests:** Actual manager rename and Other Names collision tests; unchanged Map source must retain its original pick; verify import resolution, both definitions’ picks, source/notes and aliases before and after reopen.

## 3. Material Pre-Release Defects / Risks

### B52-02 — A reader can consume a live writer’s staged grid and trigger an inconsistent rollback

**Classification:** B. Material Pre-Release Defect / Risk. **Severity:** High. **Confidence:** High.

**Files / functions:** ogmap/grids.py:222, 317, 375, 423. load / _finish_publication / save.

**Confirmed behavior:** save commits the new database row before promoting the staged file. load treats a matching stage as crash recovery and moves it into place. If a live reader does this first, the writer cannot find its stage, reports failure and restores the old database row, while the already-promoted new file remains.

**Evidence:** grid-reader-publication-evidence.json: two real project connections, with an ordered reader at the post-commit/pre-promote boundary. The reader loads 9000 m; writer raises FileNotFoundError; database row reverts to ft and old updated_at, but reopened file still holds 9000 m and the new notes. No real process kill is required for this race.

**Why it matters:** A failed save can remain partly accepted, and database metadata disagrees with the scientific file. Subsequent operations cannot rely on rollback restoring the previous accepted grid. Probability was not measured; the interleaving is deterministic and reachable with concurrent project sessions.

**Realistic scenario:** Map or another session loads a grid just as a save has committed its row but has not promoted its file.

**Smallest safe fix:** Give publication/recovery a shared ownership or locking protocol spanning commit and promotion. Recovery must distinguish an active writer, and rollback must not restore an old row after another participant has accepted its publication. Preserve the existing before/after-commit crash recovery.

**Regression tests:** Use a barrier with two connections or processes at commit/promote. Assert save outcome, row/file units, versions, geometry and values agree. Repeat for insert/update/rename and retain kill-before/after-commit tests.

### B52-03 — Bulk and mapped alias imports repeatedly duplicate the same canonical pick

**Classification:** B. Material Pre-Release Defect / Risk. **Severity:** High. **Confidence:** High.

**Files / functions:** bulk_import.py:542, 560; mapped_import.py:637, 684; database.py:1559. BulkWorkbookImporter._import_tops / MappedTableImporter.import_all; formation_tops_definition_insert trigger.

**Confirmed behavior:** Import duplicate checks compare the normalized input name literally. The insert trigger subsequently resolves aliases to the canonical definition/name. An alias therefore misses an already-present canonical row on every import.

**Evidence:** import-alias-evidence.json: actual XLSX bulk and CSV mapped import_all calls, existing Canonical pick MD 100 source XON and alias Legacy. Import Legacy once gives two identical canonical rows; repeating gives three. Both paths report no errors; all rows retain the same well/definition/MD/source.

**Why it matters:** Imports are not idempotent for supported aliases. Redundant picks inflate records, exports and displays and can interfere with later uniqueness-sensitive editing. This does not create a second definition and does not by itself prove an EUR or volumetric error.

**Realistic scenario:** A client reimports a vendor tops file using an old name after a canonical rename. Each repeat adds another copy of the same pick.

**Smallest safe fix:** Resolve the input top to its canonical identity before duplicate detection in each importer, including dynamic-top columns. Apply the current well/depth/source policy to that identity; retain genuinely distinct repeated crossings and provenance.

**Regression tests:** Actual bulk/mapped/dynamic-column imports using canonical and alias spellings, repeat import, mixed case/spacing, same MD and different sources, distinct MDs and reopen. Assert exact row counts and unchanged unrelated headers/locations.

### B52-04 — Deleting a migrated Correlation-only top is undone on project reopen

**Classification:** B. Material Pre-Release Defect / Risk. **Severity:** Medium. **Confidence:** High.

**Files / functions:** database.py:1509, 3172; correlationworkbench/store.py:330. _migrate_top_registry / delete_top_definition / top_styles.

**Confirmed behavior:** Each project open reads legacy correlation:tops entries marked added and recreates missing definitions. Deleting the global definition removes its picks/aliases but leaves that legacy creation intent in project metadata.

**Evidence:** top-ui-batch-evidence.json: actual manager deletion removes Corr-only before close; ProjectDatabase reopen recreates Corr-only. top-identity-evidence.json provides a minimal database reproduction.

**Why it matters:** An intentional delete does not persist for this supported legacy-project population. The recreated definition is empty; deleted picks are not recovered. This is not a request to add source-deletion UI.

**Realistic scenario:** An older project has a top created in Correlation. Its migrated global top is deleted, then returns after the next open.

**Smallest safe fix:** Make legacy creation backfill one-time or explicitly retire its creation metadata when the user deletes the canonical definition. Preserve unrelated Correlation styles and do not recreate deliberately deleted definitions.

**Regression tests:** Migrate an old Correlation-added top, delete through the manager, close and reopen twice; verify absence and preservation of all unrelated picks, definitions, aliases and module settings.

### B52-05 — An open Batch Calculations window cannot resolve a top renamed elsewhere

**Classification:** B. Material Pre-Release Defect / Risk. **Severity:** Medium. **Confidence:** High.

**Files / functions:** ogcore/batch_zones.py:541, 550; ogcore/batch_ui.py:630; database.py:3182. _top_pick / zone_boundaries / ZoneTab.read_definition.

**Confirmed behavior:** Persistent batch definitions are retargeted correctly, but an already-open tab retains its original top text. Calculation compares that text with fresh canonical pick names without resolving aliases.

**Evidence:** top-ui-batch-evidence.json: the live dialog calculates GROSS 80 ft / NET 20 ft before rename. After Haynesville → Haynesville New, its old name remains a valid project alias and the saved definition is correct, yet the live definition raises Skip: no Haynesville pick (zone top). Reloading the definition restores the same numerical results.

**Why it matters:** A normal cross-module rename interrupts a valid batch workflow until it is refreshed. No incorrect published numerical values were demonstrated in this reproduction.

**Realistic scenario:** Batch is left open while a top is renamed in the global manager, then the user runs the existing batch definition.

**Smallest safe fix:** Resolve zone boundary names against canonical project identities at the database-aware calculation entry and refresh held UI definitions when relevant top revisions change. Avoid changing geological boundary selection or formulas.

**Regression tests:** Open a batch tab, rename/merge a boundary in another connected window, run without reopening; test both top/base boundaries and a typed valid alias, preserving source selection and expected outputs.

### B52-06 — Protected-source enforcement misses embedded data ZIPs and nested archives

**Classification:** B. Material Pre-Release Defect / Risk. **Severity:** High. **Confidence:** High.

**Files / functions:** tools/release/check_protected.py:44, 80, 98, 116, 141. protected_in_path / zip_problems / archive_contents / executable_problems.

**Confirmed behavior:** The scanner extracts PYZ and CArchive type Z ZIP entries, but not ordinary type x data ZIP payloads. ZIP member names are checked without recursively inspecting contained archives. Package/name matching is case-sensitive.

**Evidence:** protection-matrix-evidence.json uses actual PyInstaller CArchive/PYZ writers: protected source inside a type x embedded ZIP passes customer and owner checks, as does a nested ZIP; OGCORE/FORMULAS.PY is missed. Positive controls catch all 27 tested suffix/depth variants, loose ZIP/egg/whl/PYZ, type Z, module/package/script entries, missing extensions and unreadable executables.

**Why it matters:** The release gate cannot substantiate its stated “no protected source in embedded ZIPs” guarantee. This is a verified checker gap, not evidence that the actual current package leaks source. Both actual Linux customer/owner builds passed the checker and independent source-oriented inventory. Fixture extension files are presence controls, not runnable binaries.

**Realistic scenario:** A dependency or data collection rule adds a ZIP as ordinary PyInstaller data or wraps one inside another archive; a release with protected content can be accepted.

**Smallest safe fix:** Inspect archive-like embedded data by content/name, recurse with bounded depth/size, and normalize relevant path spelling for the supported platform. Keep unreadable archive failures closed and retain clean-package positive controls.

**Regression tests:** Add real type x data ZIP, nested ZIP/PYZ, base_library.zip and Windows case variants to customer and owner negative fixtures; assert nonzero exit. Run the same checks on actual Windows artifacts.

## 4. Windows Validation Items

**C — Windows validation remains incomplete.** Linux build success is useful packaging evidence, not Windows qualification. After the listed fixes, perform the following on the exact candidate commit with the repository’s Windows constraints:

- Build all 15 extensions with matching x64 Python/Visual Studio Build Tools; verify `.pyd` load origins and rerun numerical/exception equivalence against pure Python in separate processes. Exercise DLL discovery with only Windows system directories on PATH.
- Run `Build_Windows_EXE.bat` and both actual specs in paths containing spaces. Verify all five customer executables, owner isolation, PDFium raster/PDF import, package-relative imports, fonts/icons, help and hidden scientific imports. Exercise clean-machine launch without Python installed.
- Run licensed packaged self-tests with a legitimately signed build-test license matching the embedded public key, then remove it and require exit 3. The local owner trust rejection was tested on Linux; a licensed customer frozen run was not tested because the owner's embedded-key build-test license was not available. Do not patch trust to manufacture a pass.
- Exercise Windows DPAPI/clock rollback/store behavior, Explorer drops, locked grid files, install/uninstall and writable per-user/project locations. Injected Linux PermissionError verifies fallback logic, not actual Windows file sharing.
- Check toolbar wrapping and font substitution at 100/125/150% DPI, including the 620px Seismic test case. Two actual assertions fail on this Linux/Tk stack; do not remove them simply to get green results.
- Build the final installer with `OGW_RELEASE=1`, supply the approved EULA, run final inventory/protection checks and signing checks. The trial stage explicitly allowed the existing EULA placeholder; it is not a production release approval.
- Attest the requested branch/commit in an actual checkout and rerun the two Git-tracking checks. Check shipped artifacts independently after hardening B52-06; the checks cannot replace final package inspection.

These are platform qualification items, not claims of demonstrated Windows defects.

## 5. Tk / Parallel Test-Harness Assessment

**Historical segmentation faults: unresolved.** The supplied request reports different Tk GUI tests crashing under parallel workers, but no original command, crash stack, OS/runtime tuple or core dump was supplied. This audit does not label those crashes harmless or definitively product-only/test-only.

The current full source run was serial. A separate full run used `-n 2 --dist loadfile --max-worker-restart=0` with faulthandler enabled and the same current source. Both finished with 2,700 passed / 4 ordinary assertion-or-Git failures / 19 skipped / 701 passing subtests. Neither reproduced a segmentation fault. The source run took 1,605.20 seconds of reported pytest time; parallel took 903.14 seconds. Separate X displays avoided cross-run focus interference. Parallel workers still shared their run’s X server, but not a Tcl interpreter or Python heap: xdist processes isolate those. This does not exclude native lifetime/threading faults inside a worker.

An initial parallel GUI cohort stopped at the existing toolbar assertion: 72 passed / 1 failed. A later 9-file GUI cohort completed 178 passed and 48 passing subtests, with the two known font/layout tests explicitly deselected. These cohorts overlap the full runs and are not additional unique tests. Tk emitted delayed `after` callback warnings in GUI testing; that is teardown evidence, not proof of the reported native crash’s cause.

Repository CI invokes pytest serially; the development requirements/configuration do not themselves enable xdist. Product background helpers generally separate work from UI application through queues/after callbacks; this inspection did not identify a reproducible worker-to-Tk crash. A clean audit run cannot clear a previously observed native crash.

**Release handling:** keep Tk-dependent qualification serial/process-isolated while the crash remains unclassified. Parallelize non-GUI tests separately. A dedicated GUI worker group only helps if it enforces one GUI workload per interpreter/display; it is not a demonstrated fix. Obtain the original native trace and exact command/runtime, reproduce with restart disabled and faulthandler, and determine whether a product action alone triggers it. Preserve failing evidence rather than treating isolated-file passes as resolution.

## 6. Cython Audit Result

**Module selection:** exactly the requested 15 modules, with no UI/plumbing additions: `ogcore.licensing`, `ogcore.license_runtime`, `ogcore.formulas`, `ogcore.multimineral`, `ogcore.multivariate`, `ogcore.core_equations`, `ogcore.water`, `petroworkbench.curve_ops`, `ogcore.pay`, `ogcore.batch_zones`, `ogcore.gridders`, `ogcore.gridding`, `ogcore.mincurv`, `ogcore.velocity_model`, `ogvol.engine`.

`tools/release/build_cython.py:44` compiles the existing Python sources under their existing module names. Directives retain Python language level, disable annotation typing, keep binding and keyword arguments; no C division optimization was introduced. All 15 built successfully with Linux gcc. Origin records show actual extension imports, not accidentally tested `.py` files. Public callable signatures matched in all 15 modules in the independent comparison.

**Semantic/scientific assessment:** 219 compiled reference tests passed, 1 Windows DPAPI test skipped, with 60 passing subtests. An independent cold-process source-versus-compiled comparison exercised 24 cases covering all 13 scientific modules plus a licensing internal-global lookup. Array values/NaN masks, relevant outputs, callable signatures and sampled exceptions matched. Cases include division, None/object-containing results, missing formula names, units, smoothing, pay support, batch zones, solvers, gridders, velocity and volumetrics. A patched licensing global was consumed from inside ClockState, beyond merely calling the patched attribute. No meaningful numerical/exception difference was observed in these cases; this is bounded evidence, not a proof for all possible inputs or Windows compilers.

**Protected-source enforcement:** substantially effective on tested ordinary paths and fail-closed unreadable archives, but not complete: B52-06 is a confirmed current gap. All 27 suffix/depth negative controls were caught; embedded data ZIP/nested/case variants were missed. All expected actual Linux compiled modules were present.

**PyInstaller assessment:** actual coordinated five-program customer spec and owner one-file spec built successfully. Their checks returned 0. Trial staging inventoried 1,635 files / approximately 521 MB, no WSD files, with no inventory failures after explicitly allowing the EULA placeholder. Third-party build-path string warnings were recorded. Owner tooling was kept outside the customer payload. No actual protected-source leak or shipped private key was found by the performed scans; the checker blind spots prevent treating this as a universal guarantee.

Remaining uncertainty is native Windows ABI/DLL collection, exact pinned dependency stack, clean-machine UI and licensed packaged runtime. The audit stack used Python 3.12.14, Cython 3.0.12, PyInstaller 6.22.3, NumPy 2.3.5 and Matplotlib 3.10.8 on Linux. See environment.json for full versions. These results do not certify the Windows build.

## 7. FM Tops Audit Result

The project has a useful canonical registry: definitions, aliases, per-well picks and separate provenance are real shared mechanisms, not just duplicated UI lists. SQL triggers also canonicalize raw name-based writes. Keep that architecture and the independent renderers.

Normal uncontested rename/merge, alias lookup, stratigraphic order and grid source propagation passed the current v0.9.51/v0.9.52 tests. Merge preserves pick rows and their MD/TVD/TVDSS/well/source/notes in tested paths. It intentionally can retain multiple picks/crossings; their mere existence is not a defect. Optional user-selected source retagging is an explicit workflow choice, not unconditional source preservation. No automatic fuzzy merge was demonstrated: likely-duplicate detection suggests candidates and merging is user-controlled on ordinary paths.

Canonical identity is nevertheless unsafe at alias collisions (A52-01). Cross-module behavior is incomplete for live batch definitions (B52-05), and importer canonicalization does not make duplicate checks canonical (B52-03). Creating a registry definition successfully is not sufficient evidence that every held window/reference refreshes correctly.

Persistence settings are retargeted across actual connected consumers, including Correlation/Petro/Cross Section/Map/batch references. The fresh manager probe also shows that a deleted Correlation-only definition resurrects through old metadata (B52-04). This prevents a clean migration/deletion approval.

Both structure and isopach grid source metadata update normally in the DB and grid.json; current tests assert unchanged values bytes, geometry, settings, display, control, notes and timestamps. An independent PermissionError injection blocked physical rewrites: the DB and loaded source stayed canonical before and after reopen, while the raw file retained the old alias. Grid content snapshots remained unchanged. **That documented fallback works and is not a finding.** The separate general grid publication race B52-02 is not a failure of that alias fallback.

The Global FM Tops Manager is under **Project → Global FM Tops Manager…** in the main Well Manager with a project open (`geoworkbench/main_window.py:321, 1750`). New/rename/merge/delete/order/aliases UI tests pass for ordinary cases, but actual GUI probes expose the collision and deletion defects above. Source removal is outside this requested audit and was not implemented. Project-connected consumers were traced where they actually read picks; no invented universal Seismic/Geosteering integration is required.

## 8. Data Integrity / Migration Result

**Not clean:** A52-01 and B52-02–04 affect identity, accepted state, duplicate records or deletion persistence. Do not alter project formats or clean existing client records speculatively; first fix and test the identified transitions.

Well Manager repeated header/location edits, false well_type conflict regression, genuine external conflicts, clearing coordinate pairs, correcting a bad location, corrected trigger migration and symbol persistence passed the focused current tests. Fresh project-switch probes exercised save/discard/cancel and recent-project routes with distinct project values. Stale header/IP/DST child editors refused writes to the other project; modeless production/directional windows were destroyed on switching, preserving the new project’s production and survey state. These are meaningful data assertions, not merely window-open checks.

Bulk/mapped header code updates only mapped nonempty values according to the selected policy; API ownership checks and location validation are shared. Current suite exercises imports and repeated location updates. The alias import duplication found through actual importer calls shows why those successes do not establish full idempotence. SQL raw-write canonicalization correctly reuses a definition while still permitting the duplicate picks in B52-03.

The top-registry migration adds aliases/order and canonicalizes supported old name-based picks; tests cover preserved pick fields and repeated open. However, the legacy Correlation backfill can recreate deliberately deleted definitions, so migration is not fully lifecycle-idempotent.

Independent grid crash-recovery probes preserved old values when interrupted before commit and recovered committed values after interruption. Same-name concurrent creation chose distinct paths without overwriting either grid. Those successes do not cover the active-reader race. Fresh numerical references matched vertical/quarter-circle minimum curvature, MD/TVD/TVDSS signs, sonic ft/m equivalence, seismic datum conversion and grid round-trip values. Pay/PHIH probes exercised independent curve axes, thin beds, exclusions and unit handling. Preview/discard preserved accepted full-series axes, units and external edits/deletions in tested scenarios. No new numerical formula defect was demonstrated by these checks.

## 9. Test Results

| Cohort | Result | Qualification |
|---|---|---|
| full | 4 failed, 2700 passed, 19 skipped, 2 warnings, 701 subtests passed in 1605.20s (0:26:45) | Serial source; entire collected suite |
| parallel_full | 4 failed, 2700 passed, 19 skipped, 4 warnings, 701 subtests passed in 903.14s (0:15:03) | Full source; two xdist workers; no native crash |
| targeted | 78 passed, 1 skipped, 1 warning, 48 subtests passed in 17.06s | Current v0.9.49–52, Petro API and licensing; serial |
| compiled | 219 passed, 1 skipped, 1 warning, 60 subtests passed in 110.13s (0:01:50) | Compiled scientific/licensing reference cohort |
| parallel_gui | 1 failed, 72 passed, 3 warnings in 93.87s (0:01:33) | Stopped at known toolbar failure |
| parallel_gui_extended | 178 passed, 3 warnings, 48 subtests passed in 119.71s (0:01:59) | Two font/layout tests explicitly deselected |

Cohorts overlap and must not be added into a unique pass total. Full suite exit status was 1, not a passing release gate. The user’s reported 2,718/4/1 outcome was not substituted for the actual current results.

The four full-suite failures were identical serially and in parallel:

- `test_owner_tools_build.OwnerToolBuild.test_the_owner_spec_is_in_the_source_package`: invokes Git tracking in an archive without .git; exit 128. This does not demonstrate a missing owner spec; the actual spec built successfully.
- `test_production_key.ProductionKey.test_no_private_key_material_in_the_repository`: Git ls-files fails for the same reason. Independent all-file filename/key-block scans found no private key material, but do not attest original Git tracking.
- `test_seismic_app.SeismicAppTests.test_grid_and_contours_are_separate`: surface toolbar has 2 rows rather than 1 at the tested width. This is a real current Linux layout assertion failure; Windows DPI/font behavior remains a validation item.
- `test_text_style.ControlTests.test_the_common_control_and_tk_fonts`: requested/expected bold resolves to normal on this Tk/font environment. Do not classify it as a segmentation fault or a geological defect.

The 19 full-suite skips comprise 11 missing real raster/log scan cases, 3 source-run compiled tests (separately exercised in the compiled cohort), Windows Explorer drop, Windows DPAPI, missing full Kingdom truth files, opt-in packaged PDF import, and the no-Git-history volumetric CSV comparison. The compiled cohort’s one skip is DPAPI. Missing proprietary-data and packaged Windows validation remain gaps. XML, complete failure traces and per-test skip reasons are bundled.

**Test-quality concerns:** `tests/test_v0951_fixes.py:99` imports a tops importer and checks its existence, then exercises the DB resolver; it does not actually prove bulk/mapped import idempotence. Fresh importer calls reproduced B52-03 despite those tests passing. Existing cross-module rename tests inspect refreshed/saved state and miss a held live Batch tab. Manager tests omit alias-owner collisions and deleted legacy top reopen. `tests/test_v0952_fixes.py` has useful byte/content assertions, but lacks the locked-file failure case and two-connection active publication interleaving; independent probes supplied both. `tests/test_cython_build.py:69` samples only part of the scientific selection, includes comparisons that can match exceptions rather than successful calculations, and its patched-attribute test is weaker than proving an internal global lookup. The separate all-module comparison improves evidence but should not be portrayed as exhaustive. Archive tests needed ordinary type x and nested payloads, not only top-level extension-name fixtures.

Test additions should target the six concrete transition failures, plus native Tk crash diagnosis and Windows package behavior. Avoid broad test rewrites or tests that merely assert source text. The inventory parsed all Python files without syntax errors; inventory breadth is not semantic proof.

## 10. Self-Test Results

Actual entry-point CLI tests used isolated license/settings stores. All five applications—Geo, Petro, Seismic, Geosteering and Correlation—returned the expected results:

| Runtime | All five applications | Interpretation |
|---|---|---|
| Source, unlicensed | exit 3 | License refusal exercised |
| Source, legitimate local owner test license | exit 0 | Licensed self-test bodies executed |
| Compiled copy, same legitimate test license | exit 0 | Extension-backed licensed runtime exercised |
| Actual frozen Linux customer, unlicensed | exit 3 | Packaged license gate exercised |
| Actual frozen Linux customer, local owner trust only | exit 3 | Embedded-key trust isolation preserved |

Actual frozen owner License Manager self-test returned 0 and exercised first-time test key/trust/license creation/import in a temporary owner folder. Both actual package protection checks returned 0. No private key or license was patched into application source or published. Test-only owner artifacts were kept outside the source/package/report.

Self-test bodies construct real windows and exercise application-specific runtime paths—project/data and render/import dependencies in Geo, Petro calculations/tracks, Seismic data/display, Geosteering interpretation and Correlation rendering—rather than returning 0 immediately after import. They are smoke tests, not coverage of every import/edit/save workflow. The independent geosteering window probe additionally executed its self-test body and manual fault dialog.

The actual frozen customer’s **licensed** self-test body was not executed: the locally generated owner key is deliberately rejected by the frozen customer, which trusts its embedded key. Its exit 3 must not be counted as a licensed pass. A signed Windows build-test license and packaged PDF check remain required. License signature/expiry/rollback tests passed in the source/compiled cohorts; DPAPI and native Windows storage remain unvalidated.

## 11. No-Action Observations

- Keep the independent Map/Petro/Correlation/Cross Section/Geosteering renderers. Shared canonical data is appropriate; visual implementation differences alone do not justify a release rewrite. No UI overhaul was performed or proposed.
- Automatic geosteering algorithms intentionally remain. Current commercial toolbar/menu/context/dialog gates hide automatic actions; regenerated help contains none of the removed action labels. In the actual fault-dialog probe, entered 7.5 produced exactly 7.5 throw and zero model.fit_fault calls with the commercial flag false. The direct automatic/interpretation self-test paths still work. Preserve both manual behavior and deliberately retained algorithms.
- All 29 native symbol catalog entries match the interoperability fixture metadata/order. No glyph drawing definitions changed relative to the historical comparison used only for geometry context. No runtime WSD catalog dependency or staged WSD file was found; the inventory explicitly rejects `.wsd` case-insensitively. Keep the test fixture for interoperability.
- The 5,002-well Petro tree probe filtered/restored stable row identities in approximately 0.122 seconds on this machine, with no switch_well calls during filtering and the active key unchanged. Duplicate API rows selected their own workspace keys. Standalone API lookup/search works, but the displayed row still says “[API MISSING]” because `petroworkbench/project_tree.py:322` uses only geo_api_uwi for its label. This is a confirmed contained display inconsistency (D), not data loss or a reason for a tree redesign; a later small fix should reuse _workspace_api for the label.
- Normal grid rename/merge and locked-file alias fallback preserve values. Ordinary staged-file crash recovery and distinct same-name file creation passed. Keep those protections when addressing the specific live-reader race.
- Formula evaluation uses a checked AST and an empty builtins namespace; the presence of eval alone was not reported as arbitrary code execution. No supplied source private-key block or developer private-key file was found. Approved licensing/public-key separation should remain intact.
- The existing EULA placeholder, absent real-data fixtures and missing Git history are recorded limits, not evidence to invent an application rewrite. Final production packaging must still enforce its existing release gate.

## 12. Final Recommendation

**Stop release due to blocker.** Fix A52-01 before using this candidate as a geological identity baseline for Windows release validation. Then address B52-02 grid publication ownership, B52-03 importer idempotence, B52-04 deletion migration, B52-05 live batch resolution and B52-06 package enforcement with narrow regression tests. Re-run the full serial suite and the separate compiled comparison after the targeted fixes.

Keep the reported Tk segmentation fault classified unresolved until native evidence explains it; current non-reproduction is useful but not closure. Then build the exact Windows candidate, run legitimate licensed/unlicensed packaged smoke tests and PDF/import/save/reopen workflows, and perform final installer/security inspection. No formula, renderer, UI architecture or project format redesign is warranted by this audit.

Only audit reports and curated evidence are published. All 904 application-source files remain unchanged.
