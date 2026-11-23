#!/usr/bin/env bash
# Diagnostic build only, outside Workbench. Requires the downloaded exact CPython
# v3.12.14 Modules sources and extracted external headers described in the report.
set -eu
B=/workspace/audit-v0.9.70-tk-segfault
cc -shared -fPIC -O0 -g \
 -I/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12 \
 -I/opt/codex/runtimes/codex-primary-runtime/dependencies/python/include/python3.12/internal \
 -I"$B/native/root/usr/include/tcl8.6" -I"$B/native/root/usr/include" \
 "$B/tk86-extension/_tkinter.c" -ltk8.6 -ltcl8.6 \
 -o "$B/tk86-extension/_tkinter.cpython-312-x86_64-linux-gnu.so"
