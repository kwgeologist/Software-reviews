# Reproduction instructions

All commands below are diagnostic. Run in a disposable workspace against the exact clean checkout, never client projects. The included original command.json records are authoritative for this run; absolute paths describe this audit machine and must be adjusted on another host. Existing tests remain unchanged.

## Runtime and directory setup

Set B to the extracted evidence directory's parent corresponding to this audit workspace; C is a verified checkout at `1e0867ff44516b6cf13dfdbf8b8e6391b6fbf4fa`; P is CPython 3.12.14. Use a separate virtual environment with recorded NumPy 2.5.5, Matplotlib 3.11.2, SciPy 1.18.1 and pytest 9.2.0. Do not install into or update the Workbench checkout. Use an owned Xvfb display on Linux.

The supplied drivers retain this machine's paths for audit reproducibility. Edit a COPY outside source to point B/C/P/X and dependency search paths at your environment before use. They are not a portable one-click installer. `evidence/runtime.json` records native versions and hashes. `evidence/setup_native.py` and `more_native.py` record how the debugger/header overlay was obtained. Downloaded tool packages are not project dependencies.

Tk 8.6 was selected with a CPython 3.12 `_tkinter` overlay compiled from exact upstream CPython v3.12.14 source in `evidence/tk86-extension/`. Tk 9 uses the runtime's original extension. Compile against your interpreter headers and matching Tk libraries; do not copy a Linux extension into a Windows package.

Example environment, matching recorded audit paths:

```bash
export B=/workspace/audit-v0.9.70-tk-segfault
export C=/workspace/audit-v0.9.70-integrity/checkout
export P=/workspace/audit-v0.9.56-windows/tooling/bin/python
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export PYTHONPATH="$B/tk86-extension:/workspace/audit-v0.9.68-full/deps:$B/probes"
export DISPLAY=:221
cd "$C"
"$P" -X faulthandler -m pytest -q -p no:cacheprovider tests/test_xsection.py --tb=short -rs
```

Start an Xvfb server for DISPLAY first. For Tk 9 remove only the tk86-extension entry from PYTHONPATH. Print `_tkinter.__file__`, Tcl `info patchlevel` and Tk `package provide Tk` from an actual root; module constants alone do not establish patch versions.

## Exact experiments

`run_experiments.py` records A (three fresh full Cross Section files per Tk version), D (two target cases first/after Seismic/Map/Correlation), and C (eight modules sequentially in one interpreter per version). Each run saves its full command, stdout/stderr, XML and status. `-p tk_observer` adds external observation for designated runs. The first fresh repetition is uninstrumented.

The serial module order is Geo tabs, Map drawing objects, Petro integration, Digitizer UI, Geosteering project, Seismic app, Correlation, then Cross Section. It is a defined GUI workload, not all software tests. Do not use xdist to reproduce this ordering condition.

`run_lifecycle.py` and `probes/lifecycle.py` run 200 normal-close and 200 raw-destroy Cross Section cycles for each Tk version against synthetic test fixtures. Measurements occur every twenty cycles and after explicit owner-thread collection.

`run_minimal.py` covers 200 roots with Tk only and 200 with TkAgg per Tk version. `probes/retention_compare.py`, `ownership_probe.py`, `petro_retention.py` and `referrers_probe.py` implement the historical and current ownership controls. Diagnostic removal of traces affects only disposable probe objects. It must not be copied as a blanket application cleanup routine.

## Controlled native failure, separate from SIGSEGV

With an X display and selected runtime:

```bash
"$P" -X faulthandler "$B/probes/minimal_gc.py" main
"$P" -X faulthandler "$B/probes/minimal_gc.py" worker
"$P" -X faulthandler "$B/probes/minimal_gc.py" auto-worker
```

The main control passes. The worker variants intentionally arrange collection of a destroyed root's artificial cycle off its owner thread. Observed fatal results: Tk 8.6 SIGABRT, Tk 9 SIGILL. These are unsafe negative tests, so run each in its own subprocess. The auto-worker variant enables automatic GC and allocates objects; it does not explicitly invoke worker `gc.collect`.

Native debugger command used, with LD_LIBRARY_PATH pointing to the external debugger library overlay:

```bash
gdb --batch -ex 'set pagination off' -ex 'set debuginfod enabled off' \
  -ex 'set print thread-events off' -ex run \
  -ex 'thread apply all bt 35' -ex 'info sharedlibrary' \
  --args "$P" -X faulthandler "$B/probes/minimal_gc.py" worker
```

For the original SIGSEGV use the same debugger prefix with the exact failing pytest invocation and full preceding test order. Preserve the signal line and native frames, not just Python's final `update` frame. An exit-zero gdb parent can still contain a fatal inferior signal. This audit did not alter kernel core-dump settings.

## Windows follow-up

No Windows executable was tested here. Run in a disposable Windows test environment with synthetic projects and the exact dependency/build inventory. Use the original failing sequence if available, faulthandler and a Windows native debugger or crash dump collector. Record source-test results separately from packaged compiled modules and frozen executable results. The Linux overlay/gdb scripts do not establish Windows behavior.
