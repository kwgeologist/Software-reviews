# O&G Workbench v0.9.56 — Final Windows Security & Package Audit

17 November 2026 · Read-only · Exact WindowsQualified archive

## 1. Executive Result

**Not ready for release.** Two category A distribution blockers and three category B security/packaging risks were established. The main blockers are the actual bundled Python 3.12.5 runtime below the repository’s declared security floor and incomplete segyio LGPL redistribution materials. They are separate from functional qualification and do not imply that scientific workflows failed.

The actual Windows customer/owner archives were inspected. All 15 intended protected Windows x64 modules are present; no protected source/bytecode was found in those delivered packages by the performed scans. No production private key, customer license or client project was found in the customer payload. The audit input’s encrypted self-test key is outside the customer tree, matches the documented test passphrase and does not match the embedded production public key.

This audit did not rerun general functionality, scientific formulas, FM Tops or Map/grid algorithms. No application source, Windows binary, staged file or license was modified. Only separate audit tools/fixtures and this report were created.

## 2. Baseline Verification

The input is exactly **OandG_Workbench_v0.9.56_WindowsQualified.zip**, downloaded completely from the supplied release. Size: **667,291,569 bytes**. SHA-256: `f377692f7b555e189d30a5d1e5cea45c94ad0d78f9176d798c8e269f0b67d3e1`. ZIP integrity/CRC check passed. It has 6,283 directory/file entries and 5,862 files, including source, build intermediates, staged customer payload, actual Windows customer EXEs/PYDs and the separate owner EXE. Uncompressed size is 926,936,079 bytes.

The source version/changelog identify 0.9.56, `ogcore/userdata.py` and final path handling are present, and all six owned EXEs have PE FileVersion/ProductVersion 0.9.56 and x64 machine type 0x8664. All 15 expected customer extensions are cp312-win_amd64.pyd and x64 PE files with appropriate Python 3.12 imports. The staged five EXEs/15 extensions are byte-identical to the corresponding dist files.

For each of the five customer EXEs, the extracted PYZ code/constants for ogcore.userdata, ogcore.licensing_keys and the ogcore version module match compilation of the supplied source. This independently confirms incorporation of the final user-data implementation and production trust/version constants. It is not a reproducible-build attestation for every native instruction.

The requested source state is associated with **500ba84**. As requested, no .git requirement was imposed: final feature/source/artifact evidence establishes the inspected v0.9.56 baseline. The earlier small source-only v0.9.56 ZIP and canceled Linux trial were not substituted for this archive.

All 5,862 input files were hashed before inspection and checked again afterward. No changes, additions or deletions occurred. Python’s runtime version violation is a release-policy issue within this correctly identified candidate, not a reason to silently switch baseline.

## 3. Release Blockers

### A56-W01 — Actual customer and owner runtimes are below the declared release security floor

**Classification:** A. Release Blocker. **Type:** Security baseline. **Confidence:** High.

**Files/functions:** dist/OandG_Workbench/_internal/python312.dll; dist/Owner Tools/O&G Workbench License Manager.exe; release/manifest.json:222; Build_Windows_EXE.bat:14; tools/release/check_python.py:17.

**Confirmed behavior:** The customer Python DLL identifies itself as 3.12.5. The owner executable embeds the same Python version. The repository requires at least 3.12.16 for a release, but its version check runs only when OGW_RELEASE=1. A successful default qualification build is therefore not proof this gate ran.

**Evidence:** pe-versions.json records the actual PE ProductVersion/FileVersion and architecture; baseline-verification.json records the owner-extracted DLL version and manifest floor. Both runtimes are 3.12.5; all six owned EXEs independently identify as application version 0.9.56.

**Impact/scenario:** This exact payload fails its own declared security baseline. Functional/DPAPI/PDF success does not establish an adequately patched interpreter and bundled standard library. No specific reachable vulnerability or exploit is claimed from the version alone.

**Smallest safe recommendation:** Rebuild using a supported, security-patched Windows Python consistent with an approved release baseline, and run the strict release gate. If the floor itself is inaccurate, reconcile it with current vendor security evidence rather than silently bypassing or lowering it. Recompile the 15 extensions and regenerate both distributions.

