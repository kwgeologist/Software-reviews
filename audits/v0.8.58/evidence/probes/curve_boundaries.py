exec(open('/workspace/audit-v0.8.58/probes/curves.py').read().split('out={}')[0])
from petroworkbench.well_data import WellData
out={}
with tempfile.TemporaryDirectory() as t:
 p=Path(t);db=ProjectDatabase(p/'p.ogwdb');w=db.add_well('A');lid=db.load_las_file(w,write_las(p/'a.las',np.array([100.,101.,102.]),{'GR':np.array([1.,2.,3.]),'RT':np.array([4.,5.,6.])}))
 run=cs.run(db,lid);wd=WellData.from_run(run,'a.las');wd.curves['GR'][0]=99
 out['mutable_run']={'working_value':float(wd.curves['GR'][0]),'another_run_reader':float(cs.run(db,lid).curves['GR'][0]),'canonical_curve_reader':float(cs.read(db,w,'GR')[1][0])}
 cs.forget(db);cs.run(db,lid);cs.delete_curve(db,cs.resolve(db,w,'GR'))
 out['delete']={'cached_values':cs.run(db,lid).curves['GR'].tolist(),'uncached_values':str(db.las_run(lid).curves['GR'].tolist())}
 rt=cs.resolve(db,w,'RT');cs.update_curve(db,rt,values=[8.,9.]);out['length_mismatch']={'stored_samples':len(__import__('database').unpack_array(db.row('SELECT data FROM curves WHERE id=?',(rt.id,))['data'])),'axis_samples':3,'canonical_read':str(cs.read(db,w,'RT'))}
 db.close()
Path('/workspace/audit-v0.8.58/curve-boundaries-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
