# B56-W05 — v0.9.58 accepted Windows verification command

This external helper does not change Workbench source or package files, production licenses, embedded trust or the OS clock. It runs generated test licenses and simulated dates in isolated temporary state. Its output must be outside the checkout/package. It tests compiled licensing extensions in a Python host, **not the customer executable**.

The release ZIP was independently downloaded and CRC/hash checked from tag **v0.958-WindowsCustomer**. Archive SHA-256: **355d4caee6bf2eda2796662aec3790bf8f8f399d51fafb0ba078fde12b1d1914**. The helper requires the exact two packaged extension hashes inspected in that ZIP, with no source fallback or different build accepted. Do not reuse the v0.9.57 helper.

Extract this audit bundle outside Workbench. In PowerShell in the extracted folder, run:

```powershell
$root = 'D:\OandG_Workbench_v0.9.58'
py -3.12 -B .\windows_verify_B56_W05_v0958.py --checkout "$root" --package "$root\dist\OandG_Workbench" --out "$env:USERPROFILE\Desktop\B56-W05-v0958-results"
```

Adjust `$root` to your exact verified source folder; the command above follows the path in your supplied screenshot. Use the CPython 3.12 environment that already has pytest and Workbench dependencies installed. If testing an extracted customer ZIP instead of `dist`, set `--package` to the folder containing the actual OandG_Workbench.exe and _internal directory. Never point it at an owner tool or a different version.

The helper pins relevant source/test/support files to final commit 104bf4f, requires actual ExtensionFileLoader origins within the specified package, checks and records both pinned packaged PYD SHA-256 hashes, checks the v0.9.58 lock-fix API, and repeats the held-lock regression with real Windows locking/DPAPI. It checks that expiry survives the old writer finishing, process restart, simulated rollback, reimport and renewal, with the original still denied. The production timeout remains ten seconds. It reruns all three licensing files with the package PYDs preloaded in pytest and its child Python interpreters. Only the Git-only repository test is deselected; that test already passed independently in the exact checkout with 914 tracked files.

For any future rerun, preserve the output folder, especially windows-B56-W05-summary.json, package-licensing-hashes.json, windows-compiled-tests.log, windows-compiled-results.xml and all origins-*.json / pytest-origins-*.json. Exit 0 means this helper's cases and pytest completed successfully. Exit 1 with error/traceback is inconclusive; an explicit `still reproducible` means the regression reproduced. Inspect the summary instead of treating every exit 1 as the licensing defect.

**Status: completed by the user and independently reconciled.** The supplied B56-W05-v0958-results.zip records all helper scenarios passing, exact packaged-module hashes/origins, and pytest 56 passed / 1 deselected / 5 passing subtests, zero failures/skips and pytest exit 0. B56-W05 is closed for the shipped Windows licensing extensions. This command is retained for reproduction; no further run is requested for that closure. Codex did not execute a native Windows process on its Linux host. The frozen customer EXE remains untested separately.

For an actual customer executable clock test, use only a disposable Windows VM, unchanged customer executable and existing embedded trust, legitimate production-signed expiring and renewal test licenses, and the same retained profile/disk/DPAPI state. Do not restore an older disk snapshot between expiry and rollback. Do not change the real PC clock or inject test trust. Observe expiry denial, rollback/restart/reimport denial, renewal acceptance and continued original-license denial. A helper run in Python does not establish these frozen-executable results.