**Validation:** Read PE versions from the final customer and embedded owner DLLs, require the approved floor, rerun protected-source/inventory checks and relevant Windows licensed/unlicensed/PDF smoke qualification after rebuilding.

### A56-W02 — segyio’s LGPL redistribution materials are incomplete in the staged payload

**Classification:** A. Release Blocker. **Type:** Redistribution compliance, not a software vulnerability. **Confidence:** High.

**Files/functions:** build/stage/OandG_Workbench_v0.9.56/THIRD_PARTY_NOTICES.txt:4585; release/legal/THIRD_PARTY_NOTICES.txt:4585; tools/release/third_party_notices.py:115; release/OandG_Workbench.spec:29.

**Confirmed behavior:** The installed metadata says segyio 1.9.15; its notice is only the version, LGPL-3.0-or-later label and homepage. No full LGPLv3 text was found in the staged license/text files. GPLv3 text does exist elsewhere in the notices/NumPy licenses. Readable segyio Python files and segyio.cpp are bundled, but not the complete C core/build sources or recipient source/replacement instructions.

**Evidence:** third-party-evidence.json and segyio-layout-evidence.json describe actual files, not just specs. The exact upstream v1.9.15 tag resolves to 2e420216119f0d509ddac1a581cba24d6dbf9186; its License.md is LGPLv3 and incorporates GPLv3. LGPLv3 section 4(b) requires the license documents; section 4(d) addresses replacement/relinking. The supplied native wrapper imports no separate segyio C DLL; the partial C++ file alone is not a complete buildable source package.

**Impact/scenario:** The current materials do not establish compliant commercial conveyance of the LGPL library. A homepage URL does not supply the missing LGPL text or clear corresponding-source access. This does not mean the proprietary Workbench application must be made open source.

**Smallest safe recommendation:** Add the full LGPLv3 text and clear library copyright/license notices and references to the already-present GPLv3 text. Provide exact corresponding library source/build information (including any wheel patches), either with the release or via a maintained equivalent source-access route with explicit directions. Document and test an appropriate compatible-library replacement or relinking route, and preserve the LGPL modification/reverse-engineering rights in the approved EULA.

**Validation:** Inspect the finished installer’s extracted license/source-access materials; build an interface-compatible replacement and demonstrate that the intended Windows package actually uses it. Check the Python/PYZ collection behavior as well as the external _segyio.pyd. Retain hashes/version provenance for the library and source route.

## 4. Material Security / Packaging Risks

### B56-W03 — Source backup names and Windows case variants evade release inspection

**Classification:** B. Material Security / Packaging Risk. **Type:** Confirmed gate gaps; no actual leak found. **Confidence:** High.

**Files/functions:** tools/release/check_protected.py:49; tools/release/inventory.py:61,89,99,111; release/manifest.json prohibited rules.

**Confirmed behavior:** Protected-file recognition depends on the final suffix, so formulas.py.bak is not recognized as protected source. Inventory also uses case-sensitive ownership/name/suffix checks and an exact .py comparison. Uppercase proprietary source, .GIT and project-database suffixes can be accepted.

**Evidence:** inventory-case-evidence.json: an exact copy of current ogcore/formulas.py placed at _internal/ogcore/formulas.py.bak yields no inventory or protected-tree problem. Lowercase owned extra.py is rejected; extra.PY, _internal/OGCORE/userdata.PY, .GIT/config and archive.OGWDB are not. The fixture’s clean baseline passes, and all changes are outside the supplied input.

**Impact/scenario:** A common editor/backup copy or Windows case variation can evade the checks intended to keep proprietary source/development material out of release output. This is a demonstrated checker weakness, not evidence that those files are present in the inspected customer package. Ordinary runtime dependency source is not being classified as a leak.

**Smallest safe recommendation:** Normalize relevant ownership, names and suffix rules for the supported Windows filesystem. Reject normal source-backup variants and independently detect exact protected source copies regardless of an extra backup suffix. Preserve explicit third-party/runtime exceptions.

**Validation:** Add paired lowercase/uppercase and .py.bak cases for protected and other owned code, Git metadata and project files; retain clean actual-package positive controls. Rerun checks against final Windows artifacts after fixes.

### B56-W04 — Relative application-data variables still direct default writes into the working folder

**Classification:** B. Material Security / Packaging Risk. **Type:** Conditional path/privacy risk. **Confidence:** High.

