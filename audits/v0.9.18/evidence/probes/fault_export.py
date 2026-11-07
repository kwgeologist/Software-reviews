import sys,tempfile,json,csv
from pathlib import Path
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path[:0]=[str(R),str(R/'tests')]
from test_seismic_picks_io import open_project
from seismicworkbench import picks_io as IO
from seismicworkbench.project import SeismicStore
from seismicworkbench.interpretation import fault_sticks
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);path,db,sid,shape=open_project(p/'A');store=SeismicStore(db);it,styles,vis=store.load_interpretation(sid,shape);nodes=[]
 for source,i in [('A',1),('B',2)]:
  nodes +=[{'i':i,'j':j,'twt':100.+i*10+j,'section':'ARB (Kingdom stick 7)','stick_id':'7','stick_key':'source-'+source+'-7','seq':j+1}for j in range(3)]
 it.faults['F']=nodes;store.save_interpretation(sid,it,styles,vis);export=p/'fault.csv';IO.export_native(db,'Fault',['F'],export);table=IO.read_table(export);pv=IO.preview(db,table,IO.native_mapping());obj=pv.objects[('Fault','F')];obj.mode='Create New';obj.new_name='F_round';report=IO.apply(db,pv);back=store.load_interpretation(sid,shape)[0];out={'source_sticks':len(fault_sticks(nodes)),'exported_stick_ids':sorted({r['Stick']for r in csv.DictReader(x for x in export.read_text().splitlines()if not x.startswith('#'))}),'import_report':report,'roundtrip_sticks':len(fault_sticks(back.faults['F_round'])),'roundtrip_sequences':[[p['seq']for p in pts]for pts in fault_sticks(back.faults['F_round']).values()]};db.close()
(B/'fault-export-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
