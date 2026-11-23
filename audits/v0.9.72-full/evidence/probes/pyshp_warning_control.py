from pathlib import Path
import tempfile,warnings,json,struct
import shapefile
with tempfile.TemporaryDirectory()as td:
 p=Path(td)/'synthetic'
 with shapefile.Writer(str(p),shapeType=shapefile.POINT)as w:
  w.field('NAME','C',20);w.point(1,2);w.record('synthetic')
 raw=p.with_suffix('.dbf').read_bytes();count=struct.unpack_from('<I',raw,4)[0];header,record=struct.unpack_from('<HH',raw,8)
 with warnings.catch_warnings(record=True)as ws:
  warnings.simplefilter('always')
  with shapefile.Reader(str(p))as r:records=[list(x)for x in r.records()]
 result={'control':'Pyshp writer + reader only; no Workbench imports','version':shapefile.__version__,'dbf_bytes':len(raw),'declared_records':count,'header_bytes':header,'record_bytes':record,'records':records,'warnings':[str(x.message).replace(td,'<temporary>')for x in ws]}
 Path('/workspace/audit-v0.9.72-full/pyshp-warning-control.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
