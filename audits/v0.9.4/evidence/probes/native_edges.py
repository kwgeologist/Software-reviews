import sys,tempfile,json,struct
from pathlib import Path
import numpy as np
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path[:0]=[str(R),str(R/'tests')]
from seismicworkbench import kingdom as K,kingdom_native as N
from test_native_kingdom import geometry
out={};raw=(R/'tests/data/native/kingdom_native/H02503.hzn').read_bytes()
with tempfile.TemporaryDirectory()as t:
 p=Path(t)
 for stop in [1750,2400,4200]:
  f=p/f'truncated_{stop}.hzn';f.write_bytes(raw[:stop])
  try:r=K.read_native([f]);out[f'truncate_{stop}']={'handled':True,'diagnostic_count':len(r.diagnostics)}
  except Exception as e:out[f'truncate_{stop}']={'handled':False,'exception':type(e).__name__,'message':str(e)}
 # Retain native pick codes while corrupting a picked sample to NaN.
 data=bytearray(raw);h=N.read_horizon(R/'tests/data/native/kingdom_native/H02503.hzn');d=next(d for d in N._directories(raw)if d.attribute==h.attribute)
 page,tl,tt,*_=d.tiles[0];start,mask=N.tile_offsets(page);arr=np.frombuffer(raw,'<f4',N.TILE*N.TILE,start).reshape(N.TILE,N.TILE);m=np.frombuffer(raw,np.uint8,N.TILE*N.TILE//4,mask);codes=np.stack([(m>>(2*b))&3 for b in range(4)],1).reshape(N.TILE,N.TILE);li,ti=np.argwhere(np.isin(codes,N.VALID_CODES))[0];struct.pack_into('<f',data,start+4*(int(li)*N.TILE+int(ti)),float('nan'));f=p/'nan.hzn';f.write_bytes(data);got=N.read_horizon(f);out['picked_nan']={'native_picks':got.count,'nonfinite_values':int((~np.isfinite(got.z)).sum())}
 # Current native numbering on a survey with increment 2.
 g=geometry(3,3,100,200);g.ilines=np.array([100,102,104]);g.xlines=np.array([200,202,204]);native=K.KingdomHorizon('sample',z=[100.,101.,102.],x=[np.nan]*3,y=[np.nan]*3,internal=[(0,0),(1,1),(2,2)],grid=(3,3));placed=K.place_horizon(native.with_origin(100,200),g,1.)
 out['increment_two_survey']={'input_grid_nodes':native.internal,'numbered_lines':native.with_origin(100,200).line,'placed_bins':list(zip(placed.i.tolist(),placed.j.tolist())),'unmatched':placed.unmatched}
(R.parent/'native-edge-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
