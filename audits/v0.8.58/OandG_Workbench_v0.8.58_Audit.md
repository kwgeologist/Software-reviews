# O&G Workbench v0.8.58 — Independent release audit

**Read-only stabilization audit · 3 November 2026 · Uploaded v0.8.58 baseline**

## Release decision

**Do not freeze this build for the first client installer yet.** Reproduced defects remain in canonical-curve isolation/invalidation, scientific input validation and unit boundaries. These warrant small targeted fixes and regression tests, not a suite rewrite or renderer merger. Named repositories, grids, PDF rendering and cross-module services contain substantial useful shared infrastructure.

No application code, schema, algorithms, UI or supplied data were changed. All **571 extracted archive files** remain byte-identical, with no missing or extra source files. The ZIP SHA-256 is `b5b774c349bc734cc573a89cbfe4bdc9b29cf0b9c020d99b0e7d300ff2fbe0a4`.

## Method and limits

The archive contains 416 Python files and 189,286 Python lines, including tests. This was a suite-wide audit using targeted source tracing, the entire available GUI-enabled test suite, analytical reference cases and external synthetic probes. It is not a claim that every line or UI interaction has been exhaustively verified. Priority went to shared scientific/persistence boundaries and the new release features. Instructions in source documents were treated as project context; the user's pasted audit brief governed the work.

Tests ran on Linux/Python 3.12 with a real headless Xorg display, NumPy 2.3.5, Matplotlib 3.10.8, pyproj 3.8.0, lasio 0.32, pyshp 3.1.6, segyio 1.9.15 and pytest 9.2.0. Dependencies, test environments, synthetic fixtures and probes were outside the extracted application tree.

**Full suite: 1,674 passed, 1 failed, 9 skipped; 354 subtests passed; 791.90 seconds.** The XML counts subtests in its totals; do not add its count to pytest's test count. The failure is `tests/test_text_style.py::ControlTests::test_the_common_control_and_tk_fonts`. It fails independently too: Matplotlib can list DejaVu Serif, but this cloud Tk runtime cannot render it and substitutes fixed/normal despite a bold request. This is an environment-dependent font assertion, not evidence of a Windows bold-font defect. Separately, M03 reproduces a real font-cache lifecycle defect.

The nine skips are seven missing real-log raster/autoreg fixtures, the Windows Explorer-drop test, and the opt-in packaged PDF build. No Windows installer or frozen Windows executable was run. No client database, original historical Rw failure trace, large real SEG-Y volume, 38,000-LIC library, or 200-layer mixed project was supplied. Passing synthetic tests cannot certify those workloads.

**Evidence labels:** Confirmed/reproduced means the current code and a controlled probe support the exact behavior stated. Injected I/O failure proves the failure boundary, not that a client has encountered it. Static concerns and unverified release gates are separately identified. Severity expresses potential impact under the stated trigger, not incidence in existing client projects. File references are relative to the uploaded archive root and line numbers refer only to v0.8.58.

## Findings index

| ID | Severity | Finding |
| --- | --- | --- |
| R01 | RELEASE BLOCKER | Petro working edits mutate the shared canonical-run cache |
| R02 | RELEASE BLOCKER | Deleting an imported curve leaves old values in cached runs and a ghost in rebuilt runs |
| R03 | RELEASE BLOCKER | Curve depth cache omits the well-unit dependency |
| R04 | RELEASE BLOCKER | Volumetrics validation differs by mode and admits impossible or non-finite results |
| R05 | RELEASE BLOCKER | Directional survey imports discard explicit depth units |
| R06 | RELEASE BLOCKER | Seismic synthetic input units are still inferred from magnitude |
| H01 | HIGH | Calculated curve IDs change on every Petro-state save and immediately break provenance |
| H02 | HIGH | Canonical curve updates accept arrays that do not match the depth axis |
| H03 | HIGH | Unsafe named-repository paths escape through the placeholder fallback |
| H04 | HIGH | Gridded volumetrics integrates invalid crossed polygon boundaries |
| H05 | HIGH | PDF raster publication overwrites the image before sidecar success |
| M01 | MEDIUM | Short seismic synthetics have mismatched time and trace lengths |
| M02 | MEDIUM | Affine georeferencing accepts a singular map transform with near-zero RMS |
| M03 | MEDIUM | Tk font cache survives root destruction and reuses a dead interpreter |
| L01 | LOW | Raster overlay still infers a percent-like display range from magnitude |

## RELEASE BLOCKER

### R01 — Petro working edits mutate the shared canonical-run cache

**Severity:** RELEASE BLOCKER

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** petroworkbench/well_data.py:112–130; petroworkbench/geo_link.py:148–157; ogcore/curve_store.py:255–272

**Function/class:** WellData.from_run / curve_store.run

**Current behavior:** from_run assigns the cached LasFile depth, curves dictionary, units and descriptions directly to WellData. run returns the same mutable object to subsequent callers.

**Why it matters:** Readers can obtain different scientific values from the same canonical curve depending on whether they request a run or an individual curve. A working edit can become visible before database publication; reload order then affects the answer.

**Reproduction / realistic failure:** Import GR=[1,2,3]. Build WellData.from_run(curve_store.run(...)). Set working GR[0]=99. Another run reader returns 99, while curve_store.read returns the committed value 1. No database save occurs in the probe.

