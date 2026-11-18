# O&G Workbench v0.9.56 — actual Windows security/package audit

**Not ready for release.** Two release blockers and three material risks. The supplied WindowsQualified source/build/archive was inspected read-only; all 5,862 files remain unchanged.

- [Report](OandG_Workbench_v0.9.56_Security_Package_Audit.md)
- [PDF](OandG_Workbench_v0.9.56_Security_Package_Audit.pdf)
- [HTML](OandG_Workbench_v0.9.56_Security_Package_Audit.html)
- [Report and curated evidence ZIP](OandG_Workbench_v0.9.56_Security_Package_Audit_Bundle.zip)
- [Structured findings](findings.json)

Exact input SHA-256: f377692f7b555e189d30a5d1e5cea45c94ad0d78f9176d798c8e269f0b67d3e1.

All 15 protected Windows x64 modules are present; no actual protected-source copy or production private key was found in the customer package. The main blockers are bundled Python 3.12.5 below the declared release floor and incomplete segyio LGPL materials. The report distinguishes compliance from vulnerabilities, actual findings from negative fixtures, raw dist from final staging, and supplied Windows runs from independent binary inspection.

No Windows executable was run on this Linux audit host. Focused source security tests: 69 passed / 6 skips, with 12 passing subtests. No general functional/scientific audit was repeated. The ordinary checker CLI selects Linux filenames here; actual Windows .exe paths were checked explicitly with its executable/tree routines. See the report before interpreting customer-protection.log as a package failure.

This evidence contains logs, metadata/hashes, legal-reference text and external audit probe scripts. It does not contain the software archive, source implementations, executables, private keys, license bytes or client projects. The upstream LGPL text is evidence, not an added file in the customer package. Paths in probes refer to the audit environment and must be retargeted for reproduction. Minimal negative fixtures are not runnable package validation; actual PE/archive inspection is separately recorded.
