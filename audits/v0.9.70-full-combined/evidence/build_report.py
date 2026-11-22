from pathlib import Path
import json,collections
B=Path('/workspace/audit-v0.9.70-full');O=B/'deliverables';P=Path('/workspace/audit-v0.9.70-integrity/audit/v0.9.70_project_integrity');N='OandG_Workbench_v0.9.70_Full_Combined_Audit'
f=json.loads((O/'findings.json').read_text())
r=json.loads((B/'suite-summary.json').read_text())
intro=f'''# O&G Workbench v0.9.70 — Full Suite Audit and Consolidated Findings

**Independent read-only engineering audit · 22 November 2026**  
**Baseline:** `release/1.0`, commit `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`  
**Input:** OandG_Workbench_v0.9.70.zip  
**Disposition:** correctness and save/close defects remain; do not regard the current release as fully qualified for v1.0 or live multi-computer project sharing.

## Executive assessment

This is the expanded **whole-suite audit**, combined with the recent project-integrity findings. Scope includes architecture, geological/numerical correctness, state/cache behavior, persistence, project switching, imports/exports, performance/resource management, tests, security/distribution source, legacy code and suite UI infrastructure. It covers all major workbenches and shared services. It is not limited to persistence, and it does not propose a UI overhaul.

The consolidated register contains **17 entries: 2 Critical, 8 High, 4 Medium, 1 Low and 2 Cleanup**. Nine retain their PI-001–PI-009 identifiers from the recent audit; eight FA entries come from the expanded review. Cleanup entries and unsupported-deployment risks are explicitly distinguished from reproduced defects. They are not 17 equally dangerous application bugs.

The most urgent findings are still Seismic and Geosteering releasing unsaved work after a failed save. The wider review adds a failed-save close path in Raster Digitizer, an incorrect inverse TVD→MD conversion for undulating surveys, inconsistent TVD pay net/gross on those trajectories, and a LAS-run memory budget that does not count its retained arrays. A smaller production metric defect omits EUR per foot when the well has EUR/perforations but no monthly history. No geological formula or workflow was changed.

**Full-suite execution:** {r['passed']} passed, {r['failed']} failed, {r['skipped']} skipped, with {r['subtests_passed']} passed subtests across all **287 shipped test modules**. Four isolated test processes/displays were used, with no test modules deliberately excluded. This is whole-suite execution in partitions, not a serial-process or native-Windows qualification. The targeted 235-pass/one-failure persistence runs are retained as earlier evidence and are **not added** to this full-suite total. Independent numerical, cache, Digitizer, scale and map-parity probes are separate assertion-based experiments.

A 112,000-well synthetic metadata project loaded Map data in0.79 seconds and refreshed Geo's full well list in0.99 seconds here. The regular/Seismic map coordinate probes agreed in24 posting/path cases. These results support retaining the compact shared data store and geometry services. They do not certify a 112,000-well client project with38,000 LIC files, large rasters,200 layers and real SEG-Y volumes. The cache accounting defect is especially relevant to long sessions visiting many LAS runs.

The Galveston Island missing-work incident remains **unproven**: no desktop/laptop client files, matching sidecars, logs or Dropbox history were available or inspected. Older/incomplete/different copies, failed saves and conditional WAL omissions remain separate hypotheses. The audit does not assign fault to Dropbox or claim that all committed interpretations disappear on normal close.

All application code, tests, uploaded source ZIP and release material remain unchanged. No client project/account was accessed; experiments used temporary synthetic projects. No software fix, release or commit to the Workbench repository was produced. Audit-only publication to Software-reviews is separate from software changes, under the user’s standing instruction.

## Baseline and review coverage

The uploaded ZIP is11,987,621 bytes, SHA-256 `a1043496dc4fd868ce95817887fecbbb2e02a4012cca00834d70b6fbd85a6797`; CRC passed. All652 Python files matched the Git checkout after CRLF normalization. The Git tree has961 tracked files. Its Python inventory is358 non-test files /183,997 lines, and294 test/fixture files /87,184 lines. The non-test count includes release/tooling and owner-side code as well as the customer application. There are287 test modules and seven supporting test Python files.

Every Python file received AST/import/risk inventory. Targeted manual path review covered core entry points and calculations in77 files across all subsystems; subsystem tests and source scans covered the wider tree. This is a risk-based whole-codebase audit, **not a claim that every one of184,000 source lines was manually reviewed or that all branches executed**. The file-level ledger records this distinction. No line/branch coverage percentage was measured or invented.

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
'''
for x in f:intro+=f"| {x['id']} | {x['severity']} | {x['title']} |\n"
s=intro+'\n'
for x in f:
 s+=f"### {x['id']} — {x['title']}\n\n**Severity:** {x['severity']}. **Classification:** {x['kind']}. **Confidence:** {x['confidence']}.\n\n**Files/lines:** `{x['files']}`.\n\n**Function/class:** `{x['functions']}`.\n\n**Current behavior and why it matters.** {x['explanation']}\n\n**Realistic failure / reproduction.** {x['repro']}\n\n**Expected.** {x['expected']}\n\n**Observed.** {x['actual']}\n\n**Version comparison.** {x['v69']}\n\n**Recommended correction — not implemented.** {x['fix']}\n\n**Regression tests.** {x['regression']}\n\n**Data/recovery implications.** {x['recovery']}\n\n"