**Recommended minimal fix:** Give the editable Petro workspace its own dictionaries and arrays, and define cached runs as immutable snapshots or return defensive copies. Preserve explicit canonical publication and revision notification.

**Regression test:** Edit a Petro working curve with two readers open; assert all committed readers remain unchanged until save, all agree after save, and discard/reload restores the database values.

**Evidence:** curve-boundaries-evidence.json: mutable_run; probes/curve_boundaries.py


### R02 — Deleting an imported curve leaves old values in cached runs and a ghost in rebuilt runs

**Severity:** RELEASE BLOCKER

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/curve_store.py:255–278,406–423; database.py:3839–3884

**Function/class:** curve_store.run / delete_curve / ProjectDatabase.las_run

**Current behavior:** The run stamp uses the axis timestamp and MAX(curve.modified_at). Deleting a non-latest curve need not change either. Fresh reconstruction retains the original header width/names even when a curve row is gone.

**Why it matters:** A deleted log can remain scientifically usable with its former samples in a warm cache. After cache eviction it changes to an all-NaN ghost instead of disappearing. Canonical list/resolve and run consumers disagree.

**Reproduction / realistic failure:** Prime a run containing GR and RT, delete GR through delete_curve, then resolve GR and read the run. resolve returns none; the cached run still contains [1,2,3]. Direct database reconstruction still lists GR, now all NaN.

**Recommended minimal fix:** Advance a run revision on every membership/edit operation, invalidate affected run snapshots, and rebuild the run header/column list from surviving canonical rows rather than the original inventory.

**Regression test:** Prime and unprime readers; delete first/middle/latest/all curves; verify identical surviving names, metadata and values before and after close/reopen. Include LAS export and Petro consumers.

**Evidence:** curves-evidence.json: delete_run_cache; curve-boundaries-evidence.json: delete


### R03 — Curve depth cache omits the well-unit dependency

**Severity:** RELEASE BLOCKER

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/curve_store.py:197–234; database.py:1700–1769,2492–2497

**Function/class:** curve_store.arrays / ProjectDatabase.update_well

**Current behavior:** arrays returns depth converted to the current well depth unit but caches it using only project path, curve ID and curve timestamp. Updating the well unit does not change that cache key.

**Why it matters:** Scientific consumers can receive feet-valued depths while the well is now in metres. This changes zone alignment, interpolation and depth-based integration until a cache clear, even when the underlying curve is unchanged.

**Reproduction / realistic failure:** Read a feet-axis curve at [100,101,102], change elevation_units to m, read again: [100,101,102]. Clear the curve cache and read: [30.48,30.7848,31.0896]. The same committed database state yields two different axes.

**Recommended minimal fix:** Include axis revision and target well unit in cache identity, or explicitly invalidate on those changes. Fetch current record metadata when a previously held CurveRecord is used.

**Regression test:** Exercise feet↔metres with warm/cold caches and separate database connections; compare every consumer to explicit conversion without requiring a manual forget call.

**Evidence:** curves-evidence.json: well_unit_cache; probes/curves.py


### R04 — Volumetrics validation differs by mode and admits impossible or non-finite results

**Severity:** RELEASE BLOCKER

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogvol/engine.py:267–310,366–398,511–582,585–594

**Function/class:** _derive / _integrate / _uniform_totals / _check_fraction

**Current behavior:** Only Manual calls _check_fraction. Polygon/Grid accept porosity=35 v/v. Uniform calculations accept negative net pay, and the FVF test fvf<=0 does not reject NaN.

**Why it matters:** A common percent-entry mistake produces a plausible-looking but 175-times inflated oil volume in mapped modes. Negative thickness produces negative reserves; NaN Bo produces a NaN report instead of refusing the calculation.

**Reproduction / realistic failure:** With A=150 acres,h=65 ft,Sw=.25,Bo=1.2: Polygon porosity=35 v/v returns 1,654,635,937.5 STB instead of rejecting it. Manual correctly rejects that fraction, but h=-65 returns -9,455,062.5 STB and Bo=NaN returns NaN.

**Recommended minimal fix:** Use shared finite/range validation at the active-input boundary for all modes: fractions 0–1, physical thickness policy explicit, positive finite active FVF. Flag invalid grid cells with counts or reject the calculation under an explicit policy; do not guess percent conversion.

**Regression test:** Run the same invalid cases through all three modes and UI/scenario loading: NaN/Inf, negative thickness, phi/Sw/NTG outside 0–1, zero/negative FVF, explicit % controls, and valid boundary values.

**Evidence:** volumetrics-evidence.json; probes/volumetrics.py


### R05 — Directional survey imports discard explicit depth units

**Severity:** RELEASE BLOCKER

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/survey_files.py:149–200; database.py:3915–3948,4000 onward

**Function/class:** read_surveys / import_directional_survey / store_survey

**Current behavior:** The survey reader skips a units row as nonnumeric and Survey carries no source-unit field. Imported station numbers are stored in the well depth system without conversion or a mismatch check.

