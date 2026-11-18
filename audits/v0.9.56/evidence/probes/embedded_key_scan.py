from pathlib import Path
import sys,json,re,types,io,zipfile
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56'
from PyInstaller.archive.readers import CArchiveReader
pattern=re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----\r?\n[A-Za-z0-9+/=\r\n]{40,}')
out={'private_key_hits':[],'unreadable_entries':[],'entry_count':0,'pyz_modules_scanned':0}
def scan(data,label,depth=0):
 if not isinstance(data,bytes):return
 if pattern.search(data):out['private_key_hits'].append(label)
 if depth<4 and data[:4]in[b'PK\x03\x04',b'PK\x05\x06']:
  try:
   with zipfile.ZipFile(io.BytesIO(data))as z:
    for i in z.infolist():
     if not i.is_dir()and i.file_size<64*1024*1024:scan(z.read(i),label+'/'+i.filename,depth+1)
  except Exception as e:out['unreadable_entries'].append({'entry':label,'error':type(e).__name__})
def constants(c):
 if isinstance(c,types.CodeType):
  for x in c.co_consts:yield from constants(x)
 elif isinstance(c,(str,bytes)):yield c.encode('utf-8','surrogatepass')if isinstance(c,str)else c
 elif isinstance(c,(tuple,list,frozenset)):
  for x in c:yield from constants(x)
for p in list((R/'dist/OandG_Workbench').glob('*.exe'))+[R/'dist/Owner Tools/O&G Workbench License Manager.exe']:
 a=CArchiveReader(str(p))
 for n,v in a.toc.items():
  label=p.name+'/'+n;out['entry_count']+=1
  if v[-1]=='z':
   try:
    z=a.open_embedded_archive(n)
    for name in z.toc:
     c=z.extract(name);out['pyz_modules_scanned']+=1
     for s in constants(c):scan(s,label+'/'+name,4)
   except Exception as e:out['unreadable_entries'].append({'entry':label,'error':type(e).__name__})
  else:
   try:scan(a.extract(n),label)
   except Exception as e:out['unreadable_entries'].append({'entry':label,'error':type(e).__name__})
(B/'embedded-key-scan-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
