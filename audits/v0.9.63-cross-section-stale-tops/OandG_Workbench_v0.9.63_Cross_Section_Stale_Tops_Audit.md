# O&G Workbench v0.9.63 — Cross Section stale formation tops

19 November 2026 · Read-only targeted audit · No implementation

## Conclusion

**Confirmed: Cross Section treats saved top styles as live top definitions.** Global FM Tops Manager deletion removes the definition, its aliases and its linked picks, but leaves Cross Section's in-memory and saved Section.tops entries. The Tops dialog copies those entries and only adds current global names; Display Manager independently lists Section.tops without checking current definitions. Refreshing picks does not prune the styles. Autosave and reopen preserve them.

This explains how physically deleting the named tops through Global FM Tops Manager can still leave the screenshot's rows under All Sources, even when **LO and BMB are the only current sources**. An external synthetic reproduction invoked the actual manager delete method for all twelve example names. Definitions, aliases and old-source picks disappeared; only LO/BMB remained; all twelve names remained in both UI data paths and returned after save/reopen. After refreshing picks, those names stopped rendering. The two lists share a stale state input but have separate unguarded consumer paths.

The user screenshot establishes the visible rows and All Sources selection. No client project database was supplied, so the audit does not claim to have examined that project's stored section JSON or independently enumerated its actual source rows. The same failure chain is independently confirmed in the final source without relying on client data.

## Baseline and integrity

- Repository: https://github.com/kwgeologist/O-G-WorkBench; branch release/1.0.
- Branch HEAD fetched at audit start: **42d8e330cc6013c73cedd1ca4f2cf4bae1cadc01**, the requested 42d8e33. No newer commit was present at that point. Exact detached checkout used throughout.
- Supplied ZIP: OandG_Workbench_v0.9.63.zip, **11,824,837 bytes**; SHA-256 **0582c6ddb8aa81f4ca88df52ac68aa8365daf931ddd038791ef5461faba28b58**. ZIP CRC passed.
- Eight directly relevant source files match the ZIP after CRLF normalization: database.py; geoworkbench/interpretation_dialogs.py; xsection/window.py, dialogs.py, model.py, store.py, render.py and layout.py.
- All **940 tracked source files remain unchanged**. Checkout clean. Only audit deliverables and external probes were written; temporary synthetic databases were used. No application code, client project or release artifact was changed.

All file references below refer to this exact commit. Tests ran on Linux source, not the Windows customer executable.

## Authoritative list and binding map

**Canonical definitions:** database.py:334 defines top_definitions; :3049 top_definitions() queries it with pick statistics; :3075 formation_names() returns only its current definition names, including valid definitions with no picks. It does not union stale section names or aliases into the list. Global Manager fill() uses top_definitions() at geoworkbench/interpretation_dialogs.py:138.

- **Tops dialog:** xsection/window.py:2482 passes current db.formation_names(). However, xsection/dialogs.py:351 first deep-copies every section.tops style and :352 marks every copied name as kept. Lines 354–362 append missing current names; nothing intersects existing styles with the canonical set. listed() at :481 admits everything under All Sources. _ok() at :591 copies kept styles back to the section, including deleted names. Therefore a correct current API is supplied, but is used additively instead of authoritatively.
- **Display Manager → Tops:** xsection/window.py:641–643 uses len(section.tops) and lists each style directly. It does not call formation_names(), query picks, inspect aliases or check definition membership. Rebuilding the tree does not fix its input.
- **Section rendering:** Store._read_picks at xsection/store.py:205 obtains formation_tops_for() rows, cached on each XWell.tops. database.py:3381 selects formation_tops by well/source, not the global definition table. Render._well_markers at xsection/render.py:820 requires an actual cached pick plus a matching style. Correlation lines use layout.top_groups() at xsection/layout.py:260, also derived from cached picks, then render.py:1046 uses the style. A leftover style alone does not manufacture a pick or a rendered top.
- **Saved state/layout:** Section.to_dict/from_dict at xsection/model.py:721–731 serialize/restore every style without a database membership check. Store.sections/save_section at xsection/store.py:424–428 round-trip these through xsection_items via database.py:3678–3695. Window autosave at :2617 saves both the named section and Last section state; _last_section at :2631 and open_section at :2652 restore it. _section_like at :185 copies styles into sections on other wells. These paths preserve stale styles, their ordering, colors, visibility and source assignments; they do not recreate global definitions by themselves.