**Files/functions:** ogcore/userdata.py:57; ogcore/licensing.py:418; license_manager/issuer.py:37; other APPDATA-based preference roots.

**Confirmed behavior:** The new APPDATA fallback helper validates an absolute path, but primary LOCALAPPDATA values are accepted merely when nonempty. Owner home and several existing APPDATA consumers likewise accept a relative value. LOCALAPPDATA=. and APPDATA=. resolve under the current directory.

**Evidence:** security-boundaries-evidence.json: with those relative variables in a temporary working directory, write_preference succeeds there, licensing state resolves there and issuer.home resolves there. The probe does not write a signing key or alter the host clock. The actual userdata bytecode/constants match current source in all five packaged EXEs.

**Impact/scenario:** A wrapper or misconfigured session using relative variables can put preferences/state into a project or executable working folder, contradicting the documented never-working-folder guarantee. If owner key setup is invoked in that configuration, its encrypted-key destination follows that misplaced root. This requires nonstandard environment configuration; no privilege escalation or actual production-key leak was demonstrated.

**Smallest safe recommendation:** Validate primary default application-data roots as absolute, using the same normalization as the existing fallback. On invalid roots, continue to the intended valid home/absolute fallback or raise the clear location error. Apply consistently to owner default storage; preserve deliberate explicit override semantics.

**Validation:** Test absolute, blank, whitespace and relative roots with and without a usable home; run from project/executable CWDs and assert no default files appear there. Repeat stripped-environment Windows startup and per-user license/owner storage checks.

### B56-W05 — Expired launches do not advance the rollback watermark

**Classification:** B. Material Security / Packaging Risk. **Type:** Confirmed intentional security limitation. **Confidence:** High.

**Files/functions:** ogcore/licensing.py:605–621; tests/test_licensing.py Clock tests.

**Confirmed behavior:** Clock state records only successful valid checks and caps time at expiry; an expired check does not advance it. Restoring the OS clock to the last valid time can make the same license valid again without changing state or signatures. Current tests intentionally preserve that capped-watermark behavior.

**Evidence:** security-boundaries-evidence.json uses a genuinely signed synthetic evaluation and the unmodified source check path with an explicitly supplied test key: valid at Nov 6, expired at Nov 21, then valid again at Nov 6; the watermark remains Nov 6. No host clock was actually changed, no state was deleted, and no test key was inserted into shipped trust.

**Impact/scenario:** A customer who controls the machine clock can replay a valid date after an observed expiry. This is a practical limitation of the current offline expiry/rollback policy, not a signature forgery, production-key compromise or OGW_BUILD_TEST_LICENSE bypass. Locked-down users without clock control are outside this scenario.

**Smallest safe recommendation:** Before relying on strict evaluation/time limits, explicitly accept this threat-model limitation or harden how authenticated expired observations affect the watermark, with a safe recovery policy for an accidentally fast clock. Do not promise tamper-proof time enforcement from local DPAPI alone or add a new licensing architecture during this audit.

**Validation:** Add valid→expired→backward sequences with unchanged state and test accidental forward-clock recovery. Document the separate limitation that a machine administrator can manipulate local time/state; a narrow watermark fix cannot establish trusted external time.

## 5. Actual Windows Package Assessment

Two different trees must be distinguished:

- **dist/OandG_Workbench** is the runnable PyInstaller build: 2,303 files / 250,281,991 bytes. Its inventory lacks the top-level EULA, notices, icon and generated help that staging is designed to add. Do not zip this raw tree as the finished commercial distribution.
- **build/stage/OandG_Workbench_v0.9.56** is the intended installer input: 2,309 files / 250,703,250 bytes. The stage inventory has the required runtime/docs/notices and rejects only the existing placeholder EULA. That gate is working; replacement of the placeholder is a final-distribution validation item.

Both trees were inspected against actual artifacts. The customer tree has all five expected EXEs and all 15 protected extensions. No owner package/modules were found in the customer PYZ module lists. The owner tool is outside it under dist/Owner Tools. The developer tree’s tests, generated C, object files, caches and self-test license/key do not make the qualified audit input itself a customer release package; they were not found in the designated customer payload.

