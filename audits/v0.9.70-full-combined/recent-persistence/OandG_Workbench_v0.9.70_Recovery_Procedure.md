# v0.9.70 — Copy-first recovery assessment procedure

**Status:** proposed procedure, not executed on client data. No recovery or app changes were made.  
**Baseline:** `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa` · 22 November 2026.

The goal is to identify the newest complete interpretation without destroying competing evidence. Client Dropbox/account/local-drive access needs separate explicit authorization. Steps involving those sources are for the owner or an authorized recovery operator. This document does not grant that access.

## 1. Preserve the present state before changing anything

1. Stop editing or opening further project copies. Do not resolve conflicts, rename/delete databases or sidecars, reimport interpretations, repair/migrate/vacuum/checkpoint, or replace the laptop file with the desktop file. Do not advance versions during triage.
2. If either application is still running with missing or unsaved work visible, record screenshots, active project/survey/source names, exact paths shown, status/error messages, version and time. Do not force-kill or blindly close it: this audit reproduced close-after-failed-save data loss. Obtain qualified help to preserve a filesystem/VM snapshot and any memory-only work. Do not attempt an untested in-place save as the preservation step.
3. Preserve an OS/filesystem snapshot when available. A raw multi-file copy of a live changing SQLite project is not a consistent snapshot, even if copied twice. If a stable capture cannot be obtained, label it live/possibly inconsistent and retain additional captures; do not present it as authoritative. Do not pause/resume or reconfigure the user's Dropbox account without authorization.
4. Use a new evidence directory outside every synced project, with distinct desktop/laptop/capture identifiers. Preserve originals and an untouched evidence master. Never reuse a destination or overwrite an earlier capture. All subsequent SQLite or Workbench work uses another disposable working copy.

## 2. Capture the entire evidence set

Capture these from both computers and every candidate alternate/conflicted/versioned folder. Preserve names, relative paths, sizes and timestamps, plus SHA-256 hashes of captured files. Record computer, capture time/timezone, capture method and whether writers were running.

- Every `.ogwproject` manifest, all `.ogwdb` files and **matching `-wal`, `-shm`, `-journal` files**. Include sidecars even if tiny/old/zero length. Do not rename them or mix a WAL from one capture with another database.
- Entire project-owned folder tree: DB, LIC, Well Lists, Color Bars, Control Points, Grids, Shapes (all `.shp/.shx/.dbf/.prj` companions), Map Images, Digitized, Templates, Reports, Exports, Backup, Cache and any customized role folders. Cache can contain diagnostic/derived work; do not delete it during forensics.
- All standalone `.ogsteer`, Petro workspace/template files, external interpretation exports/imports, SEG-Y/2D assets, LAS/raster images and registration/control files relevant to the missing objects. Where large assets cannot be duplicated immediately, preserve a path/size/hash inventory and record what is absent.
- Application error logs and settings describing recent projects and per-machine repository roots. Record data-root mappings without exposing credentials or unrelated personal data. A manifest can point to an absolute DB outside its folder; preserve that resolved target too when authorized.
- Existing backups and exports; a folder named Backup is not evidence a backup exists or is current. Capture actual file inventory.

Hashing/copying raw files is not SQLite opening. It may still require access/authorization and can race a running writer. Cloud-only placeholders are not complete captured contents; record availability and obtain authorized offline copies without altering originals. Keep original names in evidence masters.

## 3. Obtain independent historical candidates only with authorization

Ask the owner to preserve Dropbox version-history downloads and conflicted copies into **new separate directories**, never “restore” over the current project during investigation. Note provider version IDs, paths and displayed timestamps/timezones. Include candidate manifests/assets and same-generation sidecars if available; a database version alone may not include its WAL.

Also inventory alternate project locations, recent-path targets, local backups and unsynced desktop copies. Do not assume the visibly newest filename or mtime contains the newest interpretation. A layout/open/footprint write can update the DB while pick payloads remain older.

## 4. Work only on new disposable copies

For each candidate, make a working copy from its immutable evidence master, preserving database/sidecar basenames and folder structure. Mark it clearly as disposable and keep an acquisition hash manifest separately. Verify copied hashes before opening anything.

