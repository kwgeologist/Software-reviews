from pathlib import Path
import csv,json
B=Path('/workspace/audit-v0.9.70-full');O=B/'deliverables';O.mkdir(exist_ok=True)
P=Path('/workspace/audit-v0.9.70-integrity/audit/v0.9.70_project_integrity/OandG_Workbench_v0.9.70_Integrity_Findings.csv')
f=list(csv.DictReader(P.open(encoding='utf-8-sig')))
for r in f:r['original_severity']=r['severity'];r['severity']={'P0':'Critical','P1':'High','P2':'Medium','P3':'Low'}[r['severity']];r['origin']='Recent persistence audit, verified same baseline'
def add(id,severity,title,files,functions,kind,confidence,explanation,repro,expected,actual,regression,fix,recovery,v69='Not introduced by the v0.9.70 Tk-only delta; source path unchanged from v0.9.69.'):
 f.append(dict(id=id,severity=severity,title=title,files=files,functions=functions,kind=kind,confidence=confidence,explanation=explanation,repro=repro,expected=expected,actual=actual,v69=v69,regression=regression,fix=fix,recovery=recovery,original_severity='',origin='Expanded whole-suite audit'))
add('FA-001','High','TVD-to-MD inverse can return a point with a different TVD on an undulating survey',
'ogcore/depth.py:26–44,65–110,126–145; petroworkbench/depth_entry.py:95–107; database.py:4900–4928',
'linear_interpolate; complete_depth_triplet; DepthConverter.to_md; DepthReference.to_md; ProjectDatabase._time_depth_rows',
'Confirmed numerical defect; synthetic independent round-trip/reference check','High',
'Inverse conversion swaps MD/TVD pairs and sorts by TVD, then connects neighbors in that sorted order. For a survey whose TVD falls and rises, those neighbors can belong to unrelated MD segments. The returned MD can fail the forward conversion even when the requested TVD has exactly one valid crossing. Petro typed depth fields and database time-depth/core conversion use this helper; Geosteering has a separate first-crossing implementation.',
'Run probes/numerical_edges.py with (MD,TVD) [(0,0),(1000,1000),(2000,900),(3000,1100)] and request TVD1050.',
'Find an actual crossing in MD order, or refuse/ask for a branch if the inverse is not uniquely supported. A returned MD must map back to TVD1050.',
'The shared converter returns MD2000, whose forward TVD is900. The unique crossing is MD2750, which Geosteering independently returns as2750.0000000000005. This is not merely a choice among two valid roots.',
'Monotonic, plateau, reversed/upward and multiple-turn surveys; unique/multiple/no crossings; MD→TVD→MD where unique; Petro edited TVD/TVDSS fields and stored time-depth/core values. Include datum/unit conversion.',
'Validate inverse monotonicity/branch conditions before accepting edits. Intersect the original MD-ordered segments and use an explicit, documented branch policy; do not silently sort TVD and interpolate unrelated segments. Obtain geological workflow approval for ambiguity handling.',
'Review TVD/TVDSS-entered depths for affected non-monotonic wells; retain original entered values and surveys. Normal forward MD→TVD and monotonic-well results were not shown wrong.')
add('FA-002','High','TVD pay net and gross use incompatible measures on non-monotonic wells',
'ogcore/pay.py:146–167,175–215; ogcore/batch_zones.py (shared pay engine); petroworkbench/pay_picking.py',
'sample_support; summarize; PaySummary.ratio',
'Confirmed numerical/internal-invariant defect; geological treatment of re-crossings needs a decision','High',
'Gross TVD is max(0,TVD(base)-TVD(top)), but net sums absolute TVD differences of sample cells. An undulating interval can therefore have net greater than gross even when every sample is pay. The midpoint cell scheme can also straddle a turn, making the absolute sum depend on sampling. This contradicts the engine documentation that all-pay net equals gross and gives an invalid net/gross quantity for these intervals.',
'Run probes/numerical_edges.py on the FA-001 survey, MD1000–3000 at250-unit sample spacing with every sample pay, PHIE0.2 and SW0.3.',
'A clearly defined supported vertical-thickness measure, or explicit refusal/warning for the unsupported re-crossing geometry; do not silently publish an ordinary N:G above1.',
'Gross TVD100; net TVD275; N:G2.75, while gross/net MD are both2000. Finer sampling can change the accumulated absolute TVD net. No new geological thickness convention was implemented.',
'All-pay and subset-pay vertical/monotonic wells preserve existing values; undulating/upward/flat intervals explicitly handled; sample-phase refinement tests; batch and Petro produce the same documented outcome.',
'Detect non-monotonic TVD within the interval and define supported behavior with geological input. Keep numerator/denominator consistent under that policy; do not hide the issue by clamping N:G to1 or changing formulas broadly.',
'Existing zone/pay outputs for these trajectories may need recalculation after an approved correction. Preserve raw curves, criteria, intervals and survey so results can be reproduced.')
add('FA-003','High','LAS run cache does not account for its NumPy arrays, defeating its memory budget',
'ogcore/lru.py:12–23,28–83; ogcore/curve_store.py:35–36,311–328',
'nbytes_of; BudgetCache; curve_store.run',
'Confirmed resource/scalability defect; measured accounting mismatch','High',
'BudgetCache measures arrays and built-in containers, but assigns arbitrary objects64 bytes. curve_store.run caches a LasFile dataclass containing decoded arrays under the default size function. max_items is None. Thus the nominal256MB budget does not bound the retained LAS-run arrays; visiting many runs can retain gigabytes, even though the individual-curve cache branch is measured properly.',
'Run probes/cache_and_sources.py: import8 independent synthetic LAS runs of10001 samples, decode them through the real curve_store.run API, then compare cache.bytes with unique NumPy array bytes reachable from entries.',
'Cache accounting includes all retained run arrays and evicts old runs according to the advertised budget, with the documented allowance for one oversized current item.',
'8 entries report512 bytes but retain3,840,384 unique NumPy bytes; no evictions, max_bytes268,435,456, max_items=None. No reduced budget or fake LasFile was used. Growth to thousands of visited runs is a source-supported extrapolation, not a measured38,000-file load.',
'Use actual LasFile cache entries with many curves and raw matrices; force a small budget in tests, verify measured eviction and alias/shared-array accounting; exercise repeated wells/projects and check close cleanup without invalidating displayed data.',
'Provide explicit retained-byte sizing for LasFile/other cached dataclasses or a safe per-cache size function; add an item cap if appropriate. Keep lazy loading and existing curve identity/immutability safeguards.',
'No stored curve corruption was demonstrated. Memory exhaustion can terminate a session and expose pending unsaved work; prioritize after close/save protection.')
add('FA-004','High','Raster Digitizer permits closing after its node-state save fails',
'ograster/digitize_ui.py:754–798; ograster/calibrate.py:1341–1366; database.py:3922–3931',
'DigitizeMixin._dig_finish/_dig_store; CalibrationWindow.close/save_and_close; set_raster_digitizing',
'Confirmed UI failure injection using a synthetic image/project','High',
'_dig_store(now=True) catches storage errors and only sets a status message; it returns no failure signal. _dig_finish continues and returns True when there are no already-exported edited curves needing re-export. In particular newly traced unsaved curves rely on node autosave, yet a failed node write does not veto close. The user is told nodes are kept as they go, but closing destroys the only newer draft.',
'Run probes/digitizer_failure.py. Open Digitizer on a synthetic raster, add a new2-node curve, inject sqlite3.OperationalError in DigitizeLink.store, call finish/close and query raster_digitizing.',
'Keep the editor and its nodes on a failed node-state save; allow retry or explicit informed discard before closure.',
'_dig_finish=True; calibration window destroyed; curve.saved=False;2 draft nodes; database digitizing string remains empty. The error exists only in status before the window disappears.',
'New and exported edited curves, manual/auto-traced segments, edges, tracks and overlays; fail node persistence during timer, close, raster Save and Geo project-close. Assert exact JSON survives retry and cancellation retains the draft.',
'Return and propagate node-state save success, retain dirty nodes and refuse close on failure unless discard is explicit. Distinguish node persistence from publishing sampled LAS output.',
'An older digitizing JSON or accepted LAS may survive, but never-committed nodes generally do not after destruction. Do not present re-exporting old sampled curves as recovering the missing trace.')
add('FA-005','Medium','Production EUR per foot is omitted when monthly history is absent',
'ogcore/production.py:349–356,396–398,488–501',
'summarize; _with_eur; _all_summaries',
'Confirmed output omission; metadata-derived metric','High',
'summarize sets EUR and gross_span, then immediately returns for an empty chosen history before _with_eur computes eur_per_ft. _all_summaries explicitly includes wells with EUR/perforations but no production, so such wells are listed yet this metric remains missing. Bubbles or maps requesting the production EUR-per-foot metric omit them despite both inputs being available.',
'Run probes/numerical_edges.py: summarize([],eur=100000,gross_span=1000), compare a one-month control with the same metadata.',
'EUR/perforation span100 per foot is available independently of monthly cumulative production, or a deliberate history requirement is explained consistently.',
'EUR100000 and span1000 are present, eur_per_ft=None; with one synthetic month the same metric is100. Normal BOE/GOR/water-cut reference checks also pass.',
'No rows with EUR+span, missing EUR, missing/zero span, metric_values/all_summaries and Bubble source path. Verify month-dependent quantities remain absent when unavailable.',
'Compute metadata-only derived values before the early return, keeping monthly-history metrics and geological/unit conventions unchanged.',
'No history is overwritten. Existing well attributes can support correct display after a narrow correction; a user-selected explicit EUR/span ratio is a separate source path.')
add('FA-006','Low','Two GUI regression contracts remain dependent on font aliases or exact drag geometry',
 'tests/test_v0969_fonts_audit.py:35–48,63–69; tests/test_correlation.py:291–303,601–635; correlationworkbench/table.py:1199–1215',
 'RendererFonts.pick/check/test_tk_only_font; CorrelationAppTests.test_correlation_box_over_digital_logs_never_pans; mouse; _clamped',
 'Confirmed test failures on Linux; not established as numerical/data-loss defects','High for failures; Medium for exact cause of Correlation width difference',
 'Font tests require the actual family string equal an enumerated Tk alias, although Tk can canonicalize a family alias. The Correlation test requires a six-decimal physical width from a real MouseEvent/capture/viewport path. The latter still fails after the v0.9.69 edge-aware fixture change. These failures need narrower diagnosis and platform-aware assertions, not automatic dismissal or silent tolerance widening.',
 'Review the full-suite XML/logs and isolated-rechecks.log. Repeat the Correlation case and the native-font case on the recorded environment.',
 'Tests distinguish accepted font alias/canonicalization and viewport/pixel behavior from true wrong-font or drag defects; unexpected GUI callbacks are captured.',
 'Font expected avant garde gothic, actual urw gothic l; Correlation expected6.300000000000001, actual6.296937045548732. Correlation repeats alone; native-font isolated result recorded separately. Some logs also contain an invalid-command idle_draw callback warning, which is not treated as proof of a leak without ownership tracing.',
 'Use known equivalence/capability checks for font aliases, record event data/canvas geometry and assert the documented clamp/drag policy at physical-pixel resolution; test no-pan separately; run Windows DPI/font matrix.',
 'Diagnose event coordinates and alias mapping, then make assertions reflect the real contract without concealing visible regressions. Do not change renderer or geological workflows to satisfy a fixture.',
 'These failures alone do not show corrupted geological data. The separate PI-009 geometry non-settling failure remains a Medium operational issue, not merged into this Low test finding.',
 'Related display-dependent tests existed in v0.9.68; current Correlation fixture and Tk font test are v0.9.69 changes. Source inspection supports residual portability issues rather than a new v0.9.70 storage regression.')