**Why it matters:** A metric survey can silently be interpreted in feet, changing MD/TVD, BHL offsets and subsequent geological positioning. The angles and minimum-curvature algorithm can be correct while the physical trajectory is wrong.

**Reproduction / realistic failure:** Import MD,Inc,Azi with an explicit (m),(deg),(deg) row and stations 0 and 100 into a feet well. The stored final MD/TVD are 100 ft; the file specifies 100 m, equivalent to 328.0839895 ft.

**Recommended minimal fix:** Carry explicit source length units through parsing and convert all length columns to the well unit before storage; where the file is ambiguous require an explicit import choice or reject rather than infer magnitude.

**Regression test:** Single-well and bulk imports for metre/feet/US-survey-foot sources, both angular and positional station formats, including mismatched and absent units and transaction rollback on rejection.

**Evidence:** survey-evidence.json: metric_survey_to_feet_well; probes/surveys.py


### R06 — Seismic synthetic input units are still inferred from magnitude

**Severity:** RELEASE BLOCKER

**Classification:** Confirmed code behavior — violates explicit-unit requirement

**Confidence:** High

**Files:** ogcore/synthetic.py:24–44; seismicworkbench/synthetic.py:170–184; tests/test_synthetic.py:16–22

**Function/class:** slowness_us_per_ft / density_gcc / SyntheticWindow.compute

**Current behavior:** Unknown-unit sonic values are divided by feet-per-metre when their median exceeds 250. Density is divided by 1000 when its median exceeds 100, even if the provided unit explicitly says g/cc.

**Why it matters:** This is a live scientific unit transformation based on data magnitude. Bad or ambiguously labelled values become seemingly valid impedance inputs; output timing and amplitudes can change silently. It is distinct from percent scaling and from display-only range selection.

**Reproduction / realistic failure:** density_gcc([2500], "g/cc") returns [2.5]. slowness_us_per_ft([328.084], "") guesses metres and returns about 100 us/ft. The existing sonic test explicitly encodes the latter guess.

**Recommended minimal fix:** Honor recognized explicit units and reject invalid values in those units. For absent/unknown units, request a source-unit choice with provenance; remove the magnitude fallback and revise the legacy expectation test.

**Regression test:** Explicit g/cc must never trigger kg/m³ conversion; test absent/unknown units, explicit kg/m³ and us/m conversions, bad ranges, and the UI path into a synthetic.

**Evidence:** geometry-assets-evidence.json: synthetic_density_explicit_gcc; tests/test_synthetic.py:18


## HIGH

### H01 — Calculated curve IDs change on every Petro-state save and immediately break provenance

**Severity:** HIGH

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** database.py:4341–4394; ogcore/curve_store.py:425 onward

**Function/class:** save_petro_state / derive_curve

**Current behavior:** Saving calculated curves deletes every calc row for the well, then inserts replacements with new AUTOINCREMENT IDs. The shared CurveRecord contract describes IDs as stable; derived provenance stores parent IDs.

**Why it matters:** Deriving B from calculated A can invalidate the parent identity during the very save that creates B. Held record IDs and provenance become stale even though A was not deleted by the user.

**Reproduction / realistic failure:** Create calculated A (ID 3), derive B. A now has ID 4, get(3) returns none, and B.parents still contains [3].

**Recommended minimal fix:** Update existing calculated rows in place keyed by their stable identity; insert only new curves and delete only intentionally removed curves. Preserve IDs across metadata-only workspace saves.

**Regression test:** Derive from a calculated parent, save/reopen, rename/edit a sibling, and assert parent IDs still resolve and all provenance links remain valid.

**Evidence:** curves-evidence.json: stable_identity


### H02 — Canonical curve updates accept arrays that do not match the depth axis

**Severity:** HIGH

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/curve_store.py:327–404,217–223

**Function/class:** update_curve / arrays

**Current behavior:** Imported curve updates store arbitrary-length values without checking their axis length. arrays later detects the mismatch and returns none.

**Why it matters:** A successful update can make a previously usable scientific curve disappear from canonical readers. The invalid payload is durable; the old values are overwritten rather than rejected.

**Reproduction / realistic failure:** Import a three-sample RT curve; update it with [8,9]. Two samples are committed against a three-sample axis and curve_store.read returns none.

**Recommended minimal fix:** Validate dimensionality and axis length before entering the write transaction; reject mismatched replacements while retaining old data. Keep sample/range metadata consistent.

**Regression test:** Reject short, long, scalar and multidimensional replacements with byte-identical old data; permit a valid aligned update and verify across reopen and all reader paths.

**Evidence:** curve-boundaries-evidence.json: length_mismatch


### H03 — Unsafe named-repository paths escape through the placeholder fallback

**Severity:** HIGH

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/repositories.py:264–310; database.py:2248–2257

**Function/class:** resolve / placeholder / ProjectDatabase.resolve_path

**Current behavior:** The resolver correctly returns Unsafe repository path with path=None for an absolute relative component. placeholder then appends the raw component to a Path; an absolute component discards the placeholder prefix.

**Why it matters:** A rejected repository reference can still resolve to a real file outside its repository through the suite-wide database adapter. This defeats asset containment. The probe establishes read access; arbitrary execution or destructive deletion is not established.