## Deletion propagation

Actual UI path: geoworkbench/interpretation_dialogs.py:249 TopDefinitionsDialog.delete confirms deletion, calls db.delete_top_definition for each chosen definition and then changed(). database.py:3288 executes in a transaction: DELETE formation_tops WHERE definition_id=?, DELETE top_aliases WHERE definition_id=?, DELETE top_definitions WHERE id=?. This is an explicit application deletion, not an assumption that SQL cascades will remove picks.

- Definition: removed.
- Aliases belonging to that definition: removed.
- Picks from every source linked to that definition: removed.
- Well Manager UI: changed() at geoworkbench/interpretation_dialogs.py:80 refills the manager and refreshes Geo tabs.
- Cross Section cached picks: focus-return detects changed top revisions at window.py:120–130; refresh_science at :132 reloads picks or forgets well data and rebuilds. This normally removes rendered picks after returning to the section. There is no direct top-style deletion subscription.
- Cross Section styles, dialog entries and manager entries: not pruned. _add_top_styles at window.py:222 adds styles for observed well picks but never removes a style. rebuild at :1394 calls that additive method. Thus even a fully refreshed section still has stale top-list entries.
- Named sections, Last section state, saved datum and interval-fill name references: not cleaned by delete_top_definition. The rename/merge path has _retarget_top_references at database.py:3297 onward, including saved sections around :3363, but deletion has no corresponding reconciliation. Name references can remain without restoring picks or definitions.

## Findings

### XS-01 — Saved styles bypass canonical top membership in both lists

**Severity: Medium. Classification: confirmed operational/persistence defect. Confidence: High.** Files/functions: xsection/dialogs.py:351, :481, :591; xsection/window.py:222, :641, :2482; model.py:727; store.py:424; database.py:3288.

Current behavior: old styles are retained, current definitions are appended, all-source listing accepts all styles, Display Manager lists the raw section styles, and save/reopen restores them. Deletion of the data itself succeeds.

Failure scenario: open a section while ASTN, 605ASTN, ASTNB, 605ASTNB, CRCSL, 602CRCSL, BUDA, 602BUDA, GRGN, 602GRGN, FRWR and 602FRWR exist. Save it. Physically delete those definitions in Global Manager. Return to Cross Section and open Tops under All Sources: every old style is still available and shown as enabled. Even after picks refresh, accepting the dialog and reopening the section retains the names. A section on different wells can inherit them through _section_like.

Source filtering is not an authority check. listed() caches distinct current pick names for a chosen source, but also accepts any style whose saved source matches that selection. Thus assigning an obsolete style to LO can make it appear under LO even with no LO pick or valid definition. The external probe confirms this branch. Under All Sources no query or cache is needed at all, matching the screenshot's blank Source cells.

Recommended fix: add a small Cross Section reconciliation boundary using current canonical definition names/IDs. Preserve style/order for surviving definitions; remove absent names from active section styles before list assembly and after dialog Apply/OK, including stale snapshots. Reuse the boundary for both consumers and load/rebuild/save entry points. Do not filter valid definitions merely because the current wells or chosen source have no picks. Handle an existing alias only by resolving to a current canonical definition, never listing an absent alias as an independent top. No change to geological calculations or renderer consolidation is warranted.

Regression tests: exercise actual global deletion against a named and last section; assert absent names in Tops/Display Manager after refresh, dialog accept, reopen and _section_like; preserve surviving colors/order and valid unpicked definitions; repeat with only LO/BMB sources, All Sources, and a stale explicit LO source tag. Test a dialog snapshot opened before deletion so accepting it cannot reintroduce a removed style.

