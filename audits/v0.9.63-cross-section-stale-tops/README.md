# v0.9.63 — Cross Section stale formation tops

Read-only audit of release/1.0 at **42d8e330cc6013c73cedd1ca4f2cf4bae1cadc01**.

**Confirmed:** Global FM Tops Manager deletion succeeds, but Cross Section keeps deleted names as saved TopStyle objects. The Tops dialog copies old styles and adds current names; Display Manager independently lists section styles. Neither enforces current canonical membership. Save/reopen perpetuates the names.

The actual manager delete method was exercised with all twelve user examples. Only LO and BMB remained as sources, and the definitions, aliases and old-source picks were removed. Both UI data paths still retained all twelve names. Refreshed picks no longer render the deleted tops; stale styles alone do not create geological picks.

- [Read the report](OandG_Workbench_v0.9.63_Cross_Section_Stale_Tops_Audit.md)
- [PDF](OandG_Workbench_v0.9.63_Cross_Section_Stale_Tops_Audit.pdf)
- [Complete report and evidence ZIP](OandG_Workbench_v0.9.63_Cross_Section_Stale_Tops_Audit_Bundle.zip)
- [Structured findings](findings.json)
- [Reproduction evidence](evidence/stale-tops-evidence.json)

Two Medium findings: canonical-membership failure and a separate conditional pending-draft target path. Existing focused suite: **54 passed, 31 skipped**; migration regression: **1 passed**; independent synthetic reproduction completed with exit 0. No Tk display/native Windows UI or client database was available. Method-level list assembly, real database deletion, save/reopen and Matplotlib Agg rendering were exercised; the report explains UI harness limits.

Individual curve hiding already exists in both editors' Scale tabs. Cross Section: Hide this log (kept selected, not drawn). Correlation: Disabled (kept in the template, not drawn). An eye beside each curve is a discoverability enhancement; no UI change was implemented.

All 940 tracked source files remain unchanged. No fixes were implemented. Preserve global definitions as authority and surviving top styles; source merging/deletion or a renderer rewrite is not a remedy for the reproduced stale list.
