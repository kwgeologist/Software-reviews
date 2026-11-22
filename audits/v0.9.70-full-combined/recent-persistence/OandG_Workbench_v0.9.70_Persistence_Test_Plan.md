# v0.9.70 — Persistence regression and qualification plan

**Proposed tests, not application changes.** Baseline `1e0867f`, 22 November 2026. Current executed results are in Audit_Evidence.md; rows below describe required additions/qualification, not tests already passed.

## Common test contract

Use only disposable synthetic projects, explicit project identities and seeded geological values. Run both DELETE/FULL and explicitly inherited WAL. Isolate app settings, licenses/test trust, caches, roots and repository mappings. Never use a client project or customer executable trust override. Use real storage APIs/UI events where appropriate; a mock returning True is not persistence evidence.

Every success case must inspect committed rows/files from an independent connection **and a new interpreter/application process** after save/close. Compare payloads (depth/time values, finite samples, units, IDs, source/provenance, vertex coordinates/styles) rather than only existence or counts. A row-count-only assertion can pass despite overwrites. Track original hashes and sidecars around each experiment. Inject failures in transient objects/filesystems of test processes only; retain stderr/callback exceptions and enforce timeouts.

## Required per-module save/close/restart matrix

For each row: create → edit → apply/Finish → save → close module → close project → launch a new application process → reopen → inspect raw committed payload and reconstructed state. Repeat in a normal folder and a complete copied “synced” folder with an explicit snapshot boundary.

| Module/data | Representative payload and assertions |
| --- | --- |
| Geo / Well Manager | Dirty header/location/trajectory/manual rows; 14-digit APIs/source identifiers; test tab Save, Save Project, Close Project, window X, menu Exit, load another project. Save writes expected fields, Cancel retains exact draft, failure retains DB and UI. |
| Global FM Manager | Definition + aliases + picks across two sources; rename/delete intentionally and verify shared views refresh/restart consistently. Preserve surviving definitions/sources; no alias-induced resurrection. Intentional global deletion is a different operation from sync loss. |
| Seismic 3D | Horizon with finite/NaN grid, multi-piece fault, styles/visibility, two surveys. Save/close/restart verifies blobs and values; switch survey/project while dirty; partial loads never delete absent objects. |
| Seismic 2D / ties | Multi-line pick identity and positions, ties, active interpretation, layout/maps. New process checks every line and survey mapping and units; missing source SEG-Y must not remove stored interpretation. |
| Regular Map / Seismic Map | New/edit polygon/fault polygon/contour/line, layers and visibility, vertex/style/dip data. Verify successful Finish committed **before** refresh; failed Finish preserves draft/original. Unfinished Cancel remains explicit nondurable behavior. |
| Petro | Accepted canonical curve and its own sampling grid, zones/facies/pay/intervals, preview exclusions and multiple loaded wells. Compare actual arrays/units after restart; preview/discard never publishes. Failed detach default No retains all dirty work. |
| Correlation | Shared top/fault picks and independent session/track layout, source/style/spacing. Close failure cannot silently release state; precommitted picks survive independently. |
| Cross Section | Named and Last section, local correlation/fault/fill JSON, tracks/templates/view plus shared top picks. Inject failure on the second named/Last write; require atomicity and retained draft. |
| Geosteering | Job segments/dips/faults/targets, lateral/type IDs, zone track, project vs standalone file. Pending autosave and already-failed autosave followed by close/new/open/lateral switch must honor dirty state. |
| Grids / surfaces / control points | Edited controls, file payload/hash, project revision ownership and display style. Interrupt during staged file/DB publication; no mixed accepted state. Preserve prior valid grid on failure. |
| Raster / digitizer / LAS | Raster source/LIC transforms and picks; accepted digitized LAS + metadata and source files. Interrupt file publication; previous asset and DB relation stay consistent. |
| Production / batch / pay | Daily/monthly accepted data, calculated curves/attributes and zone/pay outputs; freeze destinations during selection changes and compare units/numerical values. Cancel/failure must not partially publish a logical operation. |

The present audit ran targeted normal/failure UI cases and a fresh-interpreter **storage** reopen for representative payloads; it did not complete this entire per-module OS-process UI matrix.

## Highest-priority failure regressions

