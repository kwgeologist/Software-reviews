import sys,json
from pathlib import Path
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path.insert(0,str(R))
from geosteering import app as G,model
from geosteering.demo import demo_job
out={}
def labels(app):
 bar=next(w for w in app.winfo_children() if w.__class__.__name__=='WrapBar')
 return [' '.join(str(w.cget('text')).split()) for w,g in bar.items if w.winfo_class()=='TButton']
for flag in [False,True]:
 with patch.object(G,'AUTOMATIC_STEERING_UI',flag):
  A=G.GeosteeringWorkbench();A.withdraw();A.load_job(demo_job());A.update();out['toolbar_'+str(flag)]=labels(A)
  if not flag:
   A.start_interpretation();md=.5*(A.job.interp.start_md+A.job.interp.end_md);calls=[];real=model.fit_fault
   def fitted(*a,**kw):
    result=real(*a,**kw);calls.append({'options':kw,'result':result});return result
   def answer(d):d.throw.set('7.5');d.mode.set('both');d.result=d.apply();d.destroy()
   with patch.object(type(A),'wait_window',side_effect=answer),patch.object(model,'fit_fault',side_effect=fitted):A.insert_fault_dialog(md)
   out['hidden_ui_manual_fault']={'calls':calls,'faults':A.job.interp.faults()}
   out['geosteering_self_test_body_exit']=G.self_test(A)
  A.dirty=False;A.job.path=None;A.on_close()
Path('/workspace/audit-v0.9.53/geosteering-independent-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
