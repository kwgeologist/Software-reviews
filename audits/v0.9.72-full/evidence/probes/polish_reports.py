from pathlib import Path
B=Path('/workspace/audit-v0.9.72-full/deliverables')
replacements={
 'Cython/Tk9':'Cython / Tk 9',' Tk8.6':' Tk 8.6',' Tk9':' Tk 9','exit0':'exit 0','exit139':'exit 139','SIGSEGV139':'SIGSEGV / exit 139','All15':'All 15','all15':'all 15','all17':'all 17','All293':'All 293','all293':'all 293','all977':'all 977','all980':'all 980','across14':'across 14','spans14':'spans 14','covers662':'covers 662','including362':'including 362','files (362':'files (362','files,186341':'files, 186,341','collecting3234':'collecting 3,234','and3234':'and 3,234','The112000':'The 112,000','all112000':'all 112,000','with38000':'with 38,000','source.980':'source. 980','Git.980':'Git. 980','total;977':'total; 977','names977':'names 977','was361432KiB':'was 361,432 KiB','in47.63s':'in 47.63 s','49.45s':'49.45 s','load0.89s':'load 0.89 s','refresh0.17s':'refresh 0.17 s','load0.70s':'load 0.70 s','load1.37s':'load 1.37 s','refresh0.91s':'refresh 0.91 s','TVD10000-9990':'TVD 10,000–9,990','MD 10000-12000':'MD 10,000–12,000','gross0/net10/PhiH2':'gross 0 / net 10 / PhiH 2','N/A; unique':'N/A; unique','Eighteen':'Eighteen','iso:2327':'iso:2,327','synthetic2327':'synthetic 2,327','In a synthetic2327':'In a synthetic 2,327','The2327-file':'The 2,327-file','all327':'all 327','a10ms':'a 10 ms','measured4.33s':'measured 4.33 s','ordinary5s':'ordinary 5 s','roughly27minutes':'roughly 27 minutes','in about0.93s':'in about 0.93 s','after0.13s':'after 0.13 s','its800':'its 800','audit\'s800':'audit\'s 800','20,000events':'20,000 events', 'Windows customer EXE/.pyd':'Windows customer EXE / .pyd'}
for p in B.glob('*.md'):
 s=p.read_text()
 for a,b in replacements.items():s=s.replace(a,b)
 s=s.replace('D:\\\\Audit_v0972\\\\','D:\\Audit_v0972\\')
 s='\n'.join(line.replace(chr(92)*2,chr(92))if 'py -3.12'in line else line for line in s.split('\n'))
 p.write_text(s)
print('Polished Markdown deliverables')