### XS-02 — Pending local pick-target names escape global membership checks

**Severity: Medium, conditional secondary path. Classification: confirmed code path; not established as the screenshot's cause. Confidence: High for the path.** Files/functions: xsection/window.py:974–1009 _target_chosen/_fill_targets; database.py:3014 top_definition and :3413 set_formation_top.

Current behavior: New top stores a local draft in _new_tops before any canonical definition/pick exists. _fill_targets removes a draft only while its name currently exists globally, then appends the remaining drafts to the canonical list. If a name remains in that queue, was picked into existence, and is globally deleted before a target-list rebuild removes the draft, the next rebuild can offer it again. Picking it can deliberately write a new pick and therefore create a definition through the normal write API. This requires the draft lifecycle, not ordinary old saved styles; it is not automatic database resurrection on reopen.

External evidence: with the global definition absent and _new_tops containing ASTN, the real _fill_targets still offers ASTN. The audit does not claim the user's window followed this particular lifecycle.

Recommended fix: distinguish a never-created explicit draft from a name known to have been deleted; reconcile the draft queue after creation/deletion. Under the requested strict binding rule, register an explicitly created new definition before offering it as a project top, while preserving the intended New top workflow. Require explicit user recreation rather than silently treating a deleted name as a valid project target.

Regression tests: New top → first pick → global delete before target refresh → focus/rebuild must not offer the deleted target; an explicit later New top action may recreate it as a current definition. Do not remove unrelated valid local work or alter picking depths/sources.

## Sources: LO and BMB

Tops dialog source options come from db.interpretation_sources('tops') at dialogs.py:369. database.py:2901 reads distinct nonblank current formation_tops.source values and also includes the active source. It does not obtain the dropdown's source codes from saved styles or from aliases. Accordingly, an extra active source can remain an option even without picks; a persistent source dropdown snapshots its options at construction. These possibilities should be inspected in a client database before claiming a removed source is still stored. No such extra source is visible in the supplied screenshot.

The screenshot's Source column is a per-style source constraint, not the provenance of every top. Its em dash means the style has no specific source assignment. Numeric prefixes such as 602/605 are name text here, not proof of current source rows. In the reproduction, interpretation_sources('tops') returns exactly BMB and LO while the twelve old names still appear. Therefore restricting or merging source names does not fix XS-01, and no source deletion or merge was performed in this audit.

## Resurrection checks and rendering limits

- **Aliases:** deleted definition aliases are explicitly removed. Normal formation_names() does not list aliases. They are unnecessary for the reproduced ghost rows. Rename/merge aliases may resolve old spellings to a surviving top, a distinct workflow.
- **Old Cross Section layouts / project-tree state:** saved TopStyle objects are sufficient. Display Manager reconstructs rows from them, not from a separate authoritative project tree. Last section, named sections and copied settings perpetuate the same stale input.
- **Cached lists/source filters:** XWell.tops can render deleted picks until refreshed. The Agg renderer reproduction confirms this conditional unrefreshed case, then confirms no deleted top marks after refresh. Do not infer persistent rendered picks solely from stale Tops rows. The source-specific _source_tops cache does not explain All Sources; its saved-style alternative can admit deleted names even with a fresh cache.
- **Remaining picks / fallback:** normal manager deletion removed all linked picks in the synthetic test. _add_top_styles rebuilds from cached well picks but is additive, not a DB definition creator. top_style() creates a local style, not a project definition. A new explicit set_formation_top write can create a definition; simply opening the dialog or saved section does not.
- **Legacy migration:** database.py:1522 handles correlation:tops entries marked added, creates legitimate canonical definitions once and removes that marker. A separate legacy interpretation migration at :1561 initializes definitions from picks only before its migration flag is set. Normal deletion after migration is not replayed from Cross Section JSON. The existing DeletedMigratedTops regression passed; the synthetic project also reopened with all twelve definitions still absent. No migration-driven recreation was found in this normal sequence.

