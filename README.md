# Software reviews

## O&G Workbench v0.9.58 — B56-W05 recheck

**Source held-lock regression passed at 104bf4f; Windows packaged behavior still unverified.** Expiry survives the older writer finishing, restart, simulated rollback and reimport; renewal works while the original remains denied. The attached WindowsCustomer ZIP exceeded the audit environment's 32 MiB transfer limit, so package/PYD hashes and packaged execution remain pending. A GitHub Release asset link to the same ZIP is needed.

- [Read the focused report](audits/v0.9.58-B56-W05/OandG_Workbench_v0.9.58_B56-W05_Verification.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.58-B56-W05/OandG_Workbench_v0.9.58_B56-W05_Verification.pdf)
- [Download report, evidence and updated Windows helper](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.58-B56-W05/OandG_Workbench_v0.9.58_B56-W05_Verification_Bundle.zip)
- [Exact Windows follow-up command](audits/v0.9.58-B56-W05/README_WINDOWS.md)

Independent source suite: **49 passed, 8 skipped, 5 passing subtests**. Repository check: **1 passed**, with **914 tracked files** verified first. Supplied Windows evidence: **56 passed, 1 deselected, 5 passing subtests**, zero failures/skips. All 914 tracked source files remain unchanged. Review limited to B56-W05.

## O&G Workbench v0.9.57 — B56-W05 independent verification

**Still reproducible in the verified source at ed117d8.** A lock-timeout interleaving can erase the expiry record and allow the original license after simulated rollback. Normal paths pass; native Windows extensions/DPAPI and the customer executable were not independently executed here.

- [Read the focused verification report](audits/v0.9.57-B56-W05/OandG_Workbench_v0.9.57_B56-W05_Verification.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.57-B56-W05/OandG_Workbench_v0.9.57_B56-W05_Verification.pdf)
- [Download report, evidence and Windows helper ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.57-B56-W05/OandG_Workbench_v0.9.57_B56-W05_Verification_Bundle.zip)
- [Windows follow-up instructions](audits/v0.9.57-B56-W05/README_WINDOWS.md)

Repository check: **1 passed**, with Git returning **913 tracked files** first. Both source files: **42 passed / 0 failed / 7 skipped**, plus 5 passing subtests. Supplied Windows results remain separately identified. All **5,932 supplied files** and the exact Git checkout remain unchanged. This verification covers only B56-W05.

## O&G Workbench v0.9.56 — Windows security/package audit

Actual WindowsQualified artifacts inspected read-only: **Not ready for release — 2 release blockers, 3 material risks.** All 15 protected Windows x64 modules are present, with no demonstrated source leak or production private key in the customer package. Main blockers: bundled Python 3.12.5 below the declared release security floor, and incomplete segyio LGPL redistribution materials.

- [Read the report](audits/v0.9.56/OandG_Workbench_v0.9.56_Security_Package_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.56/OandG_Workbench_v0.9.56_Security_Package_Audit.pdf)
- [Download report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.56/OandG_Workbench_v0.9.56_Security_Package_Audit_Bundle.zip)
- [Structured findings](audits/v0.9.56/findings.json)
- [Evidence](audits/v0.9.56/evidence)

All **5,862 supplied files remain unchanged**. Focused source security checks: 69 passed / 6 skips, 12 passing subtests. No general functionality/scientific re-audit or new native Windows execution is claimed; actual Windows PE/CArchive/PYZ/staging files were independently inspected. Only reports/curated evidence are published, never the input ZIP, private keys or licenses.

## O&G Workbench v0.9.53

Fresh full release-candidate audit: **Clean except for listed material risks; fix listed items first.** Six category B findings; no established A blocker or demonstrated Cython numerical discrepancy. The report separates normal fixes from remaining concurrency, cache, native importer, source normalization and archive-limit defects.

- [Read the report](audits/v0.9.53/OandG_Workbench_v0.9.53_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.53/OandG_Workbench_v0.9.53_Audit.pdf)
- [Download report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.53/OandG_Workbench_v0.9.53_Audit_Bundle.zip)
- [Evidence](audits/v0.9.53/evidence)
- [Structured findings](audits/v0.9.53/findings.json)

