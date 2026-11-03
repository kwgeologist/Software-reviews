import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from ogcore import synthetic as S,multimineral as M
# Independent hard-coded linear mixture: .50 calcite, .20 dolomite, .15 wet shale, .15 free fluid.
v=np.array([.5,.2,.15,.15]);rho=np.array([2.71,2.87,2.55,1.]);nphi=np.array([0.,.02,.30,1.]);pe=np.array([5.08,3.14,3.4,.36]);rh=float(v@rho);ne=float(v@nphi);u=float(v@(pe*((rho+.1883)/1.0704)));pelog=u/((rh+.1883)/1.0704)
r=M.invert(M.Model(minerals=['calcite','dolomite'],shale_mode='curve',shale_porosity=.12),{'RHOB':np.array([rh]),'NPHI':np.array([ne]),'PE':np.array([pelog])},vsh=np.array([.15]))
s=S.make_synthetic(np.arange(10,dtype=float),np.full(10,70.),np.linspace(2.3,2.6,10),dt_ms=1.,freq_hz=30.)
out={'independent_mineral_mixture':{'input_logs':{'RHOB':rh,'NPHI':ne,'PE':pelog},'expected':{'VCAL':.5,'VDOL':.2,'VSH':.15,'PHIE':.15,'PHIT':.168},'actual':{k:float(r.curves[k][0]) for k in ['VCAL','VDOL','VSH','PHIE','PHIT']},'qc':int(r.qc[0])},'short_synthetic':{'time_length':len(s.time),'trace_length':len(s.trace),'wavelet_length':len(s.wavelet)}}
Path('/workspace/audit-v0.8.58/science-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