## Validation and coverage

- Existing focused suite: **54 passed, 31 skipped**, 15.34 seconds: tests/test_v0951_fixes.py, tests/test_v0962_xsection.py and tests/test_xsection.py. GUI-dependent cases skipped because no Tk display is available. This was not a Windows UI run.
- Legacy migration regression: **1 passed**, 0.43 seconds (see exact elapsed time in migration-test.log/XML).
- Independent synthetic stale-top probe: **completed, exit 0**, confirming the defect, successful data deletion, LO/BMB-only sources, renderer refresh distinction, dialog/manager retention and save/reopen persistence. This is a reproduction confirmation, not an assertion that intended binding passes.

Probe methodology: actual ProjectDatabase, Global Manager delete method, Store, model, renderer, _list_manager, _fill_targets and TopsDialog._ok were executed. Confirmation and UI refresh were stubbed for the manager. With no Tk display, the exact non-widget constructor state-assembly AST was executed unchanged before first widget access; manager tree writes used collection sinks. This verifies list inputs and selection logic, not physical widget painting. Rendering used Matplotlib Agg against actual synthetic well data.

The passing suite does not cover this deletion-to-both-lists-to-reopen contract. Add the specific regressions above before changing code. GUI tests are still needed for focus return, modal lifetime, dropdown refresh and visual disappearance after a real manager deletion.

Exact source test command, cwd the verified checkout: PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python -m pytest -q -p no:cacheprovider tests/test_v0951_fixes.py tests/test_v0962_xsection.py tests/test_xsection.py --tb=short -rs --junitxml=/workspace/audit-v0.9.63-stale-tops/focused-results.xml.

Migration command: MPLCONFIGDIR=/tmp/stale-tops-mpl XDG_CACHE_HOME=/tmp/stale-tops-cache PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python -m pytest -q -p no:cacheprovider tests/test_v0953_fixes.py::DeletedMigratedTops::test_migrate_delete_and_reopen_twice --junitxml=/workspace/audit-v0.9.63-stale-tops/migration-results.xml.

Probe command: MPLCONFIGDIR=/tmp/stale-tops-mpl XDG_CACHE_HOME=/tmp/stale-tops-cache PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python /workspace/audit-v0.9.63-stale-tops/probes/stale_tops.py.

## Recommended fix order

1. Lock down the deletion contract with temporary-project regressions for both lists and save/reopen, including LO/BMB-only sources and unpicked valid definitions.
2. Reconcile Cross Section top styles against current global definitions at load/refresh and list/dialog boundaries; keep surviving styles and order. Revalidate on dialog accept and save to stop stale snapshots perpetuating rows.
3. Reconcile pending draft targets and source-specific saved assignments against the same authority. Do not use source filtering as a substitute for definition membership.
4. Verify real UI deletion/return/reopen, then validate rendering with refreshed picks and missing datum/fill references. Avoid broad database cleanup or renderer changes; inspect actual project state read-only if its symptoms differ from the reproduced path.

## Additional requested curve-visibility observation

Both editors already support per-curve visibility without removing the curve. Cross Section Log Display Options has **Scale → Hide this log (kept selected, not drawn)** at xsection/log_display.py:272; _scale_edited at :985 updates curve.shown at :998. The top-level Hide Curves control at :1657 intentionally sets every selected curve's visibility. Correlation's editor has **Scale → Disabled (kept in the template, not drawn)** at correlationworkbench/template_editor.py:221 and updates the selected curve's visible property at :623.

An eye beside each selected curve is a reasonable discoverability enhancement, not evidence that individual visibility storage is absent. A future eye should toggle the existing shown/visible field, preserve scale/style/track/fills and use the same icon in both applications. This was static code inspection only, not a separate Windows UI validation. No eye control was implemented during the read-only audit.

**No fix was implemented.** The confirmed failure is stale Cross Section presentation/persistence after successful global deletion, not evidence that the Global Manager failed to delete those definitions or that removed sources need merging again.
