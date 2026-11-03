# Software reviews

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
