# Recommended fixes — v0.9.72 audit only

No fixes were implemented. Keep the original finding IDs and pair each correction with the concrete failing diagnostic, not just the shipped nominal test. Do not combine unrelated rewrites with the corrective release.

## Priority and sequencing

Resolve the native stability gate, data-integrity boundaries and numerical defect first; LIC protection precedes import UX/reporting cleanup. Windows qualification follows the exact rebuilt artifact. The Full Audit gives the practical sequence.

## Corrections and regression risks

### TK-01 (Critical) — Intermittent Tk SIGSEGV remains an open release-stability gate

Capture the native fault and correct the demonstrated owner/thread lifecycle path. Preserve traces and test order. Do not label the issue fixed merely because this audit run or a targeted run passes.

Regression risks and required controls: Windows impact and frozen executable behavior are unverified; do not presume a Linux Tcl panic is the same SIGSEGV.

### FA-002 (High) — Shallow TVD reversals still escape the N/A pay convention

Check actual MD-ordered survey segments and use an appropriate absolute tolerance against cumulative reversal, not an allowance multiplied by grid resolution. Preserve the agreed N/A convention.

Regression risks and required controls: Nearly horizontal wells, unit scaling, plateaus, sparse/irregular stations, and conventional-well results need independent reference tests; do not introduce MD substitution.

### FA72-001 (High) — Overwrite No does not protect an imported project-owned LIC

Detect input/output path identity and stage/skip project-LIC synchronization or require explicit consent/backup. Enforce input preservation across every writer, not only rewrite_lic_image.

Regression risks and required controls: Project LIC paths, same-file aliases, automatic synchronization, permission failures and imported calibration must retain existing behavior.

### FA72-003 (High) — Geo Save As copies before pending form edits are saved

Resolve/save pending editors before taking the copy and honor failures/Cancel. Copy a coherent accepted application state, not a pre-prompt DB snapshot.

Regression risks and required controls: Do not create/open an unintended partial copy after cancellation or save failure; test header, tab and child-editor edits and original/copy identities.

### PI-005 (High) — A failed close-generation write silently leaves stale-copy protection ineffective

Treat generation/handoff failure as an explicit incomplete close/publication outcome. Ensure a changed project cannot retain a matching old verification record, and require retry or a clear unverified state.

Regression risks and required controls: Multi-module connections on one PC, busy timeout, WAL checkpoint failure, concurrent close and crash recovery; preserve committed data and explicit Open Anyway semantics.

### TK-02 (High) — Destroyed Geo roots remain strongly owned by traces and selection subscriptions

Own each trace/subscription token and provide idempotent disposal for supported destruction paths. Do not blanket-delete all variable traces in production.

Regression risks and required controls: Normal close versus raw destroy, worker lifetime and fixture teardown; no proof this causes original SIGSEGV or leaks client processes after they exit.

### TK-03 (High) — Petro search trace retains destroyed application roots

Retain/remove the search trace token in owner disposal and exercise all termination paths.

Regression risks and required controls: Do not lose search/filter state or infer Windows customer memory leakage from a raw-destroy test alone.

### TK-04 (High) — Wrong-thread finalization remains a demonstrated native Tcl failure class

Release Tk-containing graphs deterministically on their owner thread; keep the existing fixture guard as mitigation, not closure.

Regression risks and required controls: No global GC disabling; do not substitute this controlled panic for original SIGSEGV reproduction. The v0.9.72 application trigger remains unproved.

### FA72-002 (Medium) — Generated LICs lose Petra GROUP identity and fail same-name section round trips

Preserve the stored GROUP metadata in project LIC output; ensure exact identity is not lost behind an ambiguous fallback.

Regression risks and required controls: Older registrations without lic_section, renamed logs, multiple sections with identical labels and moved images.

### FA72-006 (Medium) — LIC Cancel is checked only between 1,000-file write batches

Check cancellation at each safe per-file boundary inside the batch; commit only completed items consistently and count remaining work. Distinguish database waits from parsing and UI refresh.

Regression risks and required controls: Do not abort an active file halfway, lose completed imports, rewrite LICs for rolled-back items, or misreport skipped versus cancelled records.

