# v0.9.39 audit evidence

Read the report first. Source ZIP SHA-256 and the final 887-file unchanged comparison are in source-integrity.json. No application source, client project, private signing key or production license is included. Probe projects are disposable synthetic projects; named wells in crosswell-alias-evidence.json are from the application test fixtures.

Six new defects are the report findings. accepted-series-evidence.json and crosswell-alias-evidence.json are passing/non-finding experiments. Do not reinterpret them as extra defects. CPU profiling results are separate from unprofiled elapsed times. The exploratory directory and early blank-default-label runs are not dense-label qualification. map-complete-*.json is the populated-label/250-layer main matrix; map-rich-100000.json waits for deferred layers and includes 125000 line features, five 256x256 grids and a 2048x1024 image. The million-well -unprofiled file is symbol-oriented with blank default well-number posts, not a million-label test. Counters cover the scopes described in the report; zeros are not proof of zero operating-system I/O. Original probe scripts retain audit-machine paths for traceability. Some richer reproduction counters were added for later reuse; only fields actually present in the captured JSON are claimed as measurements.

The original monolithic suite segfaulted; full-tests.log preserves its trace. isolated-tests contains each test file's fresh-process run, not a falsely successful replacement monolithic log. test-summary.json aggregates human pytest summaries and keeps passing subtests separate. The ordinary suite process ran alongside independent performance probes in separate interpreters/displays; pytest itself used no parallel worker mode. Three tk-repeat logs retain the full-collection/single-test diagnostic. The four ordinary failures, if present in the final summary, remain failures; environment/archive explanations do not edit them into passes. The launcher self-test logs show missing-license exit 3 before bodies executed; no license bypass or private key was introduced.

To reproduce the small probes in your own environment (application requirements plus pytest and a working Tk display for --gui):

    python reproduce.py --source /path/to/OandG_Workbench_v0.9.39 --output /tmp/ogw0939-audit
    python reproduce.py --source /path/to/OandG_Workbench_v0.9.39 --output /tmp/ogw0939-audit --gui

Optional --performance --size 100000 runs the labeled Map fixture. Repeat with 250000 and 500000. It can use several GiB of RAM and take minutes. Timings depend on hardware, fonts and system load. No source files are edited by the adapter. On a local desktop leave DISPLAY set for your own environment; Linux headless execution requires arranging a Tk display. Windows/frozen qualification was not performed in this audit.

All client report delivery commits are confined to Software-reviews under the user's explicit GitHub instruction. The application's source remains unchanged.
