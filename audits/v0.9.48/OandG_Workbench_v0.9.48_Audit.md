# O&G Workbench v0.9.48 — Pre-Release Audit

## 1. Executive Result

**Clean except for listed material risks.** No Cython-induced numerical discrepancy, lost project compatibility, or licensing-enforcement regression was demonstrated. Four material items below need correction or an explicit scope decision. Windows validation remains incomplete.

Read-only delta audit dated 16 November 2026, using v0.9.45 as the accepted baseline. The supplied v0.9.48 ZIP is authoritative: SHA-256 `143b7fa20a6b7d63ac2249527c275931beced67e15d9c5389a107424ed16a977`. It contains 899 files. The requested `release/1.0` / `194c11f` provenance cannot be independently attested because the archive has no Git metadata. Comparisons found 27 changed files, seven additions and one removal against the supplied v0.9.45 tree. All 15 protected modules' Python sources are byte-identical to that baseline.

**Integrity:** all 899 supplied files remain byte-for-byte unchanged, with zero additions or removals. Compilation, generated documentation, probes and synthetic projects were confined to external audit folders. No application code was edited.

## 2. Release Blockers

**None found.** The current Linux-built payload did not contain the protected Python modules or the Petra fixture. Verification gaps below are material risks, rather than evidence of an actual source leak. No Windows artifact was executed.

## 3. Material Pre-Release Defects / Risks

### B48-01 — Protected-source gate misses nested and non-PYZ copies

**Category B; confirmed verification defect; confidence High.** Files: `tools/release/check_protected.py:28–35,39–62`; `tools/release/inventory.py:64–75,106`; `Build_Windows_EXE.bat:31,73–86`.

**Current behavior / exact defect:** `check()` matches source only at the exact package-relative parent path and inspects Python modules only in each of the five declared executables' PYZ archives. It omits loose `.pyc`, non-PYZ CArchive entries, and the separately built owner executable. Presence of any matching `.so` or `.pyd` is accepted without import/ABI validation.

**Evidence:** Real PyInstaller archive-writer fixtures show that a missing extension, direct `.py/.pyx/.c/.cpp`, and a protected PYZ module are rejected. Conversely, `_internal/backup/ogcore/formulas.py`, `.pyx`, `.c` and `.cpp` pass **both** protection and inventory checks. Loose `_internal/ogcore/formulas.pyc`, a raw CArchive Python-module entry, and source embedded as CArchive data pass the protection check. These fixtures deliberately use placeholder extension files to test the gate; they are not executable product builds. A separate actual product build passed protection and the actual owner archive contained compiled licensing, not licensing Python bytecode.

**Impact / scenario:** An accidental backup, generated-source folder, or archive-layout change can ship proprietary code while the gate prints “none as source or bytecode.” No such leak was found in the actual build examined.

**Smallest safe correction:** Recognize protected package-path suffixes below arbitrary packaging prefixes; reject loose bytecode and inspect relevant CArchive module/data entries as well as PYZ. Add a one-file owner-artifact check for its applicable protected modules. Require platform-appropriate extensions and verify actual import origins in a packaged diagnostic, without a license bypass. Do not broaden the 15-module compilation scope.

**Regression tests:** Keep passing genuine artifacts as positive controls; inject every negative case above, including each customer executable and the owner package. Require every leak to fail. Evidence: `protection-negative-evidence.json`, `customer-protected-check.log`, `owner-archive-evidence.json`.

### B48-02 — API search and sorting ignore standalone Petro APIs

**Category B; confirmed feature defect; confidence High.** Files/functions: `petroworkbench/project_tree.py:290–310`, `ProjectTreeMixin._build_project_tree`; `petroworkbench/workspace.py:70–82`, `_default_workspace`.

**Current behavior / exact defect:** Sorting and searchable row metadata read only `state['geo_api_uwi']`. Standalone LAS workspaces store their existing API as `state['api']` and `WellData.api`.

