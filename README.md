# Software reviews

## O&G Workbench v0.9.18

Independent read-only release audit: **9 findings — 6 High, 1 Medium, 2 Low**. Proceed to targeted release hardening; resolve the six High findings before external release. Application source remains unchanged.

- [Read the report](audits/v0.9.18/OandG_Workbench_v0.9.18_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.18/OandG_Workbench_v0.9.18_Audit.pdf)
- [Download report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.18/OandG_Workbench_v0.9.18_Audit_Bundle.zip)
- [HTML report](audits/v0.9.18/OandG_Workbench_v0.9.18_Audit.html)
- [Evidence files](audits/v0.9.18/evidence)

Full GUI-enabled suite: **2,132 passed, 1 failed, 14 skipped**, plus 565 passing subtests. The font failure is attributable to cloud Tk font substitution; all three source self-tests passed. All 670 application archive files remained unchanged. Windows binaries were not executed. The report identifies the exact source ZIP hash rather than claiming verified Git commit provenance.

The report records the read-only audit as completed before publication. These deliverables were subsequently committed and pushed at the user's explicit request. The bundle contains synthetic evidence, not application source or client data.

## O&G Workbench v0.9.4

Independent read-only audit of the uploaded v0.9.4 archive: **15 findings — 4 Critical, 5 High, 5 Medium, 1 Low**. **Overall assessment: Do not release unchanged.** No application code was modified and no PR was created.

- [Read the report](audits/v0.9.4/OandG_Workbench_v0.9.4_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.4/OandG_Workbench_v0.9.4_Audit.pdf)
- [Download report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.4/OandG_Workbench_v0.9.4_Audit_Bundle.zip)
- [HTML report](audits/v0.9.4/OandG_Workbench_v0.9.4_Audit.html)
- [Structured findings](audits/v0.9.4/findings.json)

Full GUI-enabled suite: **1,827 passed, 1 failed, 9 skipped**, plus 521 passing subtests. The font-weight assertion fails in this cloud Tk environment. Separately, the real Geo source self-test exits 1 on its obsolete 100-symbol requirement; v0.9.4 intentionally ships 29 symbols. Windows runtime acceptance was not executed. The requested branch HEAD could not be identified from the archive; the report pins its exact ZIP SHA-256.

All 613 source files remain byte-identical. The bundle includes logs and controlled synthetic probes, not application source or client databases. If a file opens instead of saving, select **Download raw file** on GitHub.

## O&G Workbench v0.8.58

Independent read-only release audit: **15 findings — 6 release blockers, 5 high, 3 medium, 1 low**. Application source remains unchanged.

- [Read the report](audits/v0.8.58/OandG_Workbench_v0.8.58_Audit.md)
- [PDF report](audits/v0.8.58/OandG_Workbench_v0.8.58_Audit.pdf)
- [HTML report](audits/v0.8.58/OandG_Workbench_v0.8.58_Audit.html)
- [Complete report and evidence bundle](audits/v0.8.58/OandG_Workbench_v0.8.58_Audit_Bundle.zip)
- [Structured findings](audits/v0.8.58/findings.json)

Full GUI-enabled suite: **1,674 passed, 1 failed, 9 skipped**, plus 354 passing subtests. The font failure is environment dependent; the report distinguishes it from a separately reproduced lifecycle defect. Rw passed 20 repeated UI runs but earlier intermittence remains unexplained. Windows installer acceptance was not run. The report does **not** recommend freezing the build yet.

Open a file and select **Download raw file** to save it. The evidence bundle contains synthetic probes and logs, not application source or client databases.

## O&G Workbench v0.8.37

Independent read-only suite audit. No application code was changed during the audit.

- [Read the report](audits/v0.8.37/OandG_Workbench_v0.8.37_Audit.md)
- [PDF report](audits/v0.8.37/OandG_Workbench_v0.8.37_Audit.pdf)
- [HTML report](audits/v0.8.37/OandG_Workbench_v0.8.37_Audit.html)
- [Complete report and evidence bundle](audits/v0.8.37/OandG_Workbench_v0.8.37_Audit_Bundle.zip)

To download a file, open its link and select **Download raw file** on GitHub.

The audit records 29 findings: 2 Critical, 10 High, 9 Medium, 3 Low, and 5 Cleanup.

The initial Linux/Tk 9 test run recorded 1,424 passed, 9 failed, 8 skipped, and 285 passing subtests. A targeted rerun of the nine failures with a writable raster cache recorded 4 passed and 5 failed. See the report for evidence, platform limitations, recommended fixes, and regression tests. The full suite is not described as all passing.

The bundle includes structured findings, test logs/results, synthetic reproduction scripts and evidence, environment details, and source-integrity verification. It does not include the application source or client databases.