| Test | Trigger | Required outcome |
| --- | --- | --- |
| T01 / PI-001 | Seismic save raises disk-full/I/O/locked error; close/switch/WM exit | Same live interpretation remains; failure is actionable; no destruction or ownership release. Retry then new-process values match. |
| T02 / PI-001 | Another local connection edits same horizon/fault; choose Cancel during close | Cancel means no close and no overwrite. Reload/Overwrite retain existing documented conflict semantics. |
| T03 / PI-002 | Geosteering pending autosave fails; repeat with timer already cleared by earlier failure | dirty remains, close/switch vetoed, no implicit discard just because job has a path/project. Cover segments as well as name. |
| T04 / PI-003 | Geo dirty header + Save Project; dirty main tab + Exit/WM close | Truthful all-saved status only after real save; Save/Discard/Cancel/failure handled uniformly. |
| T05 / PI-006 | Polygon save/destination dialog/file publication fails | Original and draft vertices retained; retry writes once, undo history changes only after commit. |
| T06 / PI-007 | Correlation session / XSection autosave failure and second-write failure | Visible retained unsaved state; no close; named and Last section consistent. Map line-setting failure likewise clearly reported. |
| T07 / PI-004 | Existing manifest transferred before DB; DB directory exists | No DB/sidecar created. Clear resolved-path/missing target message. New Project still creates intentionally. |
| T08 / transaction boundary | Fail midway through helper nesting / commit / import | No partial logical operation; previous data retained, connection usable, correct error propagated. Preserve current passing nested-transaction tests. |

Use genuine temporary filesystem lock/read-only/disk-quota failures in addition to targeted exception injection where safely feasible. A mocked save failure verifies caller handling, not Windows filesystem behavior.

## Snapshot, crash and synchronization matrix

Repeat A–E with main-only, full stable folder, database+WAL, missing SHM, delayed journal, split DB/asset version, incomplete manifest, cloud-only placeholder and destination previously opened. Provider-selection simulations are not live Dropbox verification.

1. **A:** commit, keep connection idle/open and copy main. DELETE expected current committed values; WAL main-only can be stale and must not be presented as a complete snapshot.
2. **B:** save and close **all** owners/connections, produce a consistent snapshot and compare target payload/hash. Verify actual checkpoint completion rather than assuming any one closed window is sufficient.
3. **C:** abrupt exit before autosave, during uncommitted DELETE writes, after WAL commit and before checkpoint, and during file publication. Distinguish never-committed changes from recoverable committed WAL. Test recovery only on working copies.
4. **D:** two genuinely independent replicas, two local connections and two workbench processes. Confirm local conflict handling separately from lack of distributed serialization. Stale marker/foreign-host/offline lock tests cannot certify distributed exclusion.
5. **E:** retain a newer DB, select older/conflicted copy into a new destination, and test generation/completeness acceptance. No test may overwrite a user DB to simulate this.
6. Verify snapshot handoff includes asset inventory and manifest path/identity checks. SQLite backup consistency is insufficient for an asset concurrently rewritten outside SQLite.
7. Recovery no-touch test: originals main/WAL/SHM/journal directory entries and hashes identical before/after; include WAL/no-SHM/writable-directory case that current tests miss. No original SQLite open in forensic mode.

## Tk and v0.9.70 interaction tests

- Run shipped `test_v0970_tk_lifecycle.py` on native Windows and Linux at 100–200% display scaling. Retain bounded event drains and trace Configure/scrollbar/hint changes at failing 1.25 scaling.
- Run Finish through real Enter/button handlers, verify committed polygon from another connection before refresh and before closing the manager. Confirm no duplicate handlers after repeated open/close.
- Close with pending interpretation save, tree-scroll, well filter, redraw, poll and Drawings manager. Only nonpersistent UI callbacks may be cancelled before the relevant save outcome is resolved.
- Run 50 open/edit/save/close/restart cycles with callback-exception logging, bounded memory/artist/handle counts and repeated project switching. A “no TclError” test alone does not prove durability.

## Windows/package and release gate

Use the exact release executable and packaged extensions in a disposable Windows environment with synthetic projects. Record EXE/package/module hashes, platform/Tk/SQLite versions and exact commands. No packaged run occurred in this Linux audit. Verify full fresh-process workflows and filesystem locking/crash behavior; do not infer them from Linux source tests or source-only pytest passes.

Release gate: all P0/P1 regressions pass, no unacknowledged failed save can close/discard work, Open Existing never creates an absent DB, a documented single-writer snapshot workflow passes completeness checks, and native Windows Tk/close tests pass. Concurrent multi-computer editing remains unsupported until a real coordination design is separately implemented and verified. No UI redesign, renderer merging or formula changes are needed for these tests.