**Evidence:** A normal `_default_workspace()` created from a synthetic well with API `42401123450000` retained that API in state. Its tree row nevertheless displayed `[API MISSING]`; searching `4240112345` returned zero wells. No curves were loaded by the filter.

**Impact / scenario:** A user opens LAS wells in standalone Petro, then cannot find them using the newly supplied API search. Their API ordering also remains insertion order because every sort key is “missing.” The old tree's limited label handling does not establish that the new search works for standalone projects. No wrong-well load was demonstrated.

**Smallest safe correction:** Use the same resolved stored API for display, sorting and filtering: prefer the integrated project's authoritative API when applicable, otherwise the standalone state's API. Read existing metadata without loading unloaded wells or calculating curves.

**Regression tests:** Load standalone LAS/Petro workspaces with populated `api` and no `geo_api_uwi`; verify display, numeric order, formatted/10-/14-digit and partial searches, clear/rebuild, duplicate APIs, and actual selected well identity. Retain the integrated tests. Evidence: `petro-independent-evidence.json`.

### B48-03 — Manual fault acceptance still performs constrained automatic fitting

**Category B; confirmed call path, requirements risk; confidence High for behavior / Medium for intended boundary.** Files/functions: `geosteering/app.py:1526–1536,1557–1567`; `geosteering/job.py:998–1018`, `Steering.insert_fault/refit_fault`; `geosteering/model.py:1016–1023`, `fit_fault`.

**Current behavior / exact issue:** Setting `AUTOMATIC_STEERING_UI=False` removes the explicit automatic controls and dialog's opening fit. Accepting the manual fault dialog still calls `Steering.insert_fault()` or `refit_fault()`, which call the fitter. In the default `both` mode, a typed throw fixes its magnitude but the optimizer still slides the adjacent segment endpoints against the log.

**Evidence:** With the flag false, the real manual insertion callback submitted throw `7.5` and mode `both`. It called `model.fit_fault` and obtained shifts approximately `left=-9.8`, `right=-2.3`; their difference correctly remained `7.5`. The new regression checks the throw difference, not whether fitting ran.

**Impact / scenario:** If “no normal UI access to automatic fault fitting” includes automatic geometry adjustment, the manual dialog still exposes that behavior indirectly. This is **not** a newly changed scientific method or a demonstrated wrong throw: the underlying fitting behavior is unchanged from v0.9.45 and may be intentional manual-placement semantics.

**Smallest safe correction:** Resolve that specific boundary before editing. If constrained placement is permitted, state that exception explicitly. If all automatic fault fitting must be unavailable, route flag-false manual acceptance through the agreed existing manual geometry operations; retain the fitter and flag-true behavior. Do not silently change the geological workflow merely to satisfy a call-count test.

**Regression tests:** Verify typed throws **and endpoint/dip geometry** for insertion/edit, both placement modes and insufficient-log cases; test whether the fitter is permitted or forbidden under the chosen contract. Retain direct automatic algorithm tests and flag-true controls. Evidence: `geosteering-independent-evidence.json`.

### B48-04 — Renamed Petra fixture is not prohibited by the payload gate

**Category B; confirmed verification gap; confidence High.** Files: `release/manifest.json:134–169`; `tools/release/inventory.py:64–75,84–107`; `tests/test_v0948_fixes.py`, `BuiltInCatalogue.test_the_release_ships_no_wsd`.

**Current behavior / exact defect:** The forbidden filename remains `well symbols.WSD`; the file now exists as `tests/fixtures/petra_well_symbols.WSD`. The new test injects the former filename. Inventory also considers `_internal/tests` unowned and treats its fixture directory as a third-party warning.

**Evidence:** With all required payload resources present, `_internal/well symbols.WSD` fails inventory. The actual fixture bytes copied as `_internal/petra_well_symbols.WSD` pass without warning; `_internal/tests/fixtures/petra_well_symbols.WSD` passes with warnings only. The actual current manifest/spec excludes the test package, and the staged real build contained **zero WSD files**.

