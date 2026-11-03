import sys,json,tempfile
from pathlib import Path
from dataclasses import replace
import numpy as np
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from ogvol import engine as E,scenarios as S
from ogcore.surface import Surface
out={}
def const(v,u=''):return E.Input('constant',value=v,unit=u)
inputs={'net_pay':const(65,'ft'),'porosity':const(.2,'v/v'),'sw':const(.25,'v/v'),'bo':const(1.2),'bg':const(.005)}
manual=E.Case(mode='manual',inputs=inputs,area=150,area_unit='acres',rf=.2)
r=E.compute(manual);out['manual_acceptance']={k:getattr(r.totals,k) for k in ['area_acres','net_af','hcpv_af','in_place','recoverable']}
boundary=('Rectangle',np.array([[0.,0.],[43560.,0.],[43560.,150.],[0.,150.]]))
for mode in ['manual','polygon','grid']:
 ins={**inputs,'porosity':const(35,'v/v')}
 if mode=='grid':ins['net_pay']=E.Input('grid',Surface.regular(0,0,100,100,np.full((3,3),65.)),unit='ft')
 try:
  result=E.compute(E.Case(mode=mode,inputs=ins,area=150,area_unit='acres',boundary=boundary if mode=='polygon' else None,rf=.2,metres_per_unit=.3048))
  out[mode+'_porosity_35']={'accepted':True,'in_place':result.totals.in_place,'net_af':result.totals.net_af}
 except Exception as e:out[mode+'_porosity_35']={'accepted':False,'error':str(e)}
for mode in ['manual','polygon']:
 for name,val in [('net_pay',-65.),('bo',float('nan'))]:
  ins={**inputs,name:const(val,'ft' if name=='net_pay' else '')}
  try:
   result=E.compute(E.Case(mode=mode,inputs=ins,area=150,area_unit='acres',boundary=boundary if mode=='polygon' else None,rf=.2,metres_per_unit=.3048))
   out[f'{mode}_{name}_{val}']={'accepted':True,'in_place':str(result.totals.in_place)}
  except Exception as e:out[f'{mode}_{name}_{val}']={'accepted':False,'error':str(e)}
for n in [2,3,51]:
 ins={**inputs,'net_pay':E.Input('grid',Surface.regular(0,0,100,100,np.full((n,n),65.)),unit='ft')};result=E.compute(E.Case(mode='grid',inputs=ins,rf=.2,metres_per_unit=.3048))
 out[f'nodes_{n}']={'cells':result.totals.cells,'area_ft2':result.totals.area_acres*43560.}
# Inactive inputs of an oil case should not choose its integration frame.
base=E.Case(mode='grid',inputs={**inputs,'net_pay':E.Input('grid',Surface.regular(0,0,100,100,np.full((3,3),65.)),unit='ft')},rf=.2,metres_per_unit=.3048)
base_result=E.compute(base);changed=replace(base,inputs={**base.inputs,'top':E.Input('grid',Surface.regular(0,0,100,100,np.full((3,3),np.nan)),unit='ft')})
try:out['unused_top_nan_grid']={'base':base_result.totals.in_place,'with_unused_grid':E.compute(changed).totals.in_place}
except Exception as e:out['unused_top_nan_grid']={'error':str(e)}
Path('/workspace/audit-v0.8.58/volumetrics-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
