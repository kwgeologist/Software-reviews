import sys,re,json
from pathlib import Path
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path.insert(0,str(R))
from ogcore import licensing_keys
files=[p for p in R.rglob('*') if p.is_file()];bad_names=[];blocks=[]
for p in files:
 if p.suffix.lower() in ('.ogwkey','.pem','.key','.pfx','.p12'):bad_names.append(str(p.relative_to(R)))
 if re.search(rb'-----BEGIN [A-Z ]*PRIVATE KEY-----\s*[A-Za-z0-9+/=]{40,}',p.read_bytes()):blocks.append(str(p.relative_to(R)))
manifest=json.loads((R/'release/manifest.json').read_text())
result={'files_scanned':len(files),'prohibited_key_filenames':bad_names,'private_key_blocks':blocks,'embedded_public_key_ids':list(licensing_keys.PUBLIC_KEYS),'production_ready':licensing_keys.production_ready(),'owner_spec_present':(R/'release/OwnerTools_LicenseManager.spec').is_file(),'license_manager_excluded': 'license_manager' in manifest['pyinstaller']['exclude_modules'],'customer_executables':list(manifest['executables']),'git_tracking_not_verifiable_from_zip':True}
print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.39/archive-security-evidence.json').write_text(json.dumps(result,indent=2))