**Impact / scenario:** Accidentally collecting the moved fixture can pass staging despite the requirement that the commercial payload never ship the Petra catalog. This is a gate weakness, not a current demonstrated distribution leak.

**Smallest safe correction:** Explicitly prohibit the fixture's actual basename throughout the commercial payload and test that name; preserve customer Import/Export WSD functionality. A blanket ban on user interchange files is unnecessary.

**Regression tests:** Inject the actual renamed fixture at root/internal/nested locations and require release refusal; verify the normal payload stages successfully and WSD interchange remains functional. Evidence: `wsd-payload-evidence.json`.

## 4. Windows Validation Items

- Build all 15 `.pyd` modules with the supported CPython/MSVC architecture. Record the interpreter actually selected by `py -3`, compiler, exact pinned packages and extension import origins; this Linux run used GCC, CPython 3.12.14 and Cython 3.0.12, not the complete Windows constraint stack.
- Run the actual batch/spec pipeline on Windows, including all five executables, the separate one-file owner tool, PDFium DLL/version resources and dependency discovery with the restricted PATH. Exercise spaces in build/install paths and a clean target machine's VC runtime, Tcl/Tk, NumPy and cryptography dependencies.
- Run licensed frozen self-tests with a legitimately trusted build-test license, then missing/expired/wrong-module and local-owner-trust rejection checks. The Linux customer launch checks reached the real rejection gate; licensed customer-body execution remains unverified.
- Run compiled scientific/reference and equivalence tests on Windows rather than relying on the separate source-only CI test job. Verify the final staged/installed artifacts with the strengthened protection checks and production release settings.

These are unverified platform behaviors, not proof that the Windows build fails. No specific inevitable Windows `.pyd` naming or compiler-configuration failure was established from the reviewed code.

## 5. No-Action Observations

- Exactly the intended 15 modules are compiled; UI renderers, orchestration and other persistence modules were not swept into Cython. Their source calculations were not rewritten. Do not expand or merge modules for this release.
- All 29 catalog records, their order and all five metadata fields match the original v0.9.45 WSD. The moved fixture is byte-identical. Symbol geometry/rendering definitions are unchanged; only `load_wsd()` and removal of runtime `_find_wsd()` differ among the symbol function/class definitions. Explicit WSD import/export, stored codes/numbers, exact-code handling and the existing DH-to-DRY fallback remain intact in the exercised tests.
- Integrated Petro filtering detaches/moves existing rows, preserves their key mapping and active key, and does not load curves or run calculations. A 5,002-well fixture narrowed and restored in 0.13 seconds on this host; tied APIs selected their distinct expected keys. An independently generated Ctrl+F key event focused the search, with no global `bind_all` shortcut. This is a synthetic responsiveness check, not a full client-project benchmark.
- The explicit automatic-geosteering toolbar, menus and context entries are guarded; fault dialogs have no Fit control/opening fit when disabled. Flag true restored the toolbar. Automatic algorithms, dialogs and handlers remain present; direct auto-steering still produced segments. Manual numerical code, units, reports and exports were not rewritten. B48-03 qualifies the internal manual-fault call path.
- Licensing's post-baseline change isolates each Gate test's `LOCALAPPDATA` and clock store. Runtime licensing sources are unchanged; current-date and rollback tests passed in source and compiled targeted runs. Local owner trust remained rejected by frozen customer programs.
- The checked-in HTML guide still says 0.9.25 and advertises old controls, but the supported batch regenerates it before packaging. Independently regenerated HTML says 0.9.48 and has none of the removed action labels; current Assistant catalog/workflow/menu indexes were updated. The older Geosteering README is internal and not an allowlisted commercial help resource. No runtime WSD read was found. Historical release records are not current manifest dependencies.
- The Linux staging trial used `--allow-placeholders`: its existing EULA placeholder is **not** commercial legal approval. Production `OGW_RELEASE=1` checks remain required; this accepted-baseline issue is not presented as a new v0.9.48 regression.