Ordinary dependency source, including segyio Python files/C++ binding source and licensed runtime resources, is not proprietary Workbench leakage. Data collection contains the normal states/counties and registration-model runtime resources; no LAS/SEG-Y/WSD/PPF/client project or user-license files were found in the customer tree. Other release inventory warnings were ordinary third-party build-path strings, not demonstrated credentials or customer data.

## 6. Protected-Code Assessment

Exactly the intended 15 protected implementations are represented by Windows x64 extensions: ogcore.licensing, ogcore.license_runtime, ogcore.formulas, ogcore.multimineral, ogcore.multivariate, ogcore.core_equations, ogcore.water, petroworkbench.curve_ops, ogcore.pay, ogcore.batch_zones, ogcore.gridders, ogcore.gridding, ogcore.mincurv, ogcore.velocity_model and ogvol.engine. Names, PE architecture, Python imports and hashes are recorded in actual-package-assessment.json. Their usability is supported by the supplied Windows qualification; this Linux inspection cannot itself load or execute Windows PYDs.

The actual customer CArchives/PYZs and loose/nested archive tree were checked. No protected Python/PYX/PXD/generated C/C++/PYC/PYO implementation was found. The actual owner executable’s check also returned 0 and confirmed its compiled licensing core. The regular customer command initially selected extensionless Linux program names on this host and reported those missing; the audit then explicitly inspected the actual .exe paths through the checker’s same executable/tree routines and verified the 15 PYDs independently. The host naming mismatch is not a Windows package defect.

Fresh real CArchive/PYZ negative fixtures caught all 27 tested source-suffix/path-depth combinations and ordinary nested/type x/case-varied archive cases. Current oversized-entry tests passed. The prior oversized magic-only entry problem is corrected in this baseline. Unreadable/deep recognized archives fail closed in the performed cases.

However, **B56-W03** shows that a practical exact source-backup copy can evade both checkers. Therefore the actual inspected package is clear of demonstrated protected leakage, but the strengthened script is not sufficient as a universal final release guarantee. Add the backup/case controls and retain independent final-artifact inspection. Compiled native implementation is not a promise of immunity to determined reverse engineering; no such guarantee is needed to establish absence of readable source copies here.

## 7. Licensing / Key-Security Assessment

Signature verification uses the exact signed payload, validates the envelope/schema/claims and rejects unknown keys before accepting entitlements. Production trust in all five packaged PYZs matches the source public-key module and includes only the embedded production key ID ogw-2026-01; no ogw-selftest key was added there. Source code permits local owner public trust only outside frozen/_MEIPASS execution. Tests of that separation passed; a customer possessing an unrelated signing key or the self-test key cannot thereby issue a license trusted by this frozen customer.

OGW_LICENSE_FILE selects a candidate file; it does not select a trusted signing key or disable verification. A malformed/unknown-key/invalid-signature file is rejected. OGW_BUILD_TEST_LICENSE is provisioning input for a normal production-signed license, verified against embedded keys, installed in the build user’s license folder and removed via the build marker. It is not a customer self-test bypass or an embedded private key. The license_manager signing interface is not in the customer PYZ.

The supplied Windows owner self-test report identifies 0.9.56/cryptography 50.0.2 and PASSED, including encrypted key creation, owner license import and local trust behavior. The included build key is specifically ogw-selftest-01 with a public self-test passphrase. It is not a production secret and was found only under build/owner_check. Its public fingerprint differs from production trust. No production private key or active customer license was located in the designated customer tree.

This audit ran only focused security/path/protection unit checks on the supplied source: **69 passed, 6 skipped, 12 passing subtests**. The six skips are Linux limitations/GUI-dependent cases, including DPAPI; they do not negate the supplied Windows DPAPI pass. Test logs/XML specify each skip. The current runtime recovery/save/export exceptions preserve existing work intentionally and are not being called a licensing vulnerability.

There remain two qualifications: relative default application-data roots violate the no-CWD guarantee under nonstandard environment configuration (B56-W04), and the intentionally modest wall-clock policy permits the observed expired→valid replay to a previous valid date (B56-W05). No signature forgery or build/test trust bypass was demonstrated. DPAPI protects stored state confidentiality/integrity in the user scope, not an independent trustworthy clock or resistance to an administrator deleting state.

## 8. Customer vs Owner Package Separation

