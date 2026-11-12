import sys,tempfile,json,csv
from pathlib import Path
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path.insert(0,str(R))
from ogmap import isopach
from ogvol import report
from geoworkbench import spreadsheet
result=[]
with tempfile.TemporaryDirectory() as td:
 for name,fn in [('volumetrics',lambda p:report.write_csv(p,'Reviewed',{'fluid':'oil'})),('spreadsheet',lambda p:spreadsheet.export_csv(p,['API'],[{'values':['4900000001']}]))]:
  p=Path(td)/(name+'.csv');p.write_bytes(b'PREVIOUS REVIEWED EXPORT\n')
  try:
   real=csv.writer
   def writer(handle,*a,**kw):
    actual=real(handle,*a,**kw)
    class Failing:
     calls=0
     def writerow(self,row):
      self.calls+=1
      if self.calls==2:raise OSError('injected disk full during second row')
      return actual.writerow(row)
    return Failing()
   with patch('csv.writer',side_effect=writer):fn(p)
  except OSError as e:err=str(e)
  result.append({'export':name,'exception':err,'old_preserved':p.read_bytes()==b'PREVIOUS REVIEWED EXPORT\n','bytes_after':len(p.read_bytes())})
print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.39/output-failure-evidence.json').write_text(json.dumps(result,indent=2))
