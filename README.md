# Software reviews

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
