# B56-W05 Windows compiled-extension follow-up

This audit helper is separate from Workbench. It does not change source, package files, production licenses, embedded trust or the OS clock. It uses temporary application-data directories, generated test licenses and simulated dates. It tests the exact customer-package `.pyd` files in a Python host, **not the frozen customer executable**.

## Run on your normal Windows PC

1. Download/extract this verification bundle to a folder outside the Workbench source/package.
2. Open PowerShell in that extracted folder (where `windows_verify_B56_W05.py` is located).
3. Run (adjust only the Workbench root path if yours differs):

```powershell
$root = 'D:\OandG_Workbench\OandG_Workbench_v0.9.57'
py -3.12 -B .\windows_verify_B56_W05.py --checkout "$root" --package "$root\dist\OandG_Workbench" --out "$env:USERPROFILE\Desktop\B56-W05-results"
```

The package contains CPython 3.12 extensions, so use `py -3.12`. Use the same Python environment in which pytest and Workbench dependencies are already installed. The helper refuses unsupported platforms, Python optimization, source fallback, mismatched source hashes or mismatched extension hashes. Output must be outside the checkout/package.

The helper:

- Records module origins/hashes for the parent and child interpreters.
- Uses actual Windows DPAPI and the compiled implementation's Windows state lock.
- Checks expiry, rollback, process restart, reimport, signed renewal and continued rejection of the original.
- Exercises ordinary concurrent processes and a real lock holder delayed beyond the unchanged production timeout.
- Runs both requested pytest files with the pinned packaged PYDs preloaded in pytest and its subprocesses. The sole repository-only test is deselected because Codex independently reran it successfully in the verified Git checkout with 913 tracked files. This follow-up therefore does not require Git on your Windows PC.

**Return the files in `Desktop\B56-W05-results`:** especially `windows-B56-W05-summary.json`, `windows-compiled-tests.log`, `windows-compiled-results.xml`, and `origins-*.json` / `pytest-origins-*.json`.

A helper exit code **1** with `verdict_for_timeout_probe: still reproducible` means the remaining race was reproduced; it is not an unexpected helper crash. An `error`/`traceback` in the summary or Python error output instead means that run is inconclusive. Pytest may pass all ordinary cases even while the independent timeout probe reproduces the bug.

The independent helper was syntax-checked; its persistence scheduling was exercised on Linux source with POSIX locking/PlainProtector. It has **not been executed on Windows by Codex**. Do not treat it as a Windows pass until you run it and preserve the results.

## Customer executable clock test: disposable Windows VM only

Do **not** change your real PC's clock. This helper deliberately does not automate OS-date changes or modify customer executable trust.

To validate the actual EXE after the remaining source issue is resolved, use a disposable Windows VM with:

- The unchanged supplied customer package and its existing embedded production trust.
- A legitimately production-signed time-limited test license plus a separately signed valid renewal, usable in that VM (unbound or correctly bound to its machine ID).
- One retained VM user/profile/disk state across the test. Do not restore an older disk snapshot between steps, because that would discard the expiry record instead of testing its persistence. If clock sync is disabled, do so only inside that disposable VM.

In the VM only, use the same profile/state and select the old signed test license through the documented `OGW_LICENSE_FILE` path. Check it once after its expiry (expect exit 3), roll the VM clock back into its validity window, restart the app/VM while retaining state (expect 3), and reimport the identical old license (must remain refused). Import/select a valid signed renewal (expect 0), then explicitly select the old payload again (expect 3), and return to the renewal (expect 0). A refused import must not replace a working renewal; test selection of the old file explicitly when measuring the old license's denial.

Use this waiting form to collect the actual GUI executable's exit code:

```powershell
$package = 'C:\Audit\OandG_Workbench'
$process = Start-Process -FilePath "$package\OandG_Workbench.exe" -ArgumentList '--self-test' -Wait -PassThru
$process.ExitCode
```

Repeat for the defined clock/license stages; record the simulated VM date, selected signed license identity, exit code and retained state between runs. Do not inject a test public key, patch `sys.frozen`, modify the package or use the source issuer's local trust as customer EXE proof.
