import sys,tempfile,json
from pathlib import Path
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from database import ProjectDatabase
from ogcore import survey_files,depth
out={}
with tempfile.TemporaryDirectory() as t:
 p=Path(t);db=ProjectDatabase(p/'p.ogwdb');w=db.add_well('Feet well');f=p/'metric.csv';f.write_text('MD,Inc,Azi\n(m),(deg),(deg)\n0,0,0\n100,0,0\n');db.import_directional_survey(w,f,'MD, Azi, Inc');r=db.row('SELECT measured_depth,tvd FROM deviation_points WHERE well_id=? ORDER BY measured_depth DESC',(w,));out['metric_survey_to_feet_well']={'well_unit':db.well_depth_unit(w),'explicit_file_units':'m','last_MD':r['measured_depth'],'last_TVD':r['tvd'],'expected_ft':100/.3048}
 a=db.add_well('ST01','49005234560100');b=db.add_well('ST02','49005234560200');f=p/'ambiguous.csv';f.write_text('API,MD,Inc,Azi\n4900523456,0,0,0\n4900523456,100,0,0\n');surveys=survey_files.read_surveys(f);out['ambiguous_survey_match']={'candidate_wells':[a,b],'actual_match':db.survey_wells(surveys),'import_result':db.import_survey_table(f)}
 stations=[{'md':0.,'inc':0.,'azi':0.},{'md':1000.,'inc':0.,'azi':0.}];depth.minimum_curvature(stations);out['vertical_sanity']=stations[-1]
 db.close()
Path('/workspace/audit-v0.8.58/survey-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