add('FA-007','Cleanup','UI palette and ribbon metrics still have parallel definitions despite a shared theme',
 'ogcore/theme.py:14–35,65–143; ogcore/icons.py:105–119,204–248; petroworkbench/constants.py:5–25; correlationworkbench/app.py:30,94–103; xsection/window.py:286–298',
 'theme.apply; icons.icon_style; module ribbon styles and Petro constants',
 'Architectural concern for a later consistency pass; stylistic differences are not defects','High',
 'Shared theme/icons already centralize most common controls. Petro repeats several palette literals; Correlation and Cross Section define separate ribbon colors/font sizes/padding under safely separate style namespaces. This permits drift but is not evidence a full UI rewrite is needed. The consistency requirement can be met by sharing semantic tokens while keeping layouts/renderers independent.',
 'Compare palette/ribbon definitions and icon-consistency.json;35 statically literal icon_button calls were checked against the canonical action map, with zero mismatches in that subset.',
 'A later approved consistency pass uses shared dimensions/palette roles and the same canonical icon for the same action while preserving module-specific layout behavior.',
 'Duplicate colors and varying ribbon metrics exist. No universal icon mismatch was established; dynamic/wrapper calls and every visual state were not exhaustively compared.',
 'Action-to-icon registry assertions plus representative toolbar/dropdown/tab/header/status snapshots at multiple DPI and module-open orders; keep semantic plot colors separate from chrome.',
 'Later consolidate duplicated chrome tokens and reusable ribbon/dropdown treatment incrementally. Keep existing namespaced styles, layouts and independent renderers. No redesign now.',
 'No data-recovery consequence; avoid spending release-risk budget on cosmetic changes before the correctness/save failures.')