**Reproduction / realistic failure:** Create a harmless temporary outside.txt and resolve @repository/TEST//tmp/.../outside.txt. Repository status is Unsafe, but db.resolve_path returns that absolute fixture and it is readable, even without a configured root.

**Recommended minimal fix:** Do not turn an unsafe resolution into a filesystem path. Return a typed missing/unsafe result or raise at the adapter; if compatibility requires a placeholder, construct it only from sanitized display text and never concatenate untrusted path components.

**Regression test:** Exercise the database adapter and actual grid/raster/seismic loaders, not only repositories.resolve, with POSIX absolutes, Windows drives/UNC paths, traversal and symlink escapes. None may open an outside sentinel.

**Evidence:** repository-evidence.json; probes/repository.py


### H04 — Gridded volumetrics integrates invalid crossed polygon boundaries

**Severity:** HIGH

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogvol/scenarios.py:189–244; ogvol/engine.py:366–384,616–625

**Function/class:** scenarios.resolve / _integrate / _constant_case

**Current behavior:** The constants-only polygon route checks polygon_stats validity. The gridded route sends the same boundary coordinates directly to point-in-polygon testing without validating the ring.

**Why it matters:** A self-crossing outline has no unambiguous reservoir interior, yet one mode reports volumes while the other refuses it. An edited saved boundary can silently alter included cells.

**Reproduction / realistic failure:** Use a 3×3 constant net-pay grid with the bow-tie boundary [(0,0),(200,200),(0,200),(200,0)]. Grid mode accepts it, includes two cells and reports 28,941.1157 STB.

**Recommended minimal fix:** Validate boundary and compartment drawings using the shared geometry rules before integration, including closed-state checks at scenario resolution; refuse ambiguous geometry with its reason.

**Regression test:** Crossed, open, degenerate and non-finite outlines in both constant and gridded Polygon/Grid modes, including editing a previously valid stored drawing.

**Evidence:** geometry-assets-evidence.json: crossed_grid_boundary


### H05 — PDF raster publication overwrites the image before sidecar success

**Severity:** HIGH

**Classification:** Confirmed failure-handling defect — reproduced with injected I/O failure

**Confidence:** High

**Files:** ograster/pdf_import.py:371–389; ograster/pdf_import_ui.py:374

**Function/class:** Layout.write / PDF import completion

**Current behavior:** write saves directly to the final TIFF path, then writes the provenance sidecar. There is no staged publication or rollback across those operations.

**Why it matters:** If the sidecar write fails, the import raises after replacing an existing image. A preexisting sidecar can describe old content and the UI does not complete registration. Interruption during TIFF encoding also risks a partial destination.

**Reproduction / realistic failure:** Place previous bytes at an existing .tif target. Inject an OSError only at sidecar write_text. write raises, but previous bytes are gone and a new TIFF exists without its sidecar.

**Recommended minimal fix:** Stage the TIFF and JSON separately, validate them, and use the existing safeio publication/rollback service before registration. Preserve both previous outputs on failure.

**Regression test:** Failure injection at encoding, sidecar writing, promotion and registration boundaries, verifying old asset/provenance bytes and DB references remain coherent.

**Evidence:** geometry-assets-evidence.json: pdf_partial_write


## MEDIUM

### M01 — Short seismic synthetics have mismatched time and trace lengths

**Severity:** MEDIUM

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/synthetic.py:148–178,180–198; seismicworkbench/synthetic.py:200–230

**Function/class:** make_synthetic / correlate

**Current behavior:** np.convolve(rc,w,mode="same") returns max(len(rc),len(w)), not necessarily the number of time samples. The time axis remains n samples.

**Why it matters:** Short valid log intervals can fail interpolation or plotting, making a synthetic unavailable for that interval. This is a shape defect rather than a demonstrated wrong geological formula.

**Reproduction / realistic failure:** Ten time samples with default 128 ms wavelet and 1 ms sampling produce len(time)=10 and len(trace)=129. correlate uses those as xp/fp of np.interp.

**Recommended minimal fix:** Center the full convolution onto exactly the intended time-axis length, preserving alignment and polarity. Keep time/impedance/RC/trace shapes equal.

**Regression test:** Intervals shorter than, equal to and longer than the wavelet, odd/even lengths, an impulse with a hand-known peak location, and synthetic-window plotting/correlation.

**Evidence:** science-evidence.json: short_synthetic


### M02 — Affine georeferencing accepts a singular map transform with near-zero RMS

**Severity:** MEDIUM

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogmap/georef.py:104–158,166–176

**Function/class:** fit / inverse

**Current behavior:** Affine fitting rejects collinear image control points but does not reject a singular fitted 2×2 map transform. inverse detects a zero determinant only later.

**Why it matters:** Collinear map control points can appear to fit perfectly while collapsing the raster onto a line; the reported RMS is misleading as a usability check.

**Reproduction / realistic failure:** Image controls (0,0),(1,0),(0,1) mapped to (0,0),(1,0),(2,0) produce determinant 0 and RMS approximately 5.8e-16.

**Recommended minimal fix:** Validate finite coefficients, nondegenerate map controls and a scale-aware determinant/condition threshold before returning an accepted Fit. Report why the transform cannot be used.

