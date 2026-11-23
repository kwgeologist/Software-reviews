# v0.9.70 focused Tk segmentation-fault audit bundle

Start with OandG_Workbench_v0.9.70_Tk_Segfault_Audit.pdf or its Markdown equivalent. All five required deliverables are at the archive root. The evidence directory contains commands, logs, XML, JSON observations, native traces and external diagnostic probes.

The original SIGSEGV / exit139 remains unresolved. Separate wrong-thread Tcl finalization panics were reproduced; do not treat them as the same crash. No application code, existing tests, project dependencies or releases were changed.

SHA256SUMS.json covers every bundled file except itself. Paths in diagnostic scripts describe the audit machine; adapt copies outside the software checkout before reproducing. Full application source and downloaded tool installations are excluded.