## 6. Cython Audit Result

**Module selection: correct.** The module list is exactly the requested 15 and all loaded from actual built extensions under their normal import names.

**Python semantics: supported by inspection and exercised comparisons.** `annotation_typing=False`, `binding=True`, `always_allow_keywords=True`, language level 3; no enabled `cdivision`, disabled bounds checking or explicit unsafe numerical directives. Docstring removal is intentional. Public callable signatures matched across all 15 modules. An internal `ClockState()` call observed a patched `state_path`, unlike the shipped test's weaker check of the patched attribute itself. This is bounded evidence, not a proof of every possible Python input.

**Scientific equivalence: no discrepancy observed.** Independent Python and compiled processes used separate source roots. Twenty-four representative cases covered every one of the 13 scientific modules, including a real batch-zone calculation, mineral inversion, regression/clustering, pay support/summaries, smoothing, gridding/minimum curvature, velocity/depth conversion and volumetric integration. Serialized array dtype/shape/bytes, floating results and expected exception outcomes matched; valid formula helper execution was included. The broader compiled reference suite also passed. No meaningful numerical change was demonstrated.

**Protection: current artifacts passed; gate incomplete.** The actual Linux customer package contained all 15 extensions and no protected PYZ modules; the one-file owner archive contained compiled licensing and no licensing Python module. Negative tests establish B48-01/B48-04, so the gate's blanket assurance is too strong.

**PyInstaller: Linux integration built successfully using both supplied specs.** The coordinated five-program package, collision check and owner one-file build completed. Staging copied 1,632 files, with zero inventory failures and zero WSD files; placeholder/third-party warnings are recorded. The owner workflow self-test passed after making this custom cloud interpreter's Tcl/Tk libraries discoverable at build time. Initial cloud-only failures were missing `clang` and `libtcl9tk9.0.so`; GCC and proper build-library discovery resolved them. Customer rejection runs required the corresponding external library path, so they are not claimed as clean-machine standalone acceptance.

**Windows: still unvalidated.** Linux `.so` builds and rejection checks do not certify Windows `.pyd`, DLL collection, installed behavior or licensed frozen scientific execution. The complete pinned Windows dependency environment was not reproduced here.

## 7. v0.9.46–v0.9.48 Regression Result

**Yes, evidence of post-baseline defects/risks was found:** standalone API search/sort is incomplete, and the new protection/renamed-fixture assertions miss demonstrated negative cases. The manual-fault boundary needs the explicit interpretation in B48-03; its computation itself is unchanged.

No observed Cython numerical or signature regression, catalog metadata/geometry regression, project-format change or weakened licensing enforcement was found. Current controls support hiding the explicit automatic actions while retaining functional algorithms. This delta audit does not reopen the accepted baseline's unrelated known issues.

## 8. Test Results

The complete source suite collected **2,687 tests**, exactly the total implied by the brief's 2,683 passed + four skipped. It completed in one process with a real Tk display; no crash or fallback run occurred. **It did not pass completely.**

| Run | Passed | Failed | Skipped | Passing subtests | Seconds |
| --- | --- | --- | --- | --- | --- |
| Full authoritative source suite | 2664 | 4 | 19 | 684 | 1883.99 |
| Targeted source changes/release tests | 149 | 0 | 5 | 75 | 172.64 |
| Compiled scientific/licensing reference suite | 219 | 0 | 1 | 60 | 156.71 |
| Compiled Petro/new-UI integration | 88 | 0 | 0 | 60 | 299.51 |

These are separate, overlapping cohorts; do not add them as unique test totals. The four full-run failures are:

