from pathlib import Path
import json,sys,hashlib,importlib,numpy as np
B=Path('/workspace/audit-v0.9.72-full');C=B/'compiled-probe';sys.path[:0]=[str(C),str(C/'tools/release')];from cython_modules import PROTECTED
out={'kind':'audit-built Linux extensions; not Windows package','origins':{}}
for n in PROTECTED:
 m=importlib.import_module(n);p=Path(m.__file__);assert p.suffix=='.so';out['origins'][n]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
from ogcore import pay
from ogcore.depth import DepthConverter
d=np.arange(10000.,12001.,100.);c=DepthConverter([(0,0),(10000,10000),(12000,9990)],0);s=pay.summarize(d,np.ones(d.shape,bool),10000.,12000.,{'PHIE':np.full(d.shape,.2)}, {},tvd_of_md=c.tvd_of_md);out['shallow_upturn_FA_002']={'gross':s.gross,'net':s.net,'phih':s.phih,'note':s.tvd_note};(B/'compiled-origins.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