# Retain detailed persistence coverage without reusing the old executive/test count as this audit's outcome.
p=(P/'OandG_Workbench_v0.9.70_Project_Integrity_Audit.md').read_text()
s+=p[p.index('## Persistence and durability map'):p.index('## Galveston Island incident: hypotheses')]
s+='''## Whole-suite architecture and shared geological models

**The suite already has substantial shared infrastructure.** Keep that investment and the independent renderers. Wells/UID/API live in the shared database and ogcore.api; canonical FM definitions/aliases/picks are database services; curve identity/precedence/arrays use ogcore.curve_store and curve_aliases; accepted curves are distinct from previews; pay calculations are shared by Petro and batch; common depth/unit/repository/geometry services exist; Map uses compact column arrays and revision-domain invalidation; theme/icons provide common chrome.

The concrete architectural weakness is **inconsistent save outcome ownership**, demonstrated by PI-001/002/003/006/007 and FA-004. Each UI has its own dirty/autosave/close policy; some preserve state and some destroy it after errors. A small consistent success/failed/cancelled/discard contract and close coordinator is justified. Replacing frameworks, merging renderers or decomposing large modules for elegance is not justified by this evidence.

| Shared concept | Current authority / coupling | Assessment |
| --- | --- | --- |
| Wells / API / UWI | database well_uid/project-local id; ogcore.api.api14 and matching helpers; import-target guards | Full14-digit sidetrack/completion identity is preserved by the shared matcher; mapped spreadsheet reader normalizes integral numeric cells before matching. Production has a documented, ambiguity-checked short-API fallback. Do not unify these by truncating all APIs to10digits. Non-US identifiers need their supported path, not automatic API coercion. |
| Tops / aliases / sources / faults | Canonical definition IDs, aliases and source-normalized picks; per-module display state separate | Definitions/picks/styles are different things. Rename/merge retargeting and alias resolution exist, including map sources. A stale style name alone does not prove a pick survived deletion. Intentional global deletion is transactional; client LO/BMB/source contents were not available here. |
| Curves / units / sampling | Shared canonical samples/axes and origin precedence; per-view display models | This is a useful separation. Independent-axis statistics were corrected in v0.9.69. Actual sample-position compatibility is checked before multi-curve calculations. Preserve explicit resampling and raw percent/decimal semantics. FA-003 is a cache sizing failure, not a need for a new curve model. |
| Directional surveys / coordinates / depth | Shared well geometry and depth helpers; Geosteering has a minimum-curvature Trajectory plus explicit first-crossing inverse | Different interpolation/rendering contexts are legitimate, but FA-001 shows an actual inconsistent inverse. Fix the unsupported mathematical condition narrowly; do not merge all independent path/rendering implementations. |
| Horizons / faults / grids | Stable interpretation registry and per-survey picks; grid row/file publication and derived caches | Seismic has object conflict checks under its write lock and fixed deletion tombstones. DB/file publication is locally coordinated, not a distributed snapshot. PI-005 remains the relevant sync concern. |
| Selections / handoffs | ogcore.well_selection and handoff requests in project settings; UI polling | Shared selection is not a global synchronous save barrier. Destination-lock/frozen-target tests exist for imports/batch. A close request is not proof all modules saved successfully. |
| Paths / external assets | Project roles, relative paths and repository tokens; per-machine repository roots | Preserve deliberate external references and missing-source diagnostics. Make exact resolved paths/identity visible at handoff. A source folder and a client package are separate artifacts. |
| Colors / styles | Shared theme/icons/TextStyle plus renderer-specific plot styles | Namespace separation avoids opening one module changing another. Share chrome tokens later (FA-007); keep scientific color maps/styles and renderers independently configurable. |

The database and application controllers are large, but line count alone is not a finding. Lazy imports connect project/database/domain services; broad AST dependency edges include imports intentionally inside functions and do not prove an import-time circular failure. No new startup circular-import defect was established in this run. Targeted whole-object last-writer paths remain a maintenance/sharing risk, not evidence the app is broken for every single-user workflow.

## Numerical correctness: confirmed defects versus preserved contracts

FA-001 and FA-002 are material correctness findings with explicit reference values; do not dismiss them as presentation issues. For the undulating survey, the TVD1050 inverse has a unique true crossing atMD2750, yet the shared converter returnsMD2000/TVD900. For the pay interval, all-pay MD thickness2000 maps to endpoint grossTVD100 and reported netTVD275/N:G2.75. The correct handling of re-crossed beds needs a geological decision; silently clipping results would conceal the defect.

Other inspected contracts did not justify algorithm changes:

- Minimum curvature uses standard dogleg/ratio-factor geometry with clipped cosine and the zero-dogleg limit. Geosteering retains explicit path/frame/dip conventions and separate units. Negative-below-sea-level TVDSS is documented; velocity-model “TVD” below seismic datum is explicitly distinguished from well TVD below KB.
- Time/depth conversion uses TWT/2, explicit seconds/milliseconds and ft/metres factors. Isopach checks domains and brings depth references/units together; it does not claim true stratigraphic thickness without dip. Do not add a dip correction under the guise of cleanup.
- Pay cells clip midpoint support to zone boundaries and reuse weights for net/averages on supported trajectories. Percent/decimal values and cutoffs are explicit, not inferred from magnitude. Raw petrophysical outputs are intentionally not automatically clamped.
- Formula evaluation has an AST allowlist, restricted NumPy numeric functions and empty builtins. Seeing eval in a scan is not proof of arbitrary code execution. The multi-curve engine checks actual depth positions, including origins, rather than only sample intervals.
- Multimineral inversion includes closure, measurement uncertainty and rank/ambiguity QC; multivariate fitting distinguishes sample masks and target transforms. Tests provide useful synthetic reference coverage. They are not proof a chosen endpoint set/model is geologically appropriate for every client's formation.
- Production BOE, gas/liquid conversion, GOR and water-cut references matched the independent simple control:100bbl oil +600Mcf gas yields200BOE, GOR6000scf/bbl and water-cut1/3 for50bbl water. FA-005 concerns an omitted metadata metric, not these arithmetic formulas.
- Volume calculations separate geometry mode, physical units, fractions and positive FVF validation. This audit did not find evidence warranting changes to the established7758 oil volumetric coefficient or the documented area/datum conventions.

Tests used synthetic fixtures for the new numerical probes. Existing suites also use bundled real raster/navigation examples; no client's mature production history, interpreted survey or geological calibration dataset was supplied. No field-data accuracy certification is claimed.

## Performance, scalability, memory and resource assessment

### Measured checks

The independent scale probe created112,000 synthetic wells/locations, without LAS/raster/seismic payloads. On this Linux machine while other test processes competed for CPU: seed1.23s; Map store load0.787s; refresh one changed well0.161s (returned only well1); Seismic well loading0.600s; Geo project load including list1.270s; subsequent full list refresh0.985s. Peak process RSS was380,192KiB. These are one-run diagnostic measurements, not SLAs or an end-user Windows benchmark. No thresholds were encoded to bless all large projects.

The shared map data store and batch Tcl tree insertion avoid the previous per-well object/query/insert cost. Revision domains distinguish DATA, POPULATION and STYLE changes. Those are concrete reasons to leave working architecture alone. Initial full lists and whole-project metadata can still be substantial; do not add redraw/reload optimizations without measuring the actual problematic workflow.

FA-003 is independently confirmed: eight decoded LAS runs account for512bytes in a256MiB cache while retaining3.84MB of NumPy arrays. An individual current oversized entry is intentionally allowed by BudgetCache; **that is not this defect**. The defect is measuring every LasFile as64bytes and having no item cap. A long session visiting thousands of runs can grow far beyond the budget.

Other caches have useful limits: curve-array entries are sized as tuples of arrays; Correlation/XSection have curve budgets and capped raster readers; SEG-Y uses memory mapping and bounded section caching; v0.9.69 adds bounded per-map horizon surfaces; disk cache has a byte limit and dependency stamps. Do not report all caches as unbounded because one object type is undercounted. Repeated project/window lifecycle tests provide evidence for specific owners, not proof no allocation can grow in a day-long Windows session.

### Remaining scale/resource gaps

No test here loads38,000 actual LIC files,200 large shapefile layers, multiple full-size SEG-Y volumes, or every LAS run from the client's112K-well project. Large rasters and derived surfaces are separate from well metadata. Native memory-mapped Windows file handles, multi-volume bandwidth, Tk DPI/font behavior, long sessions and simultaneous asset synchronization remain qualification work. No actual orphaned Matplotlib artist accumulation was proven from the idle_draw diagnostic alone; ownership tracing is needed before calling it a leak.

## Import/export and data-integrity review

The checked pathways distinguish durable project data, imported external sources, previews and regenerated display products. Bulk/mapped headers use logical transactions, while LAS parsing/publication is deliberately per-file after successful header import; a bad LAS does not imply good headers should roll back. Raster LIC import reports per-file failures/skips and avoids guessing ambiguous well matches. Production reports duplicates and explicit units; same-source rows are updated according to the selected policy. Multi-source production selection is a documented derivation rule, not a request to merge/delete FM pick sources.

API/UWI text matching, ambiguity checks, filename/destination collision handling, staged digitized output, paired grid/file publication, malformed input tests and cancelled imports all appear in the shipped suite. Workbook export chunks well IDs, splits Excel row limits, uses atomic replacement and forces leading-equals strings to text. This is positive evidence; do not flag its use of openpyxl as inherently unsafe or claim every export format has identical safeguards.

Project Save As uses SQLite backup and path rewriting/checks, including appended shapefile sources fixed in v0.9.69. This is stronger than copying an active main DB. It is not an atomic cloud transfer of every asset. PI-004/005/008 address incomplete targets/snapshots and forensic side effects, while PI-006 and FA-004 identify drafts discarded after failed writes. No client recovery, reimport, migration or conflict resolution was attempted.

## Error handling and UI state

AST inventory found461 broad Exception/BaseException handlers in non-test code and77 whose AST body is only pass. These are triage counts, not461 defects. Harmless examples include optional cache writes (recompute on miss), callbacks for an already-destroyed widget and diagnostics that must not fail a user operation. Dangerous cases are those that release unique editable state or claim success without durable storage; those were reproduced and have individual findings.

The critical distinction is whether the live state remains retryable after an error. Petro's failed-detach default-No behavior is a good existing model. A console/log/status message that disappears when the window is destroyed is inadequate for unique unsaved interpretation. The fix should preserve state and offer retry/explicit discard without adding approval dialogs to every successful autosave.

Do not treat a status update, a refreshed tree, a DB mtime or a clean shutdown message as proof that every writer saved. Conversely, a hang after polygon Finish can occur after commit. Inspect preserved payloads before concluding either loss or success.

## Tests: strengths, gaps and failures

The full run executed every shipped test module; numerical, database, import/export, selection, cache, renderer, licensing and release checks are represented. Meaningful examples include two independent database sessions with object/payload checksums, foreign-key/integrity checks, failed-commit rollback, staged publication ownership, own-axis curve tests, underlying stored values after reopen and repeated window disposal checks. These are stronger than a startup-only smoke test.

The new independent probes still found defects despite thousands of passing tests. The suite lacks the specific invariants demonstrated by FA-001/002 (inverse round-trip and all-pay N:G on undulating paths), FA-003 (LasFile retained bytes), FA-004 (node-store failure vetoes close), and FA-005 (EUR/ft without months). The recent PI failures likewise show that happy-path persistence and a mocked dirty Cancel test do not cover every real Exit/switch route.

Static/source-inspection tests for launchers/manifests/protected modules are useful distribution guardrails, but cannot establish GUI behavior, numerical correctness or native package completeness. They must supplement, not replace, executable tests. Test-only license trust is isolated; it does not verify the customer EXE's embedded trust.

Three unique full-suite failures were observed: the Drawings manager non-settling at scaling1.25 (PI-009), Correlation box width6.296937 versus6.300000 (FA-006), and Tk family urw gothic l versus expected avant garde gothic (FA-006). These were also investigated with isolated repeats. The precise Correlation width difference and font alias behavior need platform-aware diagnosis; they are not counted as new geological data corruption. Native Windows/DPAPI, a slow package build, compiled-extension checks, Explorer drops and unavailable full native Kingdom input explain skips, as listed in the evidence document.

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
'''
(O/(N+'.md')).write_text(s)
print('Wrote consolidated main report',len(s),'characters')
