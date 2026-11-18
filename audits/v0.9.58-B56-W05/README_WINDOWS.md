# B56-W05 — v0.9.58 native Windows follow-up

This external helper does not change Workbench source or package files, production licenses, embedded trust or the OS clock. It runs generated test licenses and simulated dates in isolated temporary state. Its output must be outside the checkout/package. It tests compiled licensing extensions in a Python host, **not the customer executable**.

The attached customer ZIP could not be transferred into this audit environment (32 MiB transfer limit). Consequently the helper records hashes of the actual packaged PYDs on your machine, but they are **not yet independently pinned to the uploaded ZIP**. Please make the same ZIP available through a GitHub Release so Codex can independently match them. Do not reuse the v0.9.57 helper: its expected hashes are obsolete.

Extract this audit bundle outside Workbench. In PowerShell in the extracted folder, run:

```powershell
$root = 'D:\OandG_Workbench_v0.9.58'
py -3.12 -B .\windows_verify_B56_W05_v0958.py --checkout "$root" --package "$root\dist\OandG_Workbench" --out "$env:USERPROFILE\Desktop\B56-W05-v0958-results"
```

Adjust `$root` to your exact verified source folder; the command above follows the path in your supplied screenshot. Use the CPython 3.12 environment that already has pytest and Workbench dependencies installed. If testing an extracted customer ZIP instead of `dist`, set `--package` to the folder containing the actual OandG_Workbench.exe and _internal directory. Never point it at an owner tool or a different version.

The helper pins relevant source/test/support files to final commit 104bf4f, requires actual ExtensionFileLoader origins within the specified package, records both packaged PYD SHA-256 hashes, checks the v0.9.58 lock-fix API, and repeats the held-lock regression with real Windows locking/DPAPI. It checks that expiry survives the old writer finishing, process restart, simulated rollback, reimport and renewal, with the original still denied. The production timeout remains ten seconds. It reruns all three licensing files with the package PYDs preloaded in pytest and its child Python interpreters. Only the Git-only repository test is deselected; that test already passed independently in the exact checkout with 914 tracked files.

Return the output folder, especially windows-B56-W05-summary.json, package-licensing-hashes.json, windows-compiled-tests.log, windows-compiled-results.xml and all origins-*.json / pytest-origins-*.json. Exit 0 means this helper's cases and pytest completed successfully. Exit 1 with error/traceback is inconclusive; an explicit `still reproducible` means the regression reproduced. Inspect the summary instead of treating every exit 1 as the licensing defect.

The helper was syntax checked but **not executed on Windows here**. Expected results are not recorded as actual passes. Your supplied 56-pass Windows run remains separate evidence; module-origin/hash capture was not supplied with that screenshot.

For an actual customer executable clock test, use only a disposable Windows VM, unchanged customer executable and existing embedded trust, legitimate production-signed expiring and renewal test licenses, and the same retained profile/disk/DPAPI state. Do not restore an older disk snapshot between expiry and rollback. Do not change the real PC clock or inject test trust. Observe expiry denial, rollback/restart/reimport denial, renewal acceptance and continued original-license denial. A helper run in Python does not establish these frozen-executable results.