- `tests/test_owner_tools_build.py:39`, `test_the_owner_spec_is_in_the_source_package`: `git ls-files --error-unmatch` exits 128 because the supplied ZIP is not a Git checkout. The spec exists and built successfully.
- `tests/test_production_key.py:90`, `test_no_private_key_material_in_the_repository`: its mandatory `git ls-files` command likewise exits 128. This failure does not establish that a private key was found.
- `tests/test_seismic_app.py:1905,1976`, `test_grid_and_contours_are_separate`: a toolbar-width assertion sees two rows instead of one on this host.
- `tests/test_text_style.py:154`, `test_the_common_control_and_tk_fonts`: Tk reports normal instead of bold. The independent font query confirms requested DejaVu Serif is unavailable to this X server; Tk substitutes normal-weight `fixed` despite Matplotlib listing the family.

All four test identities/messages also occurred in the accepted v0.9.45 audit; relevant tests and UI implementation files are unchanged. The prior date-dependent Gate failure is absent. The two Git failures have confirmed archive-context causes; the two GUI failures remain host/font/layout qualifications and must be checked in the intended Windows environment. They are not erased or described as passing.

**Nineteen skips:** 12 unavailable real-raster/log/Kingdom reference fixtures; three compiled-only checks intentionally skipped in the unchanged source tree (all three ran in the compiled cohort); two Windows-only checks (Explorer drops and DPAPI); one opt-in frozen PDF integration test; one volumetrics historical-CSV comparison requiring Git history. Thus the brief's four-skip expectation differs by 15 explained fixture/platform/history skips. Exact names/reasons are in `skipped-tests.json`. Relative to v0.9.45, collection increased by 24 tests and three compiled-only skips; the licensing Gate fix removed its previous failure.

**Launcher self-tests:** Geo, Seismic, Petro and Geosteering, plus Correlation, each returned **0** both in the ordinary source tree and in the copy with all 15 modules compiled. These used the existing License Manager's isolated first-time owner workflow, which generated and imported a legitimate local test license through supported code; no enforcement or shipped keys were patched. All five source launchers returned **3** with an empty license folder. All five actual Linux customer executables returned **3** both without a license and when offered source-only local owner trust. Licensed **frozen customer** self-test bodies were not run because no shipped-key build-test license was supplied.

**Self-test meaning:** Geo exercises database/CRS, Map, gridding, raster/autoregistration, digitizing, Cross Section and PDF rendering; Seismic writes/imports SEG-Y and draws section/map data; Petro draws tracks and checks raster/autoregistration resources; Geosteering directly auto-steers, asserts segments, exports PDF and saves/reopens a job. They provide useful smoke coverage, not complete scientific equivalence. The frozen owner tool's actual GUI setup/sign/import self-test passed after resolving custom cloud-library discovery; its initial Tcl/Tk failure is retained in the evidence rather than suppressed.


**Test quality:** Petro's new fixtures populate `geo_api_uwi`, so they miss standalone `api` storage. The Ctrl+F test calls the handler after generating the event, masking an event-binding failure; the independent event-only probe passed. `test_cython_build.py` compares four source modules, not every scientific module; its core identifier assertion is truthiness only, and formula helper names are absent from the evaluation namespace, so the helper-expression case compares refusals rather than successful helper calculations. Its monkeypatch test calls the patched function directly, not an internal consumer. The independent probes corrected those coverage gaps for this audit. Ordinary CI does not compile before its pytest job; the new compiled tests consequently skip there. No negative-case coverage for `check_protected.py` was found. The WSD packaging test injects the old filename; the fault test verifies the chosen throw but not absence of constrained fitting. Correct these targeted coverage weaknesses rather than claiming the passing counts certify release behavior.

## 9. Recommendation

**Fix identified items first.** Strengthen protected-artifact and renamed-fixture release gates, correct standalone Petro API resolution, and settle the constrained-manual-fitting boundary without altering accepted geology silently. Add focused regressions, then proceed to the actual Windows build and clean-machine validation. No broad refactor, UI redesign, renderer merge, scientific rewrite or Cython-scope expansion is warranted.
