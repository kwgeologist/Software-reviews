from pathlib import Path
import urllib.request,lzma,subprocess,json
B=Path('/workspace/audit-v0.9.70-tk-segfault');D=B/'native';cache=D/'Packages.xz'
if not cache.exists():cache.write_bytes(urllib.request.urlopen('https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.xz').read())
want={'libx11-dev','libxext-dev','x11proto-dev','xtrans-dev','libdw1t64','libelf1t64'};out=[]
for block in lzma.decompress(cache.read_bytes()).decode().split('\n\n'):
 fields={line.split(': ',1)[0]:line.split(': ',1)[1]for line in block.splitlines()if ': 'in line and not line.startswith(' ')}
 if fields.get('Package')in want:
  p=D/Path(fields['Filename']).name;p.write_bytes(urllib.request.urlopen('https://deb.debian.org/debian/'+fields['Filename']).read());subprocess.run(['dpkg-deb','-x',str(p),str(D/'root')],check=True);out.append({k:fields.get(k)for k in ['Package','Version','SHA256','Filename']})
(B/'native-additional-packages.json').write_text(json.dumps(out,indent=2));print([x['Package']for x in out])