### FA72-007 (Medium) — First-N-month production includes adjustments before first production

Constrain the first-N window to 0 <= month_offset < N while leaving actual cumulative history unchanged.

Regression risks and required controls: Reported zeros, pre-production adjustments, gaps, source priority and incomplete histories; do not discard legitimate corrections globally.

### FA72-010 (Medium) — Petro successful-save reporting hides stale published zone results

Propagate/record partial-publication status, retain a reliable retry and show stale/uncertain published results explicitly. Preserve accepted curve data while making the inconsistency visible.

Regression risks and required controls: Do not discard accepted raw curves, overwrite another producer, or turn a recoverable publication failure into silent data loss.

### PI-006 (Medium) — Post-commit Map refresh failure leaves a saved shape draft that duplicates on retry

Separate committed-save acknowledgement from optional UI refresh; end the saved draft before refreshing and offer redraw retry without reinsertion.

Regression risks and required controls: Keep drafts on genuine save failure/Cancel, and preserve undo/redo and active-shape-layer behavior.

### TK-05 (Medium) — Geo destruction leaves startup and poll timers naming deleted Tcl commands

Store/cancel owner job IDs before command destruction and prevent rescheduling after disposal.

Regression risks and required controls: Startup delay, polling, unexpected close and parent/child cancellation ordering.

### TK-06 (Medium) — Repeated-root fixtures amplify lifecycle state left by earlier modules

Correct owner cleanup, assert weak-reference/callback baselines and keep a long serial stress job; subprocess isolation can contain independent groups but cannot prove a product fix.

Regression risks and required controls: Do not hide failures by weakening tests or replacing serial qualification with only isolated runs.

### TK-07 (Medium) — Embedded figure ownership still needs sequence-level qualification

Trace retained owners before changing canvas integration; qualify idle draw, toolbar, bindings and close during raster preparation on both toolkit versions.

Regression risks and required controls: Keep renderers independent; high-water RSS alone is not proof of a leak, and no evidence supports blaming a library by name alone.

### FA72-004 (Low) — Valid JSON with malformed generation fields escapes project-open error handling

Validate handoff/accepted-record field types and ranges; convert failures into the existing unverified-copy contract.

Regression risks and required controls: Corrupt valid JSON, missing/negative/oversized fields and old handoff formats; do not silently accept an invalid record.

### FA72-005 (Low) — Recovery Access labels its own current schema as a newer application version

Share a dependency-light schema version constant or keep a guarded consistency check so recovery and database metadata cannot drift.

Regression risks and required controls: Maintain recovery independence from normal migrating/writing database import paths and older/newer schema safety.

### FA72-008 (Low) — Production import accepts non-finite volumes as successful numeric data

Validate finite numeric inputs and conversion results and report the offending row/column; keep missing data distinct from invalid values.

Regression risks and required controls: Existing null markers, legitimate negative adjustments, large finite volumes and update/replace transaction semantics.

### FA72-012 (Low) — LIC progress claims success for a whole batch that rolled back

Reconcile progress counters after batch commit/rollback and label completion with errors accurately; distinguish provisional processed work from durable additions.

Regression risks and required controls: Keep per-file savepoints, summary details and partial-batch cancellation accounting consistent.

### FA72-009 (Cleanup) — Cross Section retains IDs of completed scheduled callbacks until close

Remove each completed job ID in an owner-safe wrapper/finally, preserving cancellation and disposal checks.

Regression risks and required controls: Cancelled, failed and nested callbacks and close ordering; no evidence ties this bookkeeping issue to SIGSEGV.

### FA72-011 (Cleanup) — Current crash report incorrectly says Cross Section code is unchanged since v0.9.61

Correct the evidence statement and retain an exact changed-file/commit ledger.

Regression risks and required controls: Keep original crash evidence and clearly label historical versus current test/code revisions.

## Changes that are not justified by this audit

No UI overhaul, renderer merger, framework replacement, speculative cache rewrite, schema redesign, inferred fraction conversion or new TVD geological convention. Keep existing save behavior and explicitly surface failures. Correct only demonstrated paths, then qualify the exact customer package.
