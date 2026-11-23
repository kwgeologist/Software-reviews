# O&G Workbench v0.9.72 — Read-only audit bundle

Baseline: `cbc253ccf2793859fa909e9b8521331ddf389f22`, release/1.0.
Received source ZIP SHA-256: `41ece88abe5430264e5e3905e4ee1df425cffab10c5a66fe0d2d5ca4edba2b17`.

Start with `OandG_Workbench_v0.9.72_Full_Audit.pdf` or its Markdown version. All seven required standalone reports are included, plus the previous-findings matrix and evidence.

Full serial run: **3224 passed, 10 skipped, 365 warnings, 1214 subtests passed in 4231.52s (1:10:31); inferior exit 0; gdb exit 0**. Additional compiled Linux target checks: 128 passed, 4 skipped, 74 subtests passed. Counts overlap; do not sum them as unique coverage.

There are 22 current entries: 12 new FA72 items, 3 incomplete earlier corrections, and 7 retained Tk investigation/ownership items. Fourteen of 17 original combined-audit regressions are corrected. The original intermittent Tk SIGSEGV remains open. No Windows customer binaries were supplied for this source-release audit.

No Workbench code, tests, dependency declarations, versions or release artifacts were changed. All data probes use disposable synthetic projects. No client databases, screenshot, credentials, unnecessary application source or product binaries are included.

`evidence/` contains exact commands, logs/XML, source/input hashes, runtime identity, compiled-extension origins, scripts, measurements and reproductions. Historical Tk panic traces are explicitly labelled under `evidence/prior-v0.9.70/`. Scripts record absolute paths on the audit host; adapt environment roots when reproducing. Probe completion is not a claim that the deliberately failing behavior is correct. `SHA256SUMS.json` covers every member except itself.

Published destination: https://github.com/kwgeologist/Software-reviews/tree/main/audits/v0.9.72-full .