The separate Owner Tools executable includes issuer/key-setup code by design. The customer’s five PYZ inventories contain no license_manager package or issuer module. Cryptography signing primitives may exist as ordinary library functionality, but they do not confer the missing trusted production private key or authority to issue an accepted Workbench license.

Owner key creation uses encrypted PKCS#8 with a passphrase of at least 12 characters and exclusive creation. Its intended default location is the owner profile; source review found no production private key embedded in either customer or owner. Relative APPDATA handling is the conditional location risk already reported, rather than evidence of a production key actually being written into a customer folder.

The developer qualification archive must stay private and must not be redistributed as the customer ZIP: it intentionally contains proprietary source/build material and a test-key workflow. Only the checked, finalized customer staging tree should feed the commercial installer. No private keys or license bytes are included in this audit’s published evidence.

## 9. Secrets / Sensitive-Material Assessment

The performed scans covered all input files for recognizable private-key blocks and sensitive filenames, the customer loose files and executable bytes, and nested code constants extracted from all five customer PYZs. An additional scan inspected customer/owner CArchive entries, embedded ZIP contents and their PYZ constants; it found no private-key block and no unreadable entry. Independent raw/newline-normalized hash checks against 30 supplied protected source/bytecode/generated-source references also found no exact copied implementation in customer files/ZIP members. The only real private-key PEM block found in the full input was the encrypted self-test key already classified above. No private-key block was found in the customer tree or its extracted PYZ code constants; no customer signing-key/license file or client-data extension candidate was found there. Source review of credential/password assignments identified runtime/user inputs and the documented self-test constant, not a static production API token/password.

Public signing keys, CA certificates in certifi, a public test passphrase and ordinary build directory paths are not secrets. Vendor binaries’ build paths and the supplied D:\OandG_Workbench qualification path are not, by themselves, material customer-data disclosure. The scans are bounded evidence; they are not a guarantee that every arbitrary encrypted/encoded byte sequence is harmless. Final release SBOM/secret inspection must apply to the actual signed installer and extracted contents.

## 10. Third-Party Redistribution Assessment

**Specific segyio conclusion: not yet complete for commercial distribution (A56-W02).** Actual bundled metadata is 1.9.15. The exact upstream tag’s License.md is LGPLv3; its module identifies the Statoil copyright and LGPLv3. The staged package has no full LGPLv3 text in the inspected license/text resources. GPLv3 text is already present elsewhere, so it is inaccurate to say both GPL and LGPL texts are absent. The current segyio notice is only the license label and homepage.

The package includes readable Python wrapper files and segyio.cpp. These are third-party materials, not prohibited proprietary Workbench source. They are not a complete source/build offer for the C library compiled into the extension. PE imports show no separate segyio C DLL. The external _segyio.pyd is a potential compatible-replacement boundary; the 18 segyio PYZ entries and loose Python files mean loader precedence/full-library replacement must be demonstrated rather than inferred from a one-folder layout. Provide complete corresponding library source/access and usable replacement/relinking information without unnecessarily disclosing proprietary application source.

Retain full LGPL text, GPL reference/copy, copyright/notice and source-access directions with the delivered binary, and ensure the approved EULA does not prohibit the LGPL-required modification/reverse-engineering activities. A generic upstream homepage alone is insufficient recipient guidance. A maintained exact source download/build route may be used where permitted; retain version/hash/patch records and ensure it remains available as required by the chosen conveyance route.

Other inspected materials include GPLv3/runtime exception text in NumPy notices, permissive cryptography/PDFium licenses, PSF text within the combined notices and Tcl/Tk license.terms in the actual tree. Certifi’s readable CA bundle and MPL notice are not private signing material. No additional specific redistribution defect was established for those components in the performed review. This is not blanket legal approval of every dependency: reconcile the final Windows SBOM, native components and approved EULA with the exact shipped files, not the old Linux security/inventory records.

## 11. Build / Release Inventory Assessment

Manifest-driven five-program collection, collision refusal, staging extras and separate owner build are real mechanisms. The corresponding stage EXEs/PYDs match dist byte for byte. Normal required/prohibited checks are useful, but B56-W03 proves case/backup gaps. Source rules cannot replace inspection of actual artifacts; here those artifacts were inspected.

