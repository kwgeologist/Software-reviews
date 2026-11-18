# O&G Workbench v0.9.58 — B56-W05 Recheck

18 November 2026 · Read-only · Limited to license expiry after clock rollback

## Verdict and closure status

**Windows packaged behavior still unverified. B56-W05 is not yet fully closed.** The previously demonstrated held-lock defect is corrected in the exact final source commit: the independent process regression now passes, including the older writer finishing, restart, simulated rollback, reimport, signed renewal and continued denial of the original license. No remaining reproduction was found in the tested source paths.

The remaining gap is evidence for the actual Windows customer package. The attachment could not be transferred into this environment because it exceeds the available file-transfer tool's **32 MiB limit**. No customer ZIP hash, extension hash, package inspection or packaged execution is claimed for this recheck. A request for a GitHub Release asset link to the same ZIP has been sent. This is a transfer limitation of the audit environment, not evidence that the uploaded ZIP is invalid.

## Verified inputs and provenance

- Repository: https://github.com/kwgeologist/O-G-WorkBench (private access succeeded).
- Branch fetched: release/1.0; exact detached worktree: **104bf4f32cbc66ab2f01ca865f388ea016cc7922**.
- Checkout: /workspace/verify-v0.9.58-B56-W05/checkout.
- git ls-files -z succeeded with exit 0 and **914 nonempty tracked entries** before accepting the repository test. The tracked list and file hashes are in the evidence.
- Requested customer input: **OandG_Workbench_v0.9.58_WindowsCustomer.zip**, uploaded file ID file_00000000d9a08212b7d5f10802a76c14. Transfer failed before contents could be accessed. No previous v0.9.57 package was substituted.
- Packaged ogcore/licensing and ogcore/license_runtime extensions: **not inspected, hashes pending**. Old hashes are not reused.

## Independent results

- Three source licensing test files: **49 passed, 0 failed, 8 skipped, 5 passing subtests**, 50.05 seconds. Seven v0.9.58 cases passed and its DPAPI case skipped. Across all files the skips comprise three Windows DPAPI tests and five display-dependent licensing/recovery tests.
- Git-only repository test, separately rerun: **1 passed, 0 failed, 0 skipped**, 0.37 seconds. This case is also included in the three-file run; do not add it to the pass total.
- Independent ordinary source restart/reimport/renewal/original-denial scenario: **passed**.
- Independent ordinary source concurrent-process scenario: **passed**.
- Independent real-timeout held-lock source regression: **passed**, wait **10.046658656996442 seconds**. Production timeout remained ten seconds.
- Native Windows packaged-extension checks performed here: **none**. Customer executable checks performed here: **none**. Unexecuted platform checks are not counted as passes.

These independently executed results used Python 3.12 on Linux, pure-Python source, POSIX process locking and PlainProtector. They establish the source counterexample is fixed; they do not substitute for Windows DPAPI/locking or frozen-executable validation.

## Supplied Windows evidence

The user reports **56 passed, 0 failed, 0 skipped, 1 Git-only test deselected, 5 passing subtests**. The attached screenshot shows the three licensing files, 56 passed / 1 deselected / 5 subtests passed in 75.72 seconds, and a successful Windows build.

The supplied command was: py -3.12 -m pytest -q tests/test_licensing.py tests/test_v0957_fixes.py tests/test_v0958_fixes.py --tb=short -rs -k "not test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository".

This is supplied Windows evidence, not a run independently observed here. The screenshot does not capture actual licensing module origins/hashes, so it does not independently establish that those tests loaded the exact extensions from the customer ZIP. The owner's licensing-tool self-test shown in the build output is not an actual customer EXE clock-rollback test.

## What changed and why the regression now passes

At ogcore/licensing.py:657, ClockState._update only reads/modifies/writes under the serialization lock. At lines 791–844, _state_lock now raises LicenseStateBusy at the timeout instead of returning an unlocked context. The old writer therefore cannot race with an unlocked competing state write.

ClockState.record_expired (line 758) falls back to a separate protected per-identity pending file when its state update cannot acquire the lock. Pending records are checked immediately by expired_on (line 643), merged under the state lock by _merge_pending (line 712), and removed only after being incorporated into the written state. Thus an older state snapshot can finish without erasing the separate pending expiry. A subsequent fresh check denies the expired payload and merges its pending record. A separately signed renewal has its own identity and remains usable.

