# O&G Workbench v0.9.57 — B56-W05 Independent Verification

18 November 2026 · Read-only · Scope: expiry after clock rollback only

## Verdict

**Still reproducible.** The ordinary single-process expiry/restart/reimport/renewal paths now pass in the verified source. However, an independently reproduced lock-timeout interleaving lets a legitimate older writer erase the recorded expiry; the original signed license then returns **valid** after simulated clock rollback.

This counterexample was executed against the exact Git checkout on **Linux Python source, POSIX locking and PlainProtector**. It is not a claim that the Windows `.pyd` or customer EXE was executed here. Native Windows compiled-extension/DPAPI and executable-level reproduction remain unverified independently. The supplied Windows run is recorded separately. B56-W05 cannot be marked closed on the current evidence.

## Verified inputs

- Repository: https://github.com/kwgeologist/O-G-WorkBench
- Branch fetched: `release/1.0`; detached checkout used: **ed117d8bbf66d7be9e67827831fb33dae2cb7a23**.
- Checkout path: `/workspace/verify-v0.9.57-B56-W05/checkout`.
- Exact supplied package archive: **OandG_Workbench_v0.9.57_WindowsQualified.zip**, **669,231,290 bytes**, SHA-256 **ae4939dd89300cd619c276eab530d754fafa8edd30722084c5f77c376f643dec**. ZIP CRC/integrity passed; the screenshot’s digest prefix matches. The archive has no Git metadata; an actual separate Git clone was used, not a synthetic git init.
- Actual customer tree inspected: `input/OandG_Workbench_v0.9.57/dist/OandG_Workbench` (2,303 files). Deterministic tree SHA-256: **b49657887becc05e46aa822d643f4bef5d31bcd8747db034e7b19223ce282700**; definition: SHA256 of sorted relative path + NUL + file SHA256 + LF.
- Customer `OandG_Workbench.exe` SHA-256: **e89baa9a53015c51b1277ce2523b8f3dfe3f55d8087818b4cc72e4c06e47f52e**.

The relevant source/test/build files in the ZIP match the exact checkout after CRLF/LF normalization: ogcore/licensing.py, ogcore/license_runtime.py, ogcore/licensing_keys.py, ogcore/__init__.py, tests/test_licensing.py, tests/test_v0957_fixes.py and tools/release/build_cython.py. Both licensing extensions in the package match their corresponding root built extensions byte for byte. This is source/package consistency evidence, not proof of which module origin was loaded in the supplied Windows run.

**Packaged licensing extensions inspected (Windows x64 PE / CPython 3.12 ABI):**

- `dist/OandG_Workbench/_internal/ogcore/licensing.cp312-win_amd64.pyd`: 362,496 bytes; SHA-256 **0df011b565ec4be36f9beefc56044be6214896443850a06a1c7d587c872d2bc6**.
- `dist/OandG_Workbench/_internal/ogcore/license_runtime.cp312-win_amd64.pyd`: 168,448 bytes; SHA-256 **d89050dca5aab2379e5e44bbdc6ab1d752bdf6e481f8553a6f01fd5944ad1e20**.

Both PE machine values are 0x8664 and import python312.dll. New expiry-record symbols are present in licensing.pyd. Presence/symbol/hash inspection does not count as execution of either extension.

## Repository check and test results

Before accepting the repository test, `git ls-files -z` was run from the exact checkout with check=True: **exit 0, 913 nonempty tracked entries**. The list is preserved in tracked-files.txt and its hash in git-baseline.json. Git executable: `/usr/local/bin/git`. The repository check then passed; no application fix was needed for the reported missing-git launch failure.

Exact commands used on this Linux audit machine (additional no-cache option prevents source-tree cache writes):

`git clone --no-checkout --single-branch --branch release/1.0 https://github.com/kwgeologist/O-G-WorkBench.git /workspace/verify-v0.9.57-B56-W05/checkout`

`git -C /workspace/verify-v0.9.57-B56-W05/checkout checkout --detach ed117d8bbf66d7be9e67827831fb33dae2cb7a23`

`git ls-files -z` (cwd: the verified checkout; successful output verified before pytest)

`PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python -m pytest -q -p no:cacheprovider tests/test_licensing.py::LicenseManager::test_the_manager_never_enters_a_program_and_no_private_key_is_in_the_repository --junitxml=/workspace/verify-v0.9.57-B56-W05/repository-check-results.xml`

`PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python -m pytest -q -p no:cacheprovider tests/test_licensing.py tests/test_v0957_fixes.py --junitxml=/workspace/verify-v0.9.57-B56-W05/source-results.xml`

**Actual results:**

- Repository check: **1 passed, 0 failed, 0 skipped**, 0.40s.
- Both test files, Linux source: **42 passed, 0 failed, 7 skipped, 5 passing subtests**, 4.69s. The seven skips are the two Windows DPAPI tests and five display-dependent licensing/recovery tests. The single-test cohort overlaps this run and must not be added to its pass total.
- Supplied Windows evidence: **48 passed, 1 failed, 5 passing subtests**; the reported failure was Windows failing to launch git. That is supplied evidence, not an independently observed native run. The 49 total cases agree with this checkout’s 49 collected cases. The source/Windows environmental distinction explains the seven skipped Linux cases; it does not establish a Windows pass by substitution.
- Independent source process-control probe: normal restart/reimport/renewal/original-denial scenario **passed**; normal concurrent-process state updates **passed**; held-lock timeout scenario **reproduced the bug** (probe exit 1). No test state/license was edited to force the replay; all dates were simulated parameters.
- Native Windows extension tests in this audit: **not executed**. Actual customer EXE clock test: **not executed**. These are not counted as passes or generic skips.