The actual strict stage scan reports **one failure: placeholder EULA**. The raw dist scan reports four absent stage extras, which staging is intended to supply. Neither should be misreported as a protected-source leak. The release Python floor check is conditional on OGW_RELEASE=1; the actual DLL versions demonstrate that qualification did not establish that release requirement. Use the strict branch for final production.

The existing native/security/SBOM records are mainly older Linux-trial evidence. They do not attest these exact Windows DLLs, runtime patch level or future installer contents. Refresh records from the final signed payload. Keep generated key/license/self-test folders, collision/inventory reports, manifests and hashes outside customer material unless intentionally allowlisted.

The documented signing helper targets dist, while the installer consumes build/stage and the build script can create an installer before the manual signing steps. Finalize the ordering so the bytes installed are the bytes signed and hashed. The helper also writes SHA256SUMS next to its target; do not accidentally copy an unallowlisted metadata file or use a stale staged snapshot. With no finished installer supplied, these are final distribution validation items below, not a claim that an existing installer was proven wrong.

## 12. Installer Validation Items

**C — A finished installer was not supplied.** Review of the Inno Setup script shows it recursively copies the specified staging folder to Program Files, uses the stage EULA, creates application shortcuts/file association and does not intentionally install projects, owner keys or user licenses. No uninstall rule that deletes user project folders was found. These source observations do not prove a finished installer’s contents.

- Replace/approve the placeholder EULA and require strict inventory with no placeholder exception. Preserve required LGPL rights and third-party materials.
- Sign the actual owned binaries that will be installed, then stage/hash those final bytes (or sign the staged files before the final inventory). Rebuild/sign/timestamp the installer and independently verify Authenticode chains/timestamps and extracted inner EXE hashes. All six supplied owned EXEs have no certificate table; signing is still a finalization item, not a defect in an unfinished qualification build.
- Extract the finished installer and compare its entire file list/hashes with the approved customer inventory. Assert no Owner Tools, build/owner_check keys/licenses, source backups, tests, WSD, projects, logs or unrelated previous artifacts.
- Test install/update/uninstall on a clean Windows user/admin setup, retaining existing projects and per-user licensing/preferences. Validate writable-user locations and actual DPAPI handling without writable Program Files assumptions.
- Generate final Windows SBOM/component versions and current vulnerability/secret scans. Confirm the rebuilt runtime meets the approved security floor, preserve library replacement rights and verify that normal customer trust cannot be changed by owner/test material.
- Distribute only the finished customer installer/payload. The full WindowsQualified audit input is not that payload.

## 13. Remaining Security Validation Gaps

The supplied qualification evidence reports: successful Windows build/Cython/protection checks; owner self-test; all Workbench/project launches; DPAPI and Explorer drop passes; **9 packaged production-license tests passed**; **2,800 full serial source tests passed**. These are useful functional/runtime qualification facts supplied by the user, not security proofs or runs repeated by this audit. The included owner text report corroborates its self-test; no complete signed/hash-bound 9-test/2,800-test report was located and claimed as independent execution evidence.

This audit independently read Windows PE versions/imports/certificate-table presence, actual CArchives/PYZs, source/packaged path/key/version code matches, staging hashes, extension presence, strict inventories and security boundaries. It cannot execute Windows EXEs/PYDs or verify native Windows signature trust/DPAPI from this Linux host. Do not claim a fresh Windows smoke pass here. Focused source security checks passed as reported above; no functional/scientific re-audit was performed.

Close the two blockers and either fix or explicitly accept the bounded category B risks. Then perform the finished-installer checks, exact library replacement/source-access validation and native security-negative tests (unknown/self-test keys through environment paths, invalid/expired/machine-mismatched licenses, owner trust, stripped/relative environments). Preserve results and hashes for the same final artifacts. Passing launch/PDF tests cannot substitute for those checks.

## 14. Final Recommendation

**Stop release.** The current payload must not be distributed as v1.0. Continue targeted v1.0 hardening: first rebuild on an approved patched runtime and complete segyio redistribution materials; then address source/inventory backup/case gaps and relative default data roots. Resolve or explicitly accept the documented local-clock limitation for commercial time-limited/evaluation licensing. Finish signing/EULA/installer/SBOM validation against final bytes.

No scientific, geological, FM Tops or UI redesign is justified by this audit. No application or supplied Windows artifact was changed. Publish only this report and curated evidence, not the source/build ZIP, keys or licenses.
