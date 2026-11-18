# O&G Workbench v0.9.58 — B56-W05 Recheck

18 November 2026 · Read-only · Limited to license expiry after clock rollback

## Verdict and closure status

**B56-W05 closed for the shipped Windows licensing extensions** at commit **104bf4f32cbc66ab2f01ca865f388ea016cc7922**. The supplied Windows results now establish that the exact two licensing PYDs independently inspected in the v0.9.58 customer ZIP passed the original held-lock regression with real Windows locking and DPAPI, plus restart, simulated rollback, reimport, signed renewal and continued original-license denial.

The Windows run was executed by the user and independently reconciled here against the prior package inspection, known verification helper, all module-origin records, summary, pytest log and XML. It was not rerun on this Linux audit host. No conflicting artifact hash or test outcome was found.

**Frozen customer EXE execution remains untested.** This is a separate coverage boundary, not a blocker for closure of this specific extension-level expiry-persistence finding. The completed checks exercise the affected shipped implementation and Windows persistence mechanisms directly. They do not establish frozen-EXE startup/dispatch or integration with its embedded production trust. No additional EXE-specific expiry defect is demonstrated; this closure is not a claim of full executable or release qualification. No further Windows run is requested for this scoped disposition.

## Verified inputs and provenance

- Repository: https://github.com/kwgeologist/O-G-WorkBench (private access succeeded).
- Branch fetched: release/1.0; exact detached worktree: **104bf4f32cbc66ab2f01ca865f388ea016cc7922**.
- Checkout: /workspace/verify-v0.9.58-B56-W05/checkout.
- git ls-files -z succeeded with exit 0 and **914 nonempty tracked entries** before accepting the repository test. The tracked list and file hashes are in the evidence.
- Actual customer input: **OandG_Workbench_v0.9.58_WindowsCustomer.zip**, **156,107,560 bytes**, downloaded from https://github.com/kwgeologist/Software-reviews/releases/download/v0.958-WindowsCustomer/OandG_Workbench_v0.9.58_WindowsCustomer.zip.
- Archive SHA-256: **355d4caee6bf2eda2796662aec3790bf8f8f399d51fafb0ba078fde12b1d1914**; matches the published release digest. ZIP CRC: passed. No previous v0.9.57 artifact was substituted.
- Customer root in the ZIP: **OandG_Workbench/**; extracted as /workspace/verify-v0.9.58-B56-W05/input/OandG_Workbench. The customer-only ZIP contains no source checkout or Git metadata. The release tag points to the audit repository, so it is not evidence of Workbench source provenance; the source was independently verified against the actual Workbench Git checkout.
- Customer tree: **2,303 files**; deterministic tree SHA-256 **23ed36df39ebc4733b929f48dce45117880f94d491c62bbfe50286d134842e32** (sorted relative path + NUL + each file SHA256 + LF, then SHA256).
- Customer OandG_Workbench.exe SHA-256: **06ca4fddebd249dfb363db1d1405428d068ebd44340ea72ed55a04714b0e21cb**.

**Packaged extensions inspected:**

- _internal/ogcore/licensing.cp312-win_amd64.pyd — **403,968 bytes**, SHA-256 **e56244f96c476886533a6274341ff69e390c601d05f67f8537b23afabcbd3700**.
- _internal/ogcore/license_runtime.cp312-win_amd64.pyd — **168,448 bytes**, SHA-256 **e1b0b1773754fceb00d8598039c830c904ebf0202761a6a28a4a33f694ec77d2**.

Both are PE machine 0x8664 (Windows x64), importing python312.dll. licensing.pyd contains the new LicenseStateBusy, STATE_LOCK_TIMEOUT, _keep_pending, _merge_pending, flush_pending and record_expired symbol strings. Both hashes differ from v0.9.57. Static symbol presence is consistent with the new fix but is not a runtime behavior test or a reproducible-build proof linking native bytes to the checkout. The updated Windows helper now pins these exact release-PYD hashes.

## Independent results

- Three source licensing test files: **49 passed, 0 failed, 8 skipped, 5 passing subtests**, 50.05 seconds. Seven v0.9.58 cases passed and its DPAPI case skipped. Across all files the skips comprise three Windows DPAPI tests and five display-dependent licensing/recovery tests.
- Git-only repository test, separately rerun: **1 passed, 0 failed, 0 skipped**, 0.37 seconds. This case is also included in the three-file run; do not add it to the pass total.
- Independent ordinary source restart/reimport/renewal/original-denial scenario: **passed**.
- Independent ordinary source concurrent-process scenario: **passed**.
- Independent real-timeout held-lock source regression: **passed**, wait **10.046658656996442 seconds**. Production timeout remained ten seconds.
- Native Windows packaged-extension checks: **user-executed results independently reconciled and accepted below**. No native Windows process was launched on this Linux host. Customer executable checks: **none**.

These independently executed results used Python 3.12 on Linux, pure-Python source, POSIX process locking and PlainProtector. They establish the source counterexample is fixed; they do not substitute for Windows DPAPI/locking or frozen-executable validation.

## Reconciled Windows evidence

Input: **B56-W05-v0958-results.zip**, **13,913 bytes**, SHA-256 **a7ce052bc7d7a833c39c29ffab31c8e858aa69a3941ad3d3846e183710dc3c11**. ZIP CRC passed. The 27 supplied files are preserved under evidence/windows-results; the original small results archive is included as evidence. These are test records, not application or production-license files.

**Module provenance:** package-licensing-hashes.json names the independently inspected customer archive hash and both exact PYD hashes listed above. Every one of **8 origins-*.json records** and **15 pytest-origins-*.json records** names both modules under **D:\OandG_Workbench_v0.9.58\dist\OandG_Workbench\_internal\ogcore** and matches both prior SHA-256 values. The eight helper records explicitly identify ExtensionFileLoader and Python 3.12.5 Windows AMD64. The known pytest bootstrap checks ExtensionFileLoader before writing its origin records. No inspected record reports a .py source fallback, different directory or different binary hash. This covers the helper's parent/child process records and pytest's process records.

**Held-lock behavior:** windows-B56-W05-summary.json records a **10.015999999945052-second** wait, crossing the unchanged production ten-second timeout. The record was present before the older writer resumed and still present after it finished. The original payload's restart, rollback and reimport statuses are all **expired**. Renewal installation and its subsequent check are **valid**; the original after renewal remains **expired**. pending_files_after_merge is **0**. The known helper's ordering and these statuses establish that the pending expiry survived and was merged into persistent state. reproduced is false and the timeout verdict is held-lock regression passed.

**Windows-specific checks:** DPAPI_restart_reimport_renewal_original_denied and DPAPI_concurrent_processes both report **passed**, with no error or traceback. The helper uses real Windows DPAPI and OS locks, isolated test state and simulated dates. host_clock_changed and source_or_package_modified are false. This did not change the real PC clock or customer trust.

**Test reconciliation:** windows-compiled-tests.log and the summary agree exactly: **56 passed, 1 deselected, 5 subtests passed in 73.22 seconds**. The summary records pytest_exit_code **0**. The XML contains **56 testcase elements**, **zero failures, errors or skips**; its suite count is **61**, accounting for the 56 tests plus five passing subtests. All eight v0.9.58 cases are represented. The Git-only case is absent from XML as expected from the exact -k deselection in the recorded command. It had already passed separately in the verified checkout after Git returned 914 tracked entries. Do not count the XML subtest-inclusive suite total as 61 independent top-level passes, or add the separate overlapping repository test to the source-suite pass count.

The earlier supplied screenshot's 56-pass run in 75.72 seconds remains historical supplied evidence. The accepted origin-confirmed follow-up is the 73.22-second run in this results ZIP. Neither is an executable-level clock test.

Independent reconciliation command: **python /workspace/verify-v0.9.58-B56-W05/reconcile_windows_evidence.py**. Exit 0. The script checks all recorded paths/hashes and the required lifecycle/count assertions; its structured result is evidence/windows-evidence-reconciliation.json. It reads the supplied Windows records without executing instructions from them.

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

## Accepted native command and execution boundary

The included **windows_verify_B56_W05_v0958.py** pins relevant source/support/test files to 104bf4f, requires the two exact release-PYD hashes, refuses source fallback, and records parent/child module origins. Its Windows run now supplied and reconciled used the following command (output location and source/package paths agree with the records):

py -3.12 -B .\windows_verify_B56_W05_v0958.py --checkout "D:\OandG_Workbench_v0.9.58" --package "D:\OandG_Workbench_v0.9.58\dist\OandG_Workbench" --out "C:\Users\Admin\Desktop\B56-W05-v0958-results"

The recorded pytest subprocess uses C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe -m pytest -q -p no:cacheprovider, the three full-path licensing test files, -k "not test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository", and --junitxml=C:\Users\Admin\Desktop\B56-W05-v0958-results\windows-compiled-results.xml. The exact argument array is preserved in the supplied summary. The summary records pytest exit 0 and successful helper cases with no helper error; a separate outer-shell helper exit record is not included. The known helper returns 0 for precisely those successful conditions.

This is a test of **shipped compiled extensions in a normal Python host**, using generated signed test payloads through explicit API keys and isolated state. The frozen customer EXE and its existing embedded production trust were not executed or changed. A future executable-level clock qualification, if separately requested, should use a disposable Windows VM with unchanged customer artifacts and retained profile/disk/DPAPI state. It is not required as an additional condition of this narrowly scoped extension-level closure.

## Read-only integrity and disposition

All **914 tracked source files and all 2,303 extracted customer files remain byte-identical**; the final checkout is clean at 104bf4f32cbc66ab2f01ca865f388ea016cc7922. No code, tests, source licensing keys, customer binaries, licenses or release artifacts were modified. The original ZIP hash was rechecked after inspection and is unchanged. Only this report, audit evidence and the external follow-up helper are published to Software-reviews.

**Disposition: B56-W05 closed for the shipped Windows licensing extensions.** Exact source commit and customer PYD hashes are verified; the original held-lock failure passes on the final source and on the hash-matched shipped modules under Windows DPAPI/locking. Frozen customer EXE execution remains explicitly untested. No other release findings were audited or cleared.
