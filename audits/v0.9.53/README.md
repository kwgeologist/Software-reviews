# O&G Workbench v0.9.53 audit

**Clean except for listed material risks; fix listed items first.** Six confirmed category B findings. No established A blocker or Cython numerical difference in the performed checks. All 905 supplied source files remain unchanged.

- [Report](OandG_Workbench_v0.9.53_Audit.md)
- [PDF](OandG_Workbench_v0.9.53_Audit.pdf)
- [HTML](OandG_Workbench_v0.9.53_Audit.html)
- [Report and evidence bundle](OandG_Workbench_v0.9.53_Audit_Bundle.zip)
- [Structured findings](findings.json)

Full serial suite: 4 failed, 2730 passed, 19 skipped, 2 warnings, 715 subtests passed in 1305.79s (0:21:45). Other cohorts overlap. Historical native Tk crashes remain unresolved; no current parallel full run is claimed. Windows build/package validation is incomplete.

The evidence contains test XML/logs, inventory and synthetic reproductions. There is no application archive, executable, private key, license or client project. Paths refer to the audit environment and probes must be retargeted to the same source/tooling. volumetrics-content-evidence.json is historical byte context only, not current behavioral proof. The archive limit probe lowers a constant to exercise the exact oversize branch without allocating 512MB; its default-limit positive control detects the protected source. Trial staging explicitly allowed the EULA placeholder and is not production qualification.