**Regression test:** Collinear map points, identical map points, near-singular controls, valid reflected/rotated/sheared affine transforms, and disabled-point behavior.

**Evidence:** geometry-assets-evidence.json: singular_georef


### M03 — Tk font cache survives root destruction and reuses a dead interpreter

**Severity:** MEDIUM

**Classification:** Confirmed defect — reproduced

**Confidence:** High

**Files:** ogcore/text_style.py:190–211

**Function/class:** tk_font / _TK_FONTS

**Current behavior:** The process-wide cache key uses str(root), often simply ".". A new Tk interpreter with that same name receives the old Font object, which retains its old Tcl interpreter.

**Why it matters:** Repeated root creation in tests/embedding can return an unusable font and retain dead roots. Normal Toplevel windows sharing one live root do not establish the same failure.

**Reproduction / realistic failure:** Create root A, cache a font, destroy A, create root B and request the same style. The same object is returned and actual() raises application has been destroyed.

**Recommended minimal fix:** Scope fonts by interpreter/root identity with lifecycle cleanup (prefer a per-root cache); avoid strong global retention of destroyed roots.

**Regression test:** Destroy/recreate two roots with the same Tk pathname and prove the returned font belongs to the new interpreter and old cached roots can be released.

**Evidence:** font-evidence.json: recreated_root_returns_old_font/recreated_root_error


## LOW

### L01 — Raster overlay still infers a percent-like display range from magnitude

**Severity:** LOW

**Classification:** Confirmed display-only heuristic — static inspection

**Confidence:** High

**Files:** ograster/overlay.py:227–247

**Function/class:** default_scale

**Current behavior:** Neutron/density-porosity overlay limits are multiplied by 100 when the maximum exceeds 1.5, as well as for explicit percent/pu units.

**Why it matters:** This can choose a misleading visual range for outliers or unusual curves. It changes limits, not scientific samples, and is not equivalent to a scientific percent-conversion defect.

**Reproduction / realistic failure:** Supply a decimal-family choice with maximum above 1.5 and no percent unit; default limits switch to the percent-style range.

**Recommended minimal fix:** Use explicit units and saved/user-selected scale for display defaults; preserve stored samples and user track settings.

**Regression test:** Decimal curves with large outliers and low-magnitude percent curves choose limits from metadata/controls, while value arrays remain byte-identical.

**Evidence:** Static source inspection at ograster/overlay.py:245

## Scientific reference results

These checks use analytical expectations rather than previous Workbench output. The mineral check constructs the input mixture independently with hard-coded endpoints rather than calling the production forward model.

| Check | Expected | Observed |
| --- | --- | --- |
| Manual oil: 150 ac × 65 ft | 9,750 acre-ft bulk/net in this direct-net case | 9,750 |
| HCPV: bulk × .20 × (1−.25) | 1,462.5 acre-ft | 1,462.5 |
| OOIP: 7,758 × HCPV / 1.2 | 9,455,062.5 STB | 9,455,062.5 |
| Recoverable at RF=.20 | 1,891,012.5 STB | 1,891,012.5 |
| 2×2 / 3×3 nodes | 1 / 4 cells | 1 / 4 |
| 51×51 nodes, 100-ft spacing | 2,500 cells; 25,000,000 ft² | Matches |
| Rotated 3×4 node grid, 100-ft spacing | 6 cells; 60,000 ft² | 60,000.00000000001 |
| Linear thickness plane, 5–15 ft over 40,000 ft² | 9.18273645546 acre-ft | 9.18273645546 |
| Archie: a=1,Rw=.075,Rt=10,phi=.20,m=n=2 | Sw=.433012701892 | Matches |
| Linear Vsh at GR endpoints 32 and 118 | 0 and 1 | Matches |
| Vertical survey, MD=1,000 | TVD=1,000; N=E=0 | Matches |
| Constant 60° northward survey, 1,000 MD | TVD=500; N=866.025403784 | Matches |
| Raster anchors (1000,100),(2000,1100) | row 600 ↔ depth 1500 | Matches both ways |
| Mineral mixture .50 calcite/.20 dolomite/.15 wet shale/.15 free fluid | VCAL=.50,VDOL=.20,VSH=.15,PHIE=.15 | Within 9e-11; QC=0 |
| Same mixture, shale porosity .12 | PHIT=.15+.15×.12=.168 | .1680000000033 |

The existing volumetrics tests additionally exercise four-corner means, invalid-corner exclusion, centre clipping, fault handling, rotated determinants, constant cases, mode save/reopen and grid export. Those passing cases do not cover the invalid input and invalid polygon cases in R04/H04. No saturation, shale, minimum-curvature or mineral equation change is recommended from the passing reference cases.

## Performance, memory and concurrency assessment

An external MapView probe generated **112,000 synthetic wells**. Initial set_wells plus event processing took 0.257 s; basin refresh 0.326 s; six zoomed refreshes took 0.080–0.091 s. Artist counts stayed **8 lines / 5 collections / 4 texts** across those six pans. Peak process RSS was about **162.6 MiB**, including Tk, Matplotlib and synthetic well objects. These are observations on this cloud machine, not latency promises or a complete session leak test.

