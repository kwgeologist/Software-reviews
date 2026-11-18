# v0.9.58 — B56-W05 verification closed

**B56-W05 closed for the shipped Windows licensing extensions**, source commit 104bf4f32cbc66ab2f01ca865f388ea016cc7922. The user-executed Windows run was independently reconciled against the exact inspected customer ZIP/PYD hashes and all origin, summary, log and XML records. Frozen customer EXE execution remains untested separately; it is not an additional condition of this scoped closure.

- [Report](OandG_Workbench_v0.9.58_B56-W05_Verification.md)
- [PDF](OandG_Workbench_v0.9.58_B56-W05_Verification.pdf)
- [Report, evidence and verification helper ZIP](OandG_Workbench_v0.9.58_B56-W05_Verification_Bundle.zip)
- [Accepted Windows command](README_WINDOWS.md)
- [Summary](verification-summary.json)
- [Windows reconciliation](evidence/windows-evidence-reconciliation.json)
- [Supplied Windows results](evidence/windows-results)

All 8 helper and 15 pytest process-origin records match both shipped licensing PYDs. The real Windows timeout was 10.016 seconds; expiry survived the old writer, restart, rollback and reimport. Renewal succeeded, the original remained expired, pending expiry merged, and DPAPI/concurrency checks passed.

Accepted Windows pytest result: **56 passed, 1 Git-only test deselected, 5 passing subtests, zero failures/errors/skips, pytest exit 0**. XML has 56 testcase elements and suite count 61 including five subtests. Source suite: 49 passed, 8 skipped, 5 passing subtests; independently verified repository case: 1 passed after 914 tracked files were returned by Git. Overlapping cohorts are not added together.

The small original Windows results ZIP and extracted records are retained with their input hash. The Windows run was performed by the user, not on Codex's Linux host. All 914 tracked source files and 2,303 extracted customer files remain unchanged. No other release findings were audited or cleared. No further Windows run is requested for this disposition.
