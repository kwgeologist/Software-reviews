# v0.9.58 — B56-W05 read-only recheck

**Source regression passed; Windows packaged behavior still unverified.** Exact commit: 104bf4f32cbc66ab2f01ca865f388ea016cc7922. The original held-lock expiry loss no longer reproduces: expiry survives the older writer, restart, rollback and reimport; renewal works and the original stays denied.

- [Report](OandG_Workbench_v0.9.58_B56-W05_Verification.md)
- [PDF](OandG_Workbench_v0.9.58_B56-W05_Verification.pdf)
- [Report, evidence and Windows helper ZIP](OandG_Workbench_v0.9.58_B56-W05_Verification_Bundle.zip)
- [Exact Windows follow-up command](README_WINDOWS.md)
- [Summary](verification-summary.json)

Independent source suite: 49 passed, 8 skipped, 5 passing subtests. Repository case: 1 passed, after git ls-files returned 914 tracked entries. Supplied Windows result: 56 passed, 1 deselected, 5 passing subtests, zero failures/skips. Supplied results are not an independently observed packaged run.

**Customer package inspected:** the 156,107,560-byte release ZIP downloaded successfully from tag v0.958-WindowsCustomer; CRC passed and SHA-256 matches GitHub's displayed digest: 355d4caee6bf2eda2796662aec3790bf8f8f399d51fafb0ba078fde12b1d1914. Both Windows licensing extensions were PE-inspected and hashed. The updated helper now requires those exact hashes. Native execution remains pending: the helper tests compiled extensions in Python, not the frozen customer EXE. Run only this updated helper, not the v0.9.57 version. See README_WINDOWS.md for the exact command and outputs to return.

All 914 tracked source files and 2,303 extracted customer files remain unchanged, checkout clean. No release artifact was modified. Only B56-W05 was reviewed.
