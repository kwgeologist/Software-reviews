import sys,tempfile,json,struct
from pathlib import Path
import numpy as np
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path[:0]=[str(R),str(R/'tests')]
from seismicworkbench import kingdom as K
from seismicworkbench.interpretation import Interpretation,fault_sticks
from seismicworkbench.project import SeismicStore
from test_native_kingdom import geometry
from ogcore.cfb import CompoundFile
from database import ProjectDatabase
out={};g=geometry(10,10,0,0)
with tempfile.TemporaryDirectory()as t:
 p=Path(t);db=ProjectDatabase(p/'f.ogwdb');sid=db.execute("INSERT INTO seismic_surveys(name,file_path,domain,units)VALUES('S','s.sgy','depth','ft')");it=Interpretation(g.shape)
 for index,z0 in enumerate([100.,200.]):
  f=K.KingdomFault('F',source_files={f'source{index}.FLT'});st=K.KingdomStick(1,'7',());st.points=[{'seq':i+1,'line':0.,'trace':float(i),'x':float(g.x[0,i]),'y':float(g.y[0,i]),'z':z0+i}for i in range(3)];f.sticks[(str(index),1)]=st;picks,_=K.fault_picks(f,g,1.);K.apply_faults(it,{'F':picks},'Merge' if index else 'New name',{'F':K.provenance('fault',f)})
 store=SeismicStore(db);store.save_interpretation(sid,it,{},{});db.close();db=ProjectDatabase(p/'f.ogwdb');back,_,_=SeismicStore(db).load_interpretation(sid,g.shape);out['merge_reopen']={'sticks':len(fault_sticks(back.faults['F'])),'z_order':[[x['twt']for x in pts]for pts in fault_sticks(back.faults['F']).values()],'provenance_files':back.provenance[('Fault','F')]['source_files']};db.close()
 # Actual OLE2 directory mutation, leaving header/container structurally readable.
 raw=bytearray((R/'tests/data/native/kingdom_native/F01000.FLT').read_bytes());cf=CompoundFile(bytes(raw));e=cf.entry('Fault_Data');sect=struct.unpack_from('<I',raw,0x30)[0];off=e.index*128
 while off>=cf.sector:sect=cf.fat[sect];off-=cf.sector
 struct.pack_into('<I',raw,(sect+1)*cf.sector+off+0x74,9999999);f=p/'broken.FLT';f.write_bytes(raw)
 try:r=K.read_native([f]);out['broken_flt']={'handled':True,'diagnostics':[str(x)for x in r.diagnostics]}
 except Exception as e:out['broken_flt']={'handled':False,'exception':type(e).__name__,'message':str(e)}
 # An empty placement under Replace removes a previous interpreted horizon.
 it=Interpretation((3,3));it.set_horizon_pick('H',0,0,100.);K.apply_horizons(it,{'H':K.HorizonPlacement('H',np.array([],int),np.array([],int),np.array([],float),unmatched=1)},'Replace',{});out['empty_replace']={'prior_picks':1,'after_picks':len(it.horizons['H'])}
(R.parent/'fault-persistence-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