This supports keeping the current marker collection/LOD path. It does not establish acceptable behavior for 200 mixed layers, heavy labels, multiple grids, a large shapefile, 38,000 LICs and seismic loaded together. The existing suite contains meaningful large-well, spatial-index, layer-speed, bounded-cache, production-memory and workbook-scaling checks; a timed mixed-workload soak remains a release qualification gap, not a demonstrated application failure.

`ogcore/background.py:77–124,139–175,191–204` uses a separate read-only database connection, generation/stamp checks, UI-thread delivery and close cancellation. Work is serialized through a lock before executing; therefore it is not accurate to claim every pending job simultaneously holds a seismic-sized working array. Cancellation discards obsolete requests/results but cannot interrupt an already executing operation. Add a long-operation/project-switch soak before asserting there are no resource or race issues. No evidence found here justifies replacing the current worker service.

Curve snapshots are byte-budgeted, but a byte budget does not make mutable cached scientific objects safe (R01). The Tk font dictionary retains Font/root references without lifecycle eviction (M03). No broad claim of a long-session Matplotlib, Qt or seismic-cube leak is made from static patterns alone.

## Suite coverage and architectural observations

“Inspected” below means the indicated source boundary and relevant tests were reviewed/executed; it does not mean every module action received manual acceptance testing. A passing test family is supporting evidence, not blanket certification.

| Area | Inspection and evidence | Assessment / remaining work |
| --- | --- | --- |
| Geo / Well Manager / imports | database.py, project services, API uniqueness, well-sheet/import tests, atomic-edit tests | Normalized API14 uniqueness and separate sidetrack identities are exercised; survey unit metadata is a real exception (R05). No speculative API rewrite. |
| Canonical curves / LAS / aliases | curve_store, database LAS/calc persistence, Petro bridge, alias and precedence tests, batch/pay reader entry points | DB-native storage and source-file-independent reads are present. R01–R03 and H01–H02 show important contract breaks. Remaining read_las calls include import, standalone LAS use and legacy migration, so their mere existence is not a defect. |
| Petro / batch / pay | equation AST validation, explicit fraction behavior, integration/canonical tests, sample-support engine | Current DEC is identity; explicit `/100` works. Batch/pay tests cover irregular support and source precedence. Do not reintroduce magnitude conversion. Shared curve-service fixes must be tested across these consumers. |
| Multimineral | model checks, constrained inversion, wet-shale PHIE/PHIT, resolution/QC and tests | Closure and independent mixture check pass. The tests exercise ambiguity, missing samples, limits, provenance and reopen. No evidence warrants changing the inversion model or wet-shale convention. |
| Map bubbles / wells / postings | unified definitions/select/style/combine, marker/LOD, posting normalization, dependency and layer tests | All relevant tests run. Per-item posting supports position, label toggle, decimals, color, size, font/bold/italic; current size handling permits 1 point. No current failure chain demonstrated that warrants reverting unified bubbles or adding a posting dialog. |
| Map layers / images / active grid | layer stack/order/visibility/dependency tests, image geometry, active-target tests | Independent transient marker and user-layer services remain useful. Singular image controls are not refused (M02). No merge of Map/Petro/Correlation/Cross Section/Geosteering renderers is recommended. |
| Polygon statistics / volumetrics | shared ring validation and projected/geodesic units; explicit modes; scenarios.resolve and engine | Polygon statistics have useful validity checks; gridded volume clipping bypasses them (H04). Manual is isolated from stale map objects, but uniform/mapped input validation remains inconsistent (R04). |
| Digitized map → grid | ogmap/digitized.py, ogvol/building.py, normal ProjectGrid save/regrid and end-to-end tests | Current drawing controls feed the standard grid service, with saved source provenance and regeneration tests. No separate replacement grid architecture is needed. |
| Gridding / contours / isopach | Surface geometry, grid files/publication, gridding/contour/isopach/unit tests | Node geometry and cell integration are distinct and reference areas pass. Grid save already stages file/row publication with safeio; use that pattern for the PDF defect rather than replacing it. |
| Raster / Registration / Digitizer / PDF | calibration/cache/export boundaries, PDF Layout/renderer/UI and tests | Source PDFium rendering, 12-page crop/order/align/depth-join, LZW TIFF metadata/sidecar and registration tests pass. Seven real-raster tests lack their external fixtures. PDF output publication is not atomic (H05). |
| Seismic | canonical well curves, synthetic compute, SEG-Y reader/geometry/cache/interpretation tests | Synthetic magnitude units violate the current contract (R06); short interval output shapes fail (M01). Existing SEG-Y tests run, but no client-size cube or frozen Windows runtime was exercised. |
| Geosteering | project/publish/well/display tests and shared canonical/native readers | The suite exercises edits, publish and reopening. Independent renderer is appropriate. Survey-unit errors and shared curve defects can propagate to this module; absence of a direct module failure does not insulate it. |
| Correlation / Cross Section | session, well-list, source, pay, xsection and display persistence tests | Existing integration tests pass. Keep geological workflows and independent rendering; add warm-cache cross-reader assertions when correcting shared curves. |
| Production / core / directional | production import units/summary cache, transaction paths, survey reader/store and tests | Production has explicit input factors and per-foot denominator conversion. Core dataset import is transactional. The minimum-curvature reference passes; source survey unit handling does not. |
| Shared selections / well lists | project_meta selection stamps, ordered IDs, listeners, chunked lookup and tests | Intentional shared IDs avoid a second well inventory. Cross-process propagation is polling/focus based, not instant. API ambiguity probe returned not-found rather than arbitrarily assigning a sidetrack; no wrong-well claim is made. |
| Project save/copy/move / repositories | project.py, DB path adapter, repository resolver/config/identity, asset/folder/cache tests | Project copy preserves external repository ownership and identities; roots remain local. Resolver itself rejects unsafe paths, but its adapter defeats the rejection (H03). |
| Error handling / security | safeio transaction/publication, formulas AST evaluator, path containment and failure probes | The formula evaluator restricts AST nodes, NumPy attributes and builtins; the presence of eval is not proof of arbitrary-code execution. H03 is a concrete local path failure. No credentials/licensing exploit finding is asserted. |
| Suite UI / legacy infrastructure | theme/text-style/icon ownership and UI consistency tests | Shared styling/icon services and a same-action icon test already exist. M03 is a bounded lifecycle issue; the font assertion is environment sensitive. Visual differences alone do not justify redesign or renderer consolidation. |

