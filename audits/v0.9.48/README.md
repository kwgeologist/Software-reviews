# O&G Workbench v0.9.48 — Pre-Release Audit

**Clean except for listed material risks. Fix identified items first.** No demonstrated numerical release blocker; three confirmed feature/gate defects and one manual-fault scope risk. Windows validation is incomplete.

- [Read report](OandG_Workbench_v0.9.48_Audit.md)
- [PDF](OandG_Workbench_v0.9.48_Audit.pdf)
- [HTML](OandG_Workbench_v0.9.48_Audit.html)
- [Download report/evidence bundle](OandG_Workbench_v0.9.48_Audit_Bundle.zip)
- [Structured summary](audit-summary.json) and [findings](findings.json)
- [Evidence and reproduction limits](evidence/README.md)

Full source suite: **2,664 passed, 4 failed, 19 skipped**, plus 684 passing subtests. The report explains two ZIP-without-Git failures, two repeated baseline GUI/font/layout assertions, and all skips. Compiled reference suite: 219 passed / 1 Windows-only skip; compiled integration: 88 passed. Counts overlap and are not additive.

All 899 supplied files remain unchanged. No application code or client data is included. Audit builds, licenses and private keys are excluded. The PDF contains exactly the nine requested report sections. SHA256SUMS.txt verifies the top-level artifacts.
