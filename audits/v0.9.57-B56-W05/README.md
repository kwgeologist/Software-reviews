# B56-W05 independent verification — v0.9.57

**Verdict: still reproducible in the verified Linux source at ed117d8.** A state-lock timeout allows an older writer to erase the recorded expiry. Native Windows extension/DPAPI and customer EXE behavior have not been independently executed here.

- [Verification report](OandG_Workbench_v0.9.57_B56-W05_Verification.md)
- [PDF](OandG_Workbench_v0.9.57_B56-W05_Verification.pdf)
- [HTML](OandG_Workbench_v0.9.57_B56-W05_Verification.html)
- [Report, evidence and Windows helper ZIP](OandG_Workbench_v0.9.57_B56-W05_Verification_Bundle.zip)
- [Windows follow-up instructions](README_WINDOWS.md)
- [Machine-readable summary](verification-summary.json)

Repository check: 1 passed; git ls-files succeeded with 913 tracked files. Both source test files: 42 passed, 0 failed, 7 skipped, 5 passing subtests. Supplied Windows result (not rerun here): 48 passed, 1 failed because Git could not launch, 5 passing subtests. The independent held-lock probe reproduced expired → valid after simulated rollback. No OS clock was changed.

The bundle contains reports, metadata, synthetic reproduction scripts, test logs/XML and a native Windows helper. It contains no application source archive, customer executable, private keys or production licenses. All 5,932 supplied files and the source checkout remain unchanged. Other release findings were not revisited.

Extract the ZIP outside Workbench and follow README_WINDOWS.md. The helper tests exact packaged licensing PYDs in Python, not the customer EXE. An exit 1 accompanied by `verdict_for_timeout_probe: still reproducible` denotes the reproduced race; an error/traceback is inconclusive.
