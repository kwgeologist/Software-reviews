# O&G Workbench v0.9.52 audit

Read-only full pre-release audit. **Not ready for Windows validation: one blocker and five material issues.** All 904 supplied source files remain unchanged.

- [Report](OandG_Workbench_v0.9.52_Audit.md)
- [PDF](OandG_Workbench_v0.9.52_Audit.pdf)
- [HTML](OandG_Workbench_v0.9.52_Audit.html)
- [Evidence bundle](OandG_Workbench_v0.9.52_Audit_Bundle.zip)
- [Structured findings](findings.json)

Full source and parallel runs each: 2,700 passed / 4 failed / 19 skipped, plus 701 passing subtests. See the report for failure classification and overlapping cohort qualifications. Historical Tk crashes remain unresolved; no segmentation fault reproduced in these runs. Windows validation incomplete.

Evidence contains test logs, XML, synthetic reproductions and inventory. It contains no application archive/binaries, client projects, private keys or licenses. Absolute paths refer to the audit environment; probes must be pointed at the identical source and matching tooling when reproduced. `volumetrics-content-evidence.json` is a historical byte comparison only, not current behavioral proof. Trial staging allowed the EULA placeholder explicitly; not a production approval.
