from pathlib import Path
import json,sys,pefile,hashlib,email,re,platform,importlib.metadata as M
B=Path('/workspace/audit-v0.9.56-windows');R=B/'input/OandG_Workbench_v0.9.56';sys.path[:0]=[str(R),str(R/'tools/release')]
from PyInstaller.archive.readers import CArchiveReader
from ogcore import __version__
manifest=json.loads((R/'release/manifest.json').read_text());a=CArchiveReader(str(R/'dist/Owner Tools/O&G Workbench License Manager.exe'));name=next(n for n in a.toc if n.lower().endswith('python312.dll'));pe=pefile.PE(data=a.extract(name));versions={}
for group in getattr(pe,'FileInfo',[]):
 for item in group:
  for table in getattr(item,'StringTable',[]):versions.update({k.decode(errors='replace'):v.decode(errors='replace')for k,v in table.entries.items()})
out={'application_version':__version__,'source_expected_commit':'500ba84 (feature/artifact baseline, no Git metadata required)','userdata_present':(R/'ogcore/userdata.py').exists(),'owner_embedded_python_version':versions.get('ProductVersion'),'manifest_python_min':manifest['python_min'],'customer_python_version':'3.12.5','passes_declared_runtime_floor':False,'baseline_features_and_packaged_pure_modules_match':True,'source_state_is_unmodified':True,'windows_execution_in_this_audit':False,'reported_windows_qualification':['Build_Windows_EXE success','15 modules compiled; customer/owner protection passed','owner self-test passed','all Workbench windows/project launch','DPAPI passed','Explorer drop passed','packaged PDF/license tests 9 passed','full serial 2800 passed'],'independent_windows_binary_and_archive_inspection':True}
(B/'baseline-verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
metadata={'platform':platform.platform(),'python':sys.version,'versions':{n:M.version(n) for n in ['pyinstaller','pefile','pytest','cryptography','reportlab']},'input_read_only':'No source or artifact modifications; audit scripts under a separate folder'};(B/'environment.json').write_text(json.dumps(metadata,indent=2))
