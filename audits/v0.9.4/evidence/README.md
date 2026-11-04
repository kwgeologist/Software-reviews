# O&G Workbench v0.9.4 audit evidence

Reports are read-only findings against the uploaded ZIP SHA-256 in source-integrity.json. No application source or client databases are included. The supplied audit brief is retained for scope.

Full GUI-enabled suite: 1827 passed, 1 failed, 9 skipped, 521 passing subtests, 825.01 seconds. JUnit includes subtests in its aggregate totals. The font failure repeats individually and the Tk environment diagnostic shows font substitution. geo-self-test-application.log contains a separate genuine product self-test failure against the 29-symbol catalog; its source CLI exited 1. Windows was not run.

Probes use temporary synthetic projects and controlled fixture mutations; they do not edit the application. Controlled failures are not claims of observed client incidents. To reproduce on your extracted v0.9.4 source with its included test fixtures:

    PYTHONDONTWRITEBYTECODE=1 python run_probes.py --source /path/to/OandG_Workbench_v0.9.4 --output /tmp/ogw094-audit

Add --gui for editor and live Map probes, requiring a working Tk display. Add --performance for the 112000-well synthetic API-scan probe (uses a temporary database). Dependencies are the application requirements plus pytest; the audit used Python 3.12 and a headless Xorg display. Set DISPLAY appropriately for your system. The adapter rewrites only copied audit probe scripts to use your source/output paths, then executes them in separate processes with bytecode disabled and isolated writable settings/cache folders. The application source stays unchanged. Original scripts retain the audit machine's paths for traceability. source_integrity.py records the original ZIP comparison and its paths must be adapted if rerun against another extraction.

A fault merge probe actually closes/reopens SQLite. The horizon app probe invokes real import code with a stand-in preview/save callback; the save-failure probe binds real save_now and injects a sqlite error. Catalog probes manipulate disposable user settings. Native corruption probes modify only temporary copies of bundled native fixtures. The API completion probe checks identifiers and volumes, not merely row counts.
