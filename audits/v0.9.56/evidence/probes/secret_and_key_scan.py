from pathlib import Path
import sys,json,re,hashlib,base64,marshal,types
from cryptography.hazmat.primitives import serialization
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56';D=R/'dist/OandG_Workbench';S=R/'build/stage/OandG_Workbench_v0.9.56';sys.path.insert(0,str(R))
from ogcore import licensing_keys
from PyInstaller.archive.readers import CArchiveReader
out={'customer_key_files':[],'input_private_key_blocks':[],'customer_private_key_blocks':[],'pyz_private_key_constants':[],'embedded_public_key_ids':list(licensing_keys.PUBLIC_KEYS),'customer_data_candidates':[]}
private=re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----\r?\n[A-Za-z0-9+/=\r\n]{40,}')
for p in R.rglob('*'):
 if not p.is_file():continue
 relative=str(p.relative_to(R));inside=p.is_relative_to(D)
 data=p.read_bytes()
 if private.search(data):out['input_private_key_blocks'].append(relative)
 if inside:
  if private.search(data):out['customer_private_key_blocks'].append(relative)
  if p.suffix.lower()in['.ogwkey','.ogwlic','.pfx','.p12','.key']:out['customer_key_files'].append(str(p.relative_to(D)))
  if p.suffix.lower()in['.ogwdb','.las','.sgy','.segy','.wsd','.ppf']:out['customer_data_candidates'].append(str(p.relative_to(D)))
for p in D.glob('*.exe'):
 a=CArchiveReader(str(p));z=a.open_embedded_archive(next(n for n,v in a.toc.items()if v[-1]=='z'))
 def constants(code):
  if isinstance(code,types.CodeType):
   for x in code.co_consts:yield from constants(x)
  elif isinstance(code,(str,bytes)):yield code.encode('utf-8','surrogatepass')if isinstance(code,str)else code
 for module in z.toc:
  try:code=z.extract(module)
  except Exception:continue
  if any(private.search(t)for t in constants(code)):out['pyz_private_key_constants'].append({'executable':p.name,'module':module})
p=R/'build/owner_check/lm/keys/ogw-selftest-01.ogwkey';key=serialization.load_pem_private_key(p.read_bytes(),password=b'self-test passphrase, not a real key');public=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw);out['included_build_key']={'path':str(p.relative_to(R)),'encrypted':True,'matches_documented_selftest_passphrase':True,'public_fingerprint_sha256':hashlib.sha256(public).hexdigest(),'matches_embedded_production_key':any(base64.b64decode(s)==public for s in licensing_keys.PUBLIC_KEYS.values()),'customer_contains_this_key':any(p.read_bytes()in q.read_bytes()for q in D.rglob('*')if q.is_file()and q.stat().st_size<1024*1024)}
(B/'secret-scan-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
