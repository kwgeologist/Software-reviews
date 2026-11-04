import os,sys,json,tempfile,struct,copy
from pathlib import Path
import numpy as np
ROOT=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');OUT=ROOT.parent
sys.path[:0]=[str(ROOT),str(ROOT/'tests')]
from seismicworkbench import kingdom as K,kingdom_native as N
from seismicworkbench.interpretation import Interpretation,fault_sticks
from test_native_kingdom import geometry
from ogcore import symbol_catalog as C,ihs297 as I
from database import ProjectDatabase
import well_symbols as W
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);os.environ['OGW_SYMBOL_CATALOG']=str(p/'catalog.json')
 for name,data in [('bad_numeric',{'symbols':{'OIL':{'scale':'oops'}}}),('bad_symbols_type',{'symbols':[] or ['x']}),('bad_geometry',{'symbols':{'OIL':{'render':{'body':'no-such-body'}}}})]:
  f=p/(name+'.json');f.write_text(json.dumps(data))
  try:cat=C.load(f);C.install(cat);out[name]={'load_succeeded':True,'validation':cat.validate()}
  except Exception as e:out[name]={'load_succeeded':False,'exception':type(e).__name__,'message':str(e)}
 C.install(C.builtin())
 cat=C.builtin();cat.entry('OIL').symbol_id=cat.entry('GAS').symbol_id;out['duplicate_sym']={'validation':cat.validate(),'shared_sym':cat.entry('OIL').symbol_id};C.save(cat,p/'dup.json');out['duplicate_sym']['saved']=True;out['duplicate_sym']['numeric_resolves']=W.find_symbol(str(cat.entry('GAS').symbol_id)).code;C.install(C.builtin())
 db=ProjectDatabase(p/'p.ogwdb');wid=db.add_well('Synthetic metric well','42401123450000');db.update_well(wid,{'elevation_units':'m','kb_elevation':100.})
 w=I.Well('42401123450000',1);w.tops=[('SAND',1000.,'')];w.stations=[{'md':0.,'inc':0.,'azi':0.},{'md':1000.,'inc':0.,'azi':0.}];parsed=I.Parsed(p/'synthetic.97f',wells=[w],issues=I.Issues());I.apply(db,I.plan(db,parsed,datum='EPSG:4326'))
 top=db.row('SELECT measured_depth FROM formation_tops WHERE well_id=?',(wid,))[0];survey=db.row('SELECT MAX(measured_depth) FROM deviation_points WHERE well_id=?',(wid,))[0]
 out['297_metric_well']={'well_unit':db.well_depth_unit(wid),'top_1000ft_stored':top,'survey_1000ft_stored':survey,'expected_m':304.8}
 # A fill-only import containing no child records replaces all prior IHS child data.
 empty=I.Well(w.uwi,1);I.apply(db,I.plan(db,I.Parsed(p/'headers.97f',wells=[empty],issues=I.Issues()),datum='EPSG:4326'))
 out['297_header_only_reimport']={'prior_top_count':1,'after_top_count':db.row('SELECT COUNT(*) FROM formation_tops WHERE well_id=?',(wid,))[0]}
 db.close()
 # Two additions to a fault reuse the source section/stick key and become one group.
 g=geometry(10,10,0,0);f=K.KingdomFault('F');st=K.KingdomStick(1,'7',());st.points=[{'seq':i+1,'line':0.,'trace':float(i),'x':float(g.x[0,i]),'y':float(g.y[0,i]),'z':100.+i}for i in range(3)];f.sticks[('a',1)]=st
 picks,_=K.fault_picks(f,g,1.);it=Interpretation(g.shape);K.apply_faults(it,{'F':picks},'New name',{});K.apply_faults(it,{'F':picks},'Merge',{});groups=fault_sticks(it.faults['F']);out['fault_merge']={'input_sticks_per_import':1,'imports':2,'result_sticks':len(groups),'node_sequence':[[x['seq']for x in a]for a in groups.values()]}
 # Truncate a real native horizon inside the directory, retaining the initial signature.
 raw=(ROOT/'tests/data/native/kingdom_native/H02503.hzn').read_bytes();idx=raw.find(N.DIRECTORY_TAIL);f=p/'truncated.hzn';f.write_bytes(raw[:max(N.DATA_START,idx+44)])
 try:r=K.read_native([f]);out['truncated_hzn']={'handled':True,'diagnostics':[str(x)for x in r.diagnostics]}
 except Exception as e:out['truncated_hzn']={'handled':False,'exception':type(e).__name__,'message':str(e)}
C.install(C.builtin());(OUT/'boundary-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
