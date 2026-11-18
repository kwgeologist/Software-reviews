# v0.9.58 — B56-W05 read-only recheck

**Source regression passed; Windows packaged behavior still unverified.** Exact commit: 104bf4f32cbc66ab2f01ca865f388ea016cc7922. The original held-lock expiry loss no longer reproduces: expiry survives the older writer, restart, rollback and reimport; renewal works and the original stays denied.

- [Report](OandG_Workbench_v0.9.58_B56-W05_Verification.md)
- [PDF](OandG_Workbench_v0.9.58_B56-W05_Verification.pdf)
- [Report, evidence and Windows helper ZIP](OandG_Workbench_v0.9.58_B56-W05_Verification_Bundle.zip)
- [Exact Windows follow-up command](README_WINDOWS.md)
- [Summary](verification-summary.json)

Independent source suite: 49 passed, 8 skipped, 5 passing subtests. Repository case: 1 passed, after git ls-files returned 914 tracked entries. Supplied Windows result: 56 passed, 1 deselected, 5 passing subtests, zero failures/skips. Supplied results are not an independently observed packaged run.

**Package access is blocked:** the attached WindowsCustomer ZIP exceeds the available transfer tool's 32 MiB limit. No package/PYD hash or inspection is claimed. Please upload the same ZIP to a GitHub Release and provide its asset link. The v0.9.58 helper records actual Windows PYD hashes and module origins but those hashes are not yet independently pinned to the uploaded ZIP. It tests the compiled extensions in Python, not the customer executable. Run only the updated helper, not the v0.9.57 version.

All 914 tracked source files remain unchanged, checkout clean. No release artifact was modified. Only B56-W05 was reviewed.