**Do not point Workbench, ProjectDatabase, ProjectDatabase.reader, or Recovery Access at an evidence master or original.** Normal Workbench open can create/migrate/normalize a DB. `mode=ro` is insufficient for zero-touch forensics: the audit created a `-shm` sidecar through Recovery Access on a writable WAL directory. `immutable=1` is not a universal alternative; a main-only immutable view can miss committed WAL content.

On a disposable working copy, SQLite's ordinary recovery may roll back a hot journal or read/checkpoint committed WAL. That modifies the working copy and is permitted only there. Preserve before/after hashes and logs. Do not manually concatenate/apply WAL bytes, delete journals or run “repair” against an uncertain generation.

Use version-matched SQLite tooling/Workbench Recovery Access **on the working copy** to inspect a recovered consistent view. Recovery Access's fallback makes another private copy and checks it; its export uses SQLite backup. If it reports an uncertain/moving/inconsistent source, retain the error and stop interpreting that candidate. Do not bypass the warning to obtain rows that may mix committed/uncommitted pages.

## 5. Compare content and identities, not only file timestamps

On each working copy, record:

- Manifest name, exact original/resolved DB path, database schema (`user_version`), actual `journal_mode`, SQLite version and integrity_check result after working-copy recovery. Integrity_check=ok proves structural consistency, not business completeness or newest generation.
- Wells/project-local IDs, survey/line IDs, names, external paths and geometry fingerprints; active selections/source/visibility settings separately. The same survey name on another DB is not sufficient identity.
- Every row in `seismic_horizons`, `seismic_faults`, `seismic_interpretations`, `seismic_2d_picks`, `map_drawings`, survey display/maps/layout stores and relevant project_meta records. Include counts, names, IDs, payload hashes, finite horizon-pick counts, fault-point counts and polygon vertices/style/visibility.
- Relevant `geosteer_jobs`, `xsection_items`, Correlation session/styles, canonical tops/picks/sources and Petro curve/interval data if the missing work includes them. Compare real values at known interpreted positions from screenshots, not just total row counts.
- External asset existence/hash, role-relative path resolution and per-machine `@repository` mappings. Check all saved surveys/lines and hidden/inactive objects before declaring deletion. Match SEG-Y fingerprints; do not relink to a different geometry merely to make a view open.

A missing grid can be regenerated only after preserving the input controls/interpretation; regeneration is not a recovery substitute. An interpretation existing in DB but hidden due to active survey/source/visibility should be diagnosed without deleting/reimporting it.

## 6. Interpret outcomes conservatively

| Observation | Assessment |
| --- | --- |
| Desktop has the new committed picks; laptop has an older valid snapshot | Preserve both; likely handoff/path/generation issue. Determine transfer/version history before choosing a recovery target. |
| New picks appear only after recovering a matching WAL on a working copy | Committed data was outside the main file in that capture. Preserve the entire original evidence set and produce a separate consistent export. |
| Different manifest target/repository/survey explains visibility | Record the exact binding mismatch. Correct only a new test/recovery copy after approval; do not rewrite originals. |
| A hot rollback journal restores the prior committed state | Uncommitted newer rows are not durable; don't interpret raw uncommitted pages as a valid project. Specialist analysis may still be needed. |
| Only an older backup/version contains needed objects | Preserve all candidates and plan an explicit object-aware recovery into a new project, with reconciliation of IDs and dependencies. Do not merge binary SQLite files. |
| Edits never reached SQLite and the process has exited | Database/WAL recovery may be impossible for those edits. Check authorized external exports, recordings or session evidence; do not promise recovery. |
| No client evidence yet | Root cause and recoverability remain unknown. This audit is in that category. |

## 7. Recovery output and approval boundary

Create a **new named recovery project** using a verified committed snapshot/export from a working copy. Keep the originals/evidence masters intact. Validate counts/payloads, coordinate/units/source bindings, required external assets and representative displays after fresh application restart. Compare critical objects with both originals and known interpretation examples. Record what was recovered, omitted and unresolved.

Do not replace the active client project, upload a recovered file over Dropbox, resolve conflicts, merge interpretations or resume alternating computers until the owner approves a concrete validated recovery result. None of those actions was attempted here.
