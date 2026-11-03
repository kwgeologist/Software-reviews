import sys,json,math
from pathlib import Path
import numpy as np
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from ogcore import formulas,depth,raster
from ogcore.surface import Surface
from ogvol import engine as E
out={}
names={'PHIE':np.array([.2]),'RT':np.array([10.]),**formulas.HELPERS};out['archie']={'expected':math.sqrt(.075/(10*.2**2)),'actual':float(formulas.evaluate('((1*.075)/(RT*PHIE**2))**.5',names)[0])}
out['vsh_endpoints']={'expected':[0.,1.],'actual':formulas.evaluate('(GR-32)/(118-32)',{'GR':np.array([32.,118.])}).tolist()}
c=raster.Calibration([(1000,100),(2000,1100)]);out['raster_linear_calibration']={'expected_depth':1500.,'actual_depth':float(c.depth_at([600])[0]),'expected_row':600.,'actual_row':float(c.row_at([1500])[0])}
s=[{'md':0.,'inc':60.,'azi':0.},{'md':1000.,'inc':60.,'azi':0.}];depth.minimum_curvature(s);out['constant_60_degree_survey']={'expected_tvd':500.,'actual_tvd':s[-1]['tvd'],'expected_north':1000*math.sin(math.pi/3),'actual_north':s[-1]['ns']}
a=math.pi/6;surf=Surface(np.full((3,4),10.),(0,0),(100*math.cos(a),100*math.sin(a)),(-100*math.sin(a),100*math.cos(a)))
ins={'net_pay':E.Input('grid',surf,unit='ft'),'porosity':E.Input('constant',value=.2,unit='v/v'),'sw':E.Input('constant',value=.25,unit='v/v'),'bo':E.Input('constant',value=1.2)}
r=E.compute(E.Case(mode='grid',inputs=ins,metres_per_unit=.3048));out['rotated_grid']={'expected_ft2':60000.,'actual_ft2':r.totals.area_acres*43560,'cells':r.totals.cells}
plane=np.tile(np.arange(3)*5.+5.,(3,1));ins['net_pay']=E.Input('grid',Surface.regular(0,0,100,100,plane),unit='ft');r=E.compute(E.Case(mode='grid',inputs=ins,metres_per_unit=.3048));out['linear_plane']={'expected_net_acre_ft':40000/43560*10,'actual_net_acre_ft':r.totals.net_af}
Path('/workspace/audit-v0.8.58/analytical-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
