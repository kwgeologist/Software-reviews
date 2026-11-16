# v0.9.48 audit evidence

Records are tied to the supplied ZIP SHA-256 in source-integrity.json. All 899 original files were compared to the archive after testing. The application source, compiled extensions/generated C, executable builds, WSD fixture, client projects, licenses, local trust stores and private keys are not included.

Read full-tests.log and full-results.xml together with test-summary.json; separate cohorts overlap and must not be added as unique test totals. failed-tests.json and skipped-tests.json preserve individual outcomes. The source run is not described as all passing.

protection-negative-evidence.json uses synthetic real PyInstaller archives and intentionally placeholder extension files to test checker behavior, not to simulate a runnable product. customer-protected-check.log and owner-archive-evidence.json concern actual built artifacts. The current payload was clean; these negative cases demonstrate future gate blind spots, not a shipped source leak.

The independent equivalence probe ran in separate Python/source and compiled-copy processes; origins and signatures are recorded. Expected exception cases are explicit; valid scientific results also cover every protected scientific module. Exact fixture outputs are bounded evidence, not an exhaustive proof of numerical equivalence.

Reproduction: use a disposable Linux Python 3.12 environment with the application's dependencies, pytest, Cython 3.0.12 and PyInstaller. See environment.json for actual versions. Set PYTHONDONTWRITEBYTECODE=1, writable MPLCONFIGDIR/APPDATA/LOCALAPPDATA, and a working DISPLAY for GUI probes. Absolute audit paths in probes must be adapted to an extracted v0.9.48 and an external output folder; never build inside your authoritative audit tree. probe_equivalence.py takes source root and output JSON as its two arguments. Build a second copy with tools/release/build_cython.py, then run that probe against the copy and compare cases/signatures.

probe_protection.py and probe_wsd_payload.py generate temporary bundles. probe_petro.py and probe_geosteering.py use synthetic data, not client projects. The latter records a real manual-fault fitter call and directly exercises the retained auto-steering self-test. probe_catalog_help.py additionally requires the accepted v0.9.45 source tree for historical comparisons.

Self-test runners reference an isolated legitimate local-owner test workflow created using the existing License Manager self-test, not a licensing bypass. Its private artifacts are deliberately excluded. Frozen customer programs correctly rejected that local trust. A genuinely trusted production/build-test license is still required for licensed frozen customer acceptance.

This cloud Python defaults to an absent clang and uses nonstandard Tcl/Tk 9 libraries. Compilation used CC=gcc LDSHARED='gcc -shared'. The successful owner build supplied its Python lib directory to LD_LIBRARY_PATH during build. Customer rejection launches used that external library path, and are not standalone clean-machine qualification. No Windows executable was run; no claim of Windows release validation is made.

The actual Linux staging trial permitted the pre-existing EULA placeholder. Do not distribute these audit builds. Production legal/security/release gates remain applicable.