The independent probe retains the earlier counterexample's ordering: process A reads the pre-expiry state and is paused at the real atomic-write boundary while holding its lock; process B checks a verified expired signed payload and waits the unchanged production timeout; A then resumes. No state bytes are manually deleted or corrupted. The scheduling hook is external to the checkout and all dates are API parameters, not OS clock changes.

Observed sequence:

- Expired check returned expired and explicitly reported the busy state lock and pending expiry.
- The expiry was discoverable before A resumed and remained discoverable after A finished.
- A fresh process at the earlier simulated date returned expired.
- Another rollback check and reimport of the identical payload returned expired.
- A valid signed renewal with the same license ID installed and checked as valid.
- The original signed payload still checked as expired after renewal.
- Pending files were merged and cleared; no expiry was lost.

This is a functional regression pass, not merely an assertion that the new helper or test exists. The ordinary four-process persistence scenario also passed. It does not measure the frequency of real-world stalls or establish behavior under deliberate removal of all state; those are outside this recheck.

## Exact independent commands

Source setup used git fetch origin release/1.0 from the existing authentic clone, then git worktree add --detach /workspace/verify-v0.9.58-B56-W05/checkout 104bf4f. Git rev-parse HEAD returned the full SHA above. git ls-files -z was run from this worktree, check=True, and nonempty entries counted before pytest.

Both pytest commands below used cwd /workspace/verify-v0.9.58-B56-W05/checkout:

PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python -m pytest -q -p no:cacheprovider tests/test_licensing.py tests/test_v0957_fixes.py tests/test_v0958_fixes.py --tb=short -rs --junitxml=/workspace/verify-v0.9.58-B56-W05/source-results.xml

PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python -m pytest -q -p no:cacheprovider tests/test_licensing.py::LicenseManager::test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository --junitxml=/workspace/verify-v0.9.58-B56-W05/repository-check-results.xml

Independent external regression command:

PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python /workspace/verify-v0.9.58-B56-W05/probes/posix_process_control.py --checkout /workspace/verify-v0.9.58-B56-W05/checkout --package /workspace/verify-v0.9.58-B56-W05/package-not-yet-accessible --out /workspace/verify-v0.9.58-B56-W05/process-control-output --skip-pytest

The source control's package argument is an unused label inherited from the earlier harness; that nonexistent path was not opened, imported or treated as an inspected artifact. Its module-origin logs identify the exact source checkout. Probe exit code: 0. Tests and all probes were kept outside the application source/package; bytecode/cache writes were disabled for test execution.

## Native follow-up and next closure evidence

An updated Windows helper, **windows_verify_B56_W05_v0958.py**, is included with README_WINDOWS.md and the exact PowerShell command. It pins relevant source/support/test files to 104bf4f, refuses source fallback for both licensing modules, records loaded-module origins and hashes, repeats the held-lock sequence under real Windows locking/DPAPI, and reruns all three licensing files with the customer-package PYDs preloaded in pytest and its child interpreters. Only the independently passed Git-only case is deselected.

Because the ZIP is not yet independently accessible, this helper **records hashes on the Windows machine rather than claiming a previously verified package digest**. Those records must subsequently be matched to the same supplied customer ZIP. It has been syntax-checked, but has not been executed on Windows here. An actual native helper pass is still needed; expected counts are not fabricated as results.

Return the output folder's summary, PYD hashes, origin records, pytest log and XML. For an actual customer executable clock test, use only a disposable Windows VM with the unchanged package, existing embedded trust, legitimate production-signed test licenses and retained profile/disk/DPAPI state. Do not roll back the VM disk between expiry and clock rollback, change the real PC clock, or inject alternate trust. Compiled extensions in a Python test host and the customer executable are separate verification layers.

## Read-only integrity and disposition

All **914 tracked source files remain byte-identical** and the final checkout is clean at 104bf4f32cbc66ab2f01ca865f388ea016cc7922. No code, tests, source licensing keys, customer binaries, licenses or release artifacts were modified. The customer ZIP was not accessible to modify. Only this report, audit evidence and the external follow-up helper are published to Software-reviews.

**Disposition:** source fix verified for B56-W05, including the independent held-lock regression; full Windows customer-package closure remains pending artifact inspection and native origin-confirmed results. No other release findings were audited.
