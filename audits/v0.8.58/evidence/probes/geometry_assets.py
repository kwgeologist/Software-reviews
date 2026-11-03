import sys,json,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from ogmap import georef as G
from ograster import pdf_import as P
from ogvol import engine as E
from ogcore.surface import Surface
from ogcore import synthetic
out={}
print(G.Point.__annotations__ if hasattr(G,'Point') else [k for k in dir(G) if 'Point' in k])
points=[G.ControlPoint(ix=0,iy=0,mx=0,my=0),G.ControlPoint(ix=1,iy=0,mx=1,my=0),G.ControlPoint(ix=0,iy=1,mx=2,my=0)]
f=G.fit(points);out['singular_georef']={'coefficients':f.coefficients,'rms':f.rms,'determinant':float(np.linalg.det(G.matrix(f.coefficients)))}
ins={'net_pay':E.Input('grid',Surface.regular(0,0,100,100,np.full((3,3),65.)),unit='ft'),'porosity':E.Input('constant',value=.2,unit='v/v'),'sw':E.Input('constant',value=.25,unit='v/v'),'bo':E.Input('constant',value=1.2)}
bow=np.array([[0.,0.],[200.,200.],[0.,200.],[200.,0.]])
try:
 r=E.compute(E.Case(mode='grid',inputs=ins,boundary=('crossed',bow),metres_per_unit=.3048));out['crossed_grid_boundary']={'accepted':True,'cells':r.totals.cells,'in_place':r.totals.in_place}
except Exception as e:out['crossed_grid_boundary']={'accepted':False,'error':str(e)}
with tempfile.TemporaryDirectory() as t:
 target=Path(t)/'existing.tif';target.write_bytes(b'previous asset');layout=P.Layout('synthetic.pdf');
 try:
  with patch.object(P.Layout,'assemble',return_value=Image.new('RGB',(3,3),'white')),patch.object(Path,'write_text',side_effect=OSError('synthetic sidecar write failure')):layout.write(target)
 except OSError as e:out['pdf_partial_write']={'raised':str(e),'previous_bytes_preserved':target.read_bytes()==b'previous asset','tiff_written':target.read_bytes()[:2] in (b'II',b'MM'),'sidecar_exists':target.with_suffix('.tif.json').exists()}
out['synthetic_density_explicit_gcc']={'input':[2500.],'unit':'g/cc','result':synthetic.density_gcc([2500.],'g/cc').tolist()}
Path('/workspace/audit-v0.8.58/geometry-assets-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