## Tests: strengths, holes and release qualification

The tests do more than assert that helper functions exist. They cover database round trips, real Tk interactions, Map collections/layer changes, project assets, failure rollback, cross-module curve consumption, numerical planes, source precedence and saved layouts. That investment should be preserved.

The most valuable missing tests are the exact probes in this report, promoted into regression tests after a minimal fix:

1. **Canonical reader agreement:** interleave run/list/read readers, working edits, commit/discard, delete and reopen; do not only re-resolve a newly returned record.
2. **Identity and shape invariants:** derive from a calculated parent, keep stable IDs/provenance, and reject updates of wrong dimensionality/length before any overwrite.
3. **Unit dependency invalidation:** well unit changes under a warm cache and explicit survey-file units through single/bulk UI imports.
4. **Scientific validation by mode:** the same phi/Sw/NTG/thickness/FVF invalid values in Manual, Polygon and Grid. Mode round-trip tests alone do not exercise validity contracts.
5. **Adapter-level asset containment:** existing resolver tests are insufficient when resolve_path later turns unsafe results into usable paths.
6. **Failure-safe PDF publication:** inject errors into the final TIFF/sidecar/registration sequence and verify previous bytes and DB state survive.
7. **Independent numerical boundaries:** short synthetic windows, invalid geometry and singular georeferences, alongside valid analytical cases.
8. **Real release artifact:** build on Windows, run all five frozen applications on a clean machine without Python/Poppler, import the 12-page PDF, save/reopen/register/digitize, and export PDF/SVG. Exercise an unwritable installation directory and writable user/project paths.
9. **Representative soak:** instrument mixed 112k-well/200-layer projects, project switches and well changes; record timings/RSS/artist count/file-handle trends instead of assuming six marker pans establish long-session safety.

`tests/test_curve_store.py:183–201` verifies updated imported IDs, child parent metadata and list deletion, but not cached run membership, calculated-parent identity after derive, or well-unit changes with a warm cache. `tests/test_synthetic.py:18` actively encodes a now-disallowed magnitude-unit guess. Windows PDF build-script assertions inspect commands; they cannot prove those commands created a self-contained DLL set. `tests/test_pdf_packaging.py:145` explicitly gates the artifact build behind OGW_PACKAGING_TEST.

### Rw intermittence: unresolved, not dismissed

The existing Rw UI integration test passed in the full suite and **20/20 same-process repetitions** (29.94 seconds) in a fresh process. The current calculator path reads Tk variables synchronously and calls the water helpers; the shared Background worker is not on that calculation path. The Arps reference is exercised in that test. Neither observation establishes the cause of an earlier reported intermittent failure.

No failing historical trace or reliably failing sequence was available. A race, stale state, test isolation and floating-point/sampling tolerance therefore cannot be ranked as a confirmed cause. Keep this as an open release qualification item: retain the original failing assertion and capture selected notebook tab, root/interpreter identity, variable values, active well/depth unit, generated curve index/TVD, pending callbacks and exact numerical difference at failure. Repeat in the original Windows runner and in suite order. Do not relax a tolerance, add sleeps or delete the assertion merely because these repetitions pass. No speculative Rw code change is recommended.

### Windows packaging: encouraging implementation, unverified artifact

The current Windows build explicitly collects pypdfium2 and pypdfium2_raw/native bindings, includes PDF/SVG backends, merges runtime components and performs self-tests with Python-related environment variables cleared and a restricted PATH. Source launchers check/install dependencies. Source PDF rendering and missing-library diagnostics are covered and ran here.

That supports the design, but **it is not a clean-Windows acceptance result**. The actual frozen package test was skipped, Windows Explorer drops were skipped, and DLL/installer behavior remains unverified. Treat Windows acceptance as a required gate after the code blockers are fixed; do not label a DLL failure as reproduced when none was run.

## Safe to leave alone

