from pathlib import Path
import json
B=Path('/workspace/audit-v0.9.72-full');O=B/'deliverables';N='OandG_Workbench_v0.9.72_'
S=json.loads((B/'full-serial/final-summary.json').read_text())
assert S['finished']
counts=S['counts']
rows=[('Collected main tests',S['collected_main_tests']),('Test modules',S['test_modules']),('Passed',counts['passed']),('Failed',counts['failed']),('Skipped',counts['skipped']),('Errors',counts['errors']),('Passed subtests (separate)',counts['subtests_passed']),('Pytest seconds',S.get('pytest_seconds')),('Driver seconds',round(S['seconds'],2)),('Main inferior peak RSS, KiB',S['peak_inferior_RSS_KiB']),('Inferior exit',S['inferior_exit_code_from_gdb']),('gdb exit',S['gdb_exit_code']),('Native signals',', '.join(S['native_signals'])or'None observed')]
table='| Measurement | Result |\n| --- | --- |\n'+'\n'.join('| '+str(k)+' | '+str(v)+' |'for k,v in rows)
p=O/(N+'Audit_Evidence.md');s=p.read_text();marker='## Runtime identity'
addition='## Final full-run reconciliation\n\n'+table+'\n\n'
addition+='The completed main-test count reconciles to collection: '+str(counts['passed']+counts['failed']+counts['skipped']+counts['errors'])+' / '+str(S['collected_main_tests'])+'. Passed subtests are additional records, not additional collected main tests. JUnit suite attributes and any failure cases are preserved in `full-serial/final-summary.json`.\n\n'
addition+='### Full-run skip reasons\n\n'+'\n'.join('- '+line for line in S['skips'])+'\n\n'
addition+='This result does not close the supplied intermittent SIGSEGV. No native crash occurred in this attempt, so no faulting C stack from this run exists. The debugger reports normal process termination; earlier controlled panic traces remain separately labelled historical evidence.\n\n'if not S['native_signals']else'The native stop remains a failed/incomplete qualification; consult the preserved C stack in the native log.\n\n'
addition+=f"The terminal reports {S.get('warning_count')} warnings, retained in the full log. Repeated Pyshp DBF-size warnings also reproduce with Pyshp 3.1.9's own writer/reader without any Workbench import (`probes/pyshp_warning_control.py`, `pyshp-warning-control.json`); the synthetic record reads back correctly. This does not establish Workbench project corruption or qualify other GIS readers. Matplotlib legend warnings and other warning contexts remain in the log. No warning filters were added.\n\n"
addition+='The original reported crash-path test, `tests.test_xsection.PunchListWindowTests::test_settings_hold_from_one_session_to_the_next`, completed successfully in this run; its exact XML result is in the final summary. A single successful recheck is not closure of the intermittent native fault.\n\n'
p.write_text(s.replace(marker,addition+marker))
p=O/(N+'Full_Audit.md');s=p.read_text();marker='Additional isolated audit-built Linux'
addition=f"The main test count reconciles to all {S['collected_main_tests']:,} collected cases. Pytest time: {S.get('pytest_seconds')} s; driver time: {S['seconds']:.2f} s. Peak main-inferior RSS: {S['peak_inferior_RSS_KiB']:,} KiB ({S['peak_inferior_RSS_KiB']/1024/1024:.2f} GiB). This is process high-water memory, not a measured leak. Individual skip reasons are listed in the evidence report.\n\n"
p.write_text(s.replace(marker,addition+marker,1))
print('Added final measurements and skip reconciliation')
