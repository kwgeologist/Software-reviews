import sys,json,math,tempfile
from pathlib import Path
import numpy as np
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path.insert(0,str(R))
from ogcore.depth import minimum_curvature,complete_depth_triplet
from ogcore.surface import Surface,write_zmap,read_zmap
from seismicworkbench.synthetic import synthetic_times
from seismicworkbench.wells import SeismicWell
out={}
s=[{'md':0,'inc':0,'azi':90},{'md':1000,'inc':0,'azi':90}];minimum_curvature(s);assert abs(s[-1]['tvd']-1000)<1e-9 and abs(s[-1]['ew'])<1e-9
out['vertical_survey']=s[-1]
s=[{'md':0,'inc':0,'azi':90},{'md':1000,'inc':90,'azi':90}];minimum_curvature(s);expected=2000/math.pi;assert abs(s[-1]['tvd']-expected)<1e-9 and abs(s[-1]['ew']-expected)<1e-9
out['quarter_circle_survey']={'actual':s[-1],'expected_vertical_and_east':expected}
triplet=complete_depth_triplet(md=1000,survey=[(0,0),(1000,800)],elevation=500,prefer='md');assert triplet==(1000,800,-300);out['md_tvd_tvdss']=triplet
for unit,scale in [('ft',1),('m',.3048)]:
 d=np.array([1000,1500,2000])*scale;ss=500*scale-d;t=synthetic_times(d,ss,unit,np.full(3,100.),0,10000)
 np.testing.assert_allclose(t,[100,200,300],atol=1e-9);out['constant_sonic_'+unit]=t.tolist()
w=SeismicWell(id=1,name='reference',depth_units='ft');v=w.seismic_values([-1000/.3048],'depth',datum_elevation=100,units='m');np.testing.assert_allclose(v,[1100],atol=1e-9);out['seismic_depth_m_with_100m_datum']=v.tolist()
x,y=np.meshgrid(np.arange(6)*100.+500000,np.arange(5)*100.+3000000);z=2000+.01*(x-500000)-.02*(y-3000000)
surface=Surface.regular(500000,3000000,100,100,z,name='Reference',unit='ft')
np.testing.assert_allclose(surface.sample([500050,500250],[3000050,3000250]),[1999.5,1997.5],atol=1e-9)
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'plane.zmap';write_zmap(surface,p);back=read_zmap(p);np.testing.assert_allclose(back.values,z,atol=1e-7);np.testing.assert_allclose(back.origin,surface.origin);out['zmap_roundtrip']={'shape':list(back.shape),'max_error':float(np.max(np.abs(back.values-z)))}
out['status']='passed';Path('/workspace/audit-v0.9.53/scientific-reference-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