- The separate scientific renderers and existing tool workflows: there is no demonstrated reason for a renderer merger or total UI overhaul.
- DB-native curve ownership: correct architectural direction; fix snapshot/invalidation/identity boundaries instead of returning to LAS as the live database.
- Volumetrics node/cell conventions, determinant area and passing manual reference arithmetic.
- The constrained multimineral closure, wet-shale PHIE/PHIT and ambiguity reporting supported by the inspected tests and independent mixture.
- Shared ProjectGrid geometry, staged grid publication, digitized-source provenance and regeneration.
- Map collection/LOD rendering, layer order and transient marker separation supported by the current tests and marker probe.
- Production's explicit conversion factors, core transactional import and API14 uniqueness protections where the relevant tests pass.
- Explicit legacy import/migration/standalone LAS paths: do not delete compatibility code merely because read_las remains searchable.
- Existing shared theme/icon/text-style services. Centralize remaining policy through these services when warranted; visual preferences are not release defects.

No genuinely unreachable application implementation was established strongly enough to recommend deletion in this pass. No changes to scientific formulas, workflows, frameworks or database ownership are proposed for stylistic reasons.

## Top 10 fixes / practical fix order

1. **R01:** isolate Petro edits from canonical cached runs; prove commit/discard reader agreement.
2. **R02:** make run membership and reconstructed headers follow canonical deletion.
3. **R03:** include well/axis unit dependencies in scientific cache invalidation.
4. **R05:** preserve/validate source survey units at every import boundary.
5. **R04:** enforce finite, physical active inputs consistently in all volumetrics modes.
6. **R06:** remove scientific magnitude-unit guessing and its legacy test expectation.
7. **H01 + H02:** preserve calculated IDs/provenance and reject malformed curve replacements before writing.
8. **H03:** enforce repository containment at the suite's filesystem adapter, not only the resolver.
9. **H04:** share polygon validity checks with gridded volumetrics.
10. **H05:** stage PDF image/sidecar publication with rollback.

Make each change narrowly, add its reproducer as a regression and rerun the affected consumers. Then run the full suite, original Rw stress sequence, representative mixed-project soak and clean-Windows artifact acceptance before freezing. M01/M02 are small contained correctness fixes worth completing during stabilization; they do not require architectural changes. Do not combine these corrections with UI redesign or bulk cleanup.

## A. Release Blockers

**R01–R06 should stop an unconditional release freeze:** uncommitted working data leaking into shared canonical reads; deleted curves still usable; unit-dependent stale depth arrays; invalid physical volumetrics reports; ignored survey units; and magnitude-based synthetic unit conversion. Each has a code-supported trigger and evidence. This is not a claim that all existing projects have already suffered these failures.

The clean-Windows installer/runtime check is an additional **unmet release gate**, not a reproduced package defect. Resolve code blockers first, then qualify the actual artifact. The earlier Rw intermittence also remains open until its original failure is understood or bounded with evidence.

## B. Recommended Before Release

Fix H01–H05: stable calculated identities and valid array writes, safe repository adaptation, validated grid clipping and atomic PDF publication. Complete the short-synthetic and singular-georef corrections (M01/M02) where feasible. Add the concrete regression cases and perform Windows and representative-project acceptance. Correct test assumptions about fonts without masking actual style regressions.

## C. Safe to Defer

Defer visual harmonization, further shared-style cleanup and the display-only default-range heuristic (L01) unless an actual user case needs it immediately. M03 can be deferred if the distributed lifecycle strictly uses one Tk interpreter per process, with the test/embedding limitation documented. Keep independent renderers, valid compatibility migrations and passing scientific algorithms intact. Broad dead-code removal, speculative optimizations and a new framework are outside stabilization needs.

## D. Architecture Validation

| System | Rating | Justification |
| --- | --- | --- |
| Canonical DB-native curves | Release blocker | Ownership is correct, but reproduced mutable snapshots, deletion and unit-cache errors violate one-value/one-axis consistency. |
| Project persistence | Mostly sound | Staged grid/project services and round-trip tests support the design, with PDF publication and calculated identities requiring localized repair. |
| Named repositories | Needs work | Identity/local-root separation is sensible, but the unsafe-path placeholder bypass defeats the adapter's containment guarantee. |
| Grid architecture | Mostly sound | Shared node geometry, file publication and cell area checks are sound in tested cases; keep active-input and geometry validation explicit at consumers. |
| Reservoir Volumetrics modes | Release blocker | Explicit modes/manual isolation and reference arithmetic work, but invalid inputs still produce scientific reports and gridded clipping accepts invalid boundaries. |
| Digitized layer → grid | Mostly sound | Current drawing controls use the normal grid pipeline and regeneration tests; no duplicate grid engine replacement is justified. |
| Raster/PDF workflow | Needs work | Source rendering, multi-page joining and registration tests pass, but output publication can destroy an existing raster on failure and real-raster fixtures are incomplete. |
| Map layer architecture | Mostly sound | Shared layers/transient separation and collection rendering have useful coverage; the singular georef case is a contained consumer defect. |
| Cross-module state synchronization | Release blocker | Selection/revision infrastructure exists, but run versus individual-curve readers demonstrably disagree under ordinary shared-service mutations. |
| Packaged Windows runtime | Needs work | Build configuration addresses native PDF dependencies, but the actual clean-Windows artifact was not executed, so installer readiness cannot be certified. |
