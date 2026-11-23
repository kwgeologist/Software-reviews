from pathlib import Path
import urllib.request,lzma,subprocess,json
B=Path('/workspace/audit-v0.9.70-tk-segfault');D=B/'native';D.mkdir(exist_ok=True)
u='https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.xz';raw=urllib.request.urlopen(u).read();packages=lzma.decompress(raw).decode();want={'gdb','tk8.6-dev','tcl8.6-dev','libdebuginfod1t64','libipt2','libbabeltrace1','libsource-highlight4t64','libboost-regex1.83.0','libpython3.13'};out=[]
for block in packages.split('\n\n'):
 fields={}
 for line in block.splitlines():
  if ': 'in line and not line.startswith(' '):k,v=line.split(': ',1);fields[k]=v
 if fields.get('Package')in want:
  p=D/Path(fields['Filename']).name;p.write_bytes(urllib.request.urlopen('https://deb.debian.org/debian/'+fields['Filename']).read());subprocess.run(['dpkg-deb','-x',str(p),str(D/'root')],check=True);out.append({k:fields.get(k)for k in ['Package','Version','SHA256','Filename']})
(B/'native-packages.json').write_text(json.dumps(out,indent=2));print([x['Package']for x in out])
# Exact CPython patch release source for a diagnostic extension linked to system Tcl/Tk8.6.
S=B/'tk86-extension';(S/'clinic').mkdir(exist_ok=True,parents=True)
for name in ['_tkinter.c','tkinter.h','clinic/_tkinter.c.h']:
 p=S/name;p.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/python/cpython/v3.12.14/Modules/'+name).read())
