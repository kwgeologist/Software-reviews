# v0.8.58 audit evidence

No application source or client project data is included. Reports refer to the latest supplied ZIP by SHA-256. `source-integrity.json` compares all 571 archive files after testing.

`full-tests.log` is the complete GUI-enabled pytest run; `full-results.xml` includes passing subtests in its aggregate count. The human result is 1674 passed, 1 failed, 9 skipped, 354 passing subtests. `skipped-tests.json` records why. Font and Rw focused results are separate, not replacements for the full run.

Probes create temporary synthetic databases/assets and never edit application source. They show exact triggers, not incidence in client projects. The PDF failure uses an injected OSError. Source paths and output locations in the original probe scripts match the audit machine. To reproduce elsewhere, use the bundled `run_probes.py` adapter and an extracted v0.8.58 tree:

    python run_probes.py --source /path/to/OandG_Workbench_v0.8.58 --output /tmp/ogw-audit-repro

Run in a disposable environment with the application's requirements plus pytest/reportlab. Python 3.12, NumPy, Matplotlib, Pillow, pyproj, lasio, pyshp and segyio were available during the audit. Set PYTHONDONTWRITEBYTECODE=1 and MPLCONFIGDIR to an external writable folder. Optional `--gui` also runs the font, 112k marker and repeated Rw probes and requires a Tk display; original source-integrity verification is tied to the uploaded archive path and is excluded from this adapter. Read probe files before running. The adapter writes only to the chosen output folder and temporary project folders.

The report's performance numbers cover synthetic markers, not a full client project. Windows installers and the frozen executable test were not executed. A passing Rw repetition does not explain the earlier intermittence.