add('FA-008','Cleanup','Legacy hand-drawn Map icon module has no tracked runtime callers',
 'ogmap/icons.py:1–79; ogcore/icons.py:1–119',
 'ogmap.icons._draw/image',
 'Confirmed no tracked import/reference found; external integrations not supplied','Medium',
 'ogmap/icons.py implements the older20-pixel hand-drawn navigation icons. Current suite controls use the canonical ogcore icon sheet. Whole-tree import/reference scans found no tracked caller/import of the legacy module. This is a contained superseded implementation, not a reason to merge renderers or remove compatibility code generally.',
 'Inspect static-inventory.json import graph and legacy-icons-reference-scan.json. Search tracked source/scripts/build declarations for ogmap.icons, from ogmap import icons, relative icon imports and literal module loading.',
 'Keep only one supported icon implementation in active use, with explicit compatibility policy if an external caller still needs the old API.',
 'No tracked runtime reference found; only the legacy module itself defines this implementation. The scan cannot rule out an external consumer importing it.',
 'Import/launch/package smoke tests and canonical navigation icon checks after any future removal; verify no external integration contract first.',
 'Document it as dormant/superseded. Remove only after confirming no external API commitment; do not delete it during this audit. Leave other legacy migrations that still have readers/tests alone.',
 'None; the original file remains unchanged.')
order={'Critical':0,'High':1,'Medium':2,'Low':3,'Cleanup':4};f.sort(key=lambda r:(order[r['severity']],r['id']))
(O/'findings.json').write_text(json.dumps(f,indent=2))
fields=list(dict.fromkeys(k for r in f for k in r))
with (O/'OandG_Workbench_v0.9.70_Combined_Findings.csv').open('w',newline='',encoding='utf-8-sig')as h:
 w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(f)
print('Wrote17 findings:2Critical,8High,4Medium,1Low,2Cleanup')