Full serial suite: **2,730 passed / 4 failed / 19 skipped**, plus 715 passing subtests. Failures and the difference from the supplied baseline are explained in the report. Compiled reference tests: 219 passed / 1 skipped; compiled integration: 76 passed. Actual Linux customer/owner builds and CLI checks completed; native Windows qualification remains incomplete. Historical Tk crashes remain unresolved. All **905 supplied files remain unchanged**; only audit deliverables are published.

## O&G Workbench v0.9.52

Fresh full pre-release audit: **Not ready for Windows validation.** One release blocker (alias ownership can silently select a different geological top) and five material defects/risks. No demonstrated Cython numerical discrepancy. Historical Tk segmentation faults remain unresolved; none reproduced in the current serial or parallel full run.

- [Read the report](audits/v0.9.52/OandG_Workbench_v0.9.52_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.52/OandG_Workbench_v0.9.52_Audit.pdf)
- [Download report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.52/OandG_Workbench_v0.9.52_Audit_Bundle.zip)
- [Evidence files](audits/v0.9.52/evidence)
- [Structured findings](audits/v0.9.52/findings.json)

Full serial and parallel source runs each: **2,700 passed, 4 failed, 19 skipped**, plus 701 passing subtests. Failures are explained in the report. Compiled reference cohort: 219 passed / 1 skipped. Actual Linux customer/owner specs built; Windows qualification remains incomplete. All **904 supplied files remain unchanged**. Only audit deliverables are published; no application source archive, binaries, private keys, licenses or client projects.

## O&G Workbench v0.9.48

Read-only pre-release audit against the accepted v0.9.45 baseline: **Clean except for listed material risks; fix identified items first.** Three confirmed feature/release-gate defects and one manual-fault scope risk. No demonstrated Cython numerical blocker. Windows validation remains incomplete.

- [Read the report](audits/v0.9.48/OandG_Workbench_v0.9.48_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.48/OandG_Workbench_v0.9.48_Audit.pdf)
- [Download report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.48/OandG_Workbench_v0.9.48_Audit_Bundle.zip)
- [Evidence files](audits/v0.9.48/evidence)

Full source suite: **2,664 passed, 4 failed, 19 skipped**, plus 684 passing subtests. The report explains two archive-without-Git failures and two repeated baseline font/layout assertions. Compiled reference tests: 219 passed / 1 skipped; compiled integration: 88 passed. Separate cohorts overlap. All **899 supplied files remain unchanged**. Only audit deliverables are published; no application source, binaries, licenses, private keys or client projects are included.

## O&G Workbench v0.9.39

Fresh whole-package read-only audit for private/internal v1.0: **BLOCK v1.0**. Six new confirmed defects: **5 High, 1 Medium**. The previously known A38-P01 dense-label limitation remains **Medium**, separately identified.

- [Read the report](audits/v0.9.39/OandG_Workbench_v0.9.39_Audit.md)
- [Download PDF](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.39/OandG_Workbench_v0.9.39_Audit.pdf)
- [Download complete report and evidence ZIP](https://github.com/kwgeologist/Software-reviews/raw/refs/heads/main/audits/v0.9.39/OandG_Workbench_v0.9.39_Audit_Bundle.zip)
- [Detailed evidence files](audits/v0.9.39/evidence)
- [Structured findings](audits/v0.9.39/findings.json)

The full single-process suite hit a Linux/Tk segmentation fault. A complete serial file-isolated rerun recorded **2,596 passed, 4 failed, 15 skipped**, plus **605 passing subtests**. The report distinguishes two archive-without-Git failures, one Tk font-substitution failure and one Seismic toolbar layout assertion. It does not claim the crashed run passed. All eight focused v0.9.39 regressions passed independently. Five launcher self-tests were refused at the missing-license gate; Windows packaged runtime was not tested.

Includes Map measurements at 100,000 / 250,000 / 500,000 wells, a separate million-well symbol-oriented run, and a richer 100,000-well asset fixture. All **887 source files remain byte-identical**, with no missing or added files. No application changes were made. Report/evidence publication is separately authorized by the user.

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