The pure-Python origins for the Linux execution are in the verified checkout. Windows `.pyd` files were not loadable on this Linux host and no emulation was substituted for Windows DPAPI/locking.

## Remaining failure chain

The fix adds a persistent per-signed-payload expiry record. It correctly keeps the old license denied while allowing a separately signed renewal (including a renewal under the same license ID). Existing tests cover the normal paths, real processes under ordinary lock timing, and DPAPI separately.

The uncovered boundary is `ogcore/licensing.py:653–735`:

1. Writer A takes the state lock, reads a valid state with no expired record, and is delayed before committing a normal `remember()` update.
2. Writer B observes the signed license expired. `_state_lock.__enter__` retries, but at its unmodified **10-second** deadline returns with `locked=False` rather than refusing the update.
3. `_update` does not check that ownership was obtained. B proceeds with an unlocked read/modify/write and records the expiry. Its current check returns `expired`.
4. A resumes and legitimately writes its previously read state, overwriting B’s record. Its normal timestamp update contains no expiry entry.
5. A fresh check of the same signed payload at the earlier simulated date returns **valid**.

The independent multi-process probe used the real lock timeout: **10.04487989199697 seconds** in the observed run. The record was present before the old holder resumed, absent afterward, and replay status was **valid**. The exact independent process command was: PYTHONDONTWRITEBYTECODE=1 /workspace/audit-v0.9.56-windows/tooling/bin/python probes/posix_process_control.py --checkout /workspace/verify-v0.9.57-B56-W05/checkout --package /workspace/verify-v0.9.57-B56-W05/input/OandG_Workbench_v0.9.57/dist/OandG_Workbench --out /workspace/verify-v0.9.57-B56-W05/process-control-output --skip-pytest (cwd: /workspace/verify-v0.9.57-B56-W05). The ordinary multi-process case passed; the failure specifically exercises lock contention beyond the deadline. The scheduling hook pauses one writer at the real persistence boundary while it holds the lock; it does not change licensing source, signatures, dates on the host, state bytes or the lock timeout. A process suspended or stalled for longer than that deadline is the realistic interleaving represented by the probe; its frequency was not measured.

Evidence: `process-control-output/posix-process-replay.json`, process-control.log and the external probe script. A separate thread-level source reproduction independently showed the same result after 10.001 seconds. This is within B56-W05’s requested concurrency/persistence scope; no other release finding was revisited.

**Narrow recommendation, no implementation performed:** do not perform a state read/modify/write without acquiring its serialization lock, and do not claim durable expiry after persistence failed. Ensure the expired observation can be merged durably without an older writer erasing it. Add a real lock-holder-beyond-deadline process regression using Windows locking and DPAPI before closing the issue.

## Exact Windows follow-up

The bundle includes **windows_verify_B56_W05.py**. Save/extract the bundle outside the Workbench source and package, then run the command in README_WINDOWS.md. It requires native Windows and Python 3.12, refuses source fallback, and pins both imported extension SHA-256 values to the actual package hashes above.

It uses isolated temporary application-data/state/license files, generated ephemeral test keys and simulated dates. It never changes the OS clock or installs a real license. It exercises restart, reimport, renewal, original-license denial, concurrent processes with DPAPI, and the real held-lock timeout. It records loaded module origins for parent/child processes. It also reruns both requested pytest files with the same package PYDs preloaded in pytest and its restarted/concurrent child interpreters. Only the repository-only test is deselected there, because it has already independently passed from the verified Git checkout; Git is therefore not required for the user’s native extension follow-up.

This helper tests **compiled extensions in a Python test host**, not the frozen customer executable or its embedded trust. It has been syntax-checked and its scheduling approach exercised by the Linux process control, but it has **not** been executed on Windows here. The supplied `.pyd`/EXE files remain unchanged.

For an executable-level clock test, use only a disposable Windows VM with the unchanged customer package, existing embedded trust and legitimately production-signed old/renewal test licenses. Preserve the same VM disk/profile/DPAPI state across expiry, reboot and clock rollback; reverting an old disk snapshot would discard the record and test a different scenario. Do not change the real PC’s clock or inject a new trust key. A safe VM procedure and the waiting/exit-code command are included in README_WINDOWS.md; no VM execution is claimed.

## Integrity and disposition

The exact Git checkout remains clean at ed117d8bbf66d7be9e67827831fb33dae2cb7a23. All **5,932 supplied archive files** remain unchanged. Reports, audit probes and isolated test data were kept outside the checkout/package. No source, test, `.pyd`, `.exe`, signed license or release artifact was modified.

**Disposition: keep B56-W05 open.** The normal fix is effective in tested source paths, but the lock-timeout loss of the recorded expiry still reproduces at the verified commit. Return the native helper summary/origin logs if Windows confirmation is wanted; do not treat supplied functional passes or static package presence as an executable-level closure test.
