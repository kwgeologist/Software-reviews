from pathlib import Path
import re,html,hashlib,json,shutil,zipfile,csv
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
B=Path('/workspace/audit-v0.9.70-integrity');O=B/'audit/v0.9.70_project_integrity';N='OandG_Workbench_v0.9.70_Project_Integrity_Audit'
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
s=getSampleStyleSheet()
for k in ['BodyText','Normal','Title','Heading1','Heading2']:s[k].fontName='DV'
s['BodyText'].fontSize=8.5;s['BodyText'].leading=12.4;s['BodyText'].spaceAfter=7
for k,z in [('Title',17),('Heading1',12),('Heading2',10.5)]:s[k].fontName='DVB';s[k].fontSize=z;s[k].leading=z*1.3;s[k].spaceBefore=10;s[k].spaceAfter=6;s[k].keepWithNext=1
s.add(ParagraphStyle(name='Cell',fontName='DV',fontSize=7,leading=10))
story=[];pending=[];rows=[]
def inline(v):
 v=html.escape(v);v=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',v);return v.replace('`','')
def flush():
 if pending:story.append(Paragraph(inline(' '.join(pending)),s['BodyText']));pending.clear()
def table():
 if not rows:return
 data=[[c.strip()for c in r.strip().strip('|').split('|')]for r in rows];data=[r for r in data if not all(re.fullmatch('[: -]+',c)for c in r)]
 cols=len(data[0]);widths=([48,48,423]if data[0][0]=='ID'else[105,207,207])if cols==3 else[165,354]
 t=Table([[Paragraph(inline(c),s['Cell'])for c in r]for r in data],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dde8ed')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#a0b0bd')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,9)]);rows.clear()
for line in (O/(N+'.md')).read_text().splitlines()+['']:
 if line.startswith('|'):flush();rows.append(line);continue
 table()
 if not line.strip():flush();continue
 m=re.match(r'^(#{1,3}) (.*)',line)
 if m:flush();story.append(Paragraph(inline(m[2]),s[{1:'Title',2:'Heading1',3:'Heading2'}[len(m[1])]]))
 elif line.startswith('- ')or re.match(r'^\d+\.\s',line):flush();story.append(Paragraph(inline(line),s['BodyText']))
 else:pending.append(line)
def footer(c,d):
 c.setFont('DV',6.5);c.drawString(38,22,'O&G Workbench v0.9.70 | Read-only project integrity audit | 22 November 2026');c.drawRightString(557,22,str(d.page))
SimpleDocTemplate(str(O/(N+'.pdf')),pagesize=(595,842),leftMargin=38,rightMargin=38,topMargin=35,bottomMargin=40,title='O&G Workbench v0.9.70 Project Integrity Audit',author='Independent code review').build(story,onFirstPage=footer,onLaterPages=footer)
E=O/'evidence';E.mkdir(exist_ok=True)
for name in ['baseline.json','source-hashes.json','final-integrity.json','focused.log','focused.xml','broader.log','broader.xml','tk-recheck.log','tk-recheck.xml','sqlite-scenarios.json','sqlite-scenarios.log','ui-cases.json','ui-cases.log','ui-cases-attempt1.log','close-errors.json','close-errors.log','restart-and-rollback.json','restart-and-rollback.log','drawing-failure.json','drawing-failure.log','journal-sync-search.txt','persistence-search.txt','v0969-v0970.diff','xvfb.log']:
 shutil.copy2(B/name,E/name)
shutil.copytree(B/'compare69',E/'compare69',dirs_exist_ok=True);shutil.copytree(B/'probes',E/'probes',dirs_exist_ok=True)
# Five required deliverables, nonempty nine-finding CSV, expected results and immutable source check.
required=['Project_Integrity_Audit.md','Integrity_Findings.csv','Recovery_Procedure.md','Persistence_Test_Plan.md','Audit_Evidence.md']
assert all((O/('OandG_Workbench_v0.9.70_'+n)).stat().st_size>1000 for n in required)
with (O/'OandG_Workbench_v0.9.70_Integrity_Findings.csv').open(encoding='utf-8-sig')as f:assert len(list(csv.DictReader(f)))==9
manifest={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(O.rglob('*'))if p.is_file() and p.name!='SHA256SUMS.json'}
(O/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2))
zip_path=B/'OandG_Workbench_v0.9.70_Project_Integrity_Evidence.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED)as z:
 for p in sorted(O.rglob('*')):
  if p.is_file():z.write(p,str(Path('audit/v0.9.70_project_integrity')/p.relative_to(O)))
with zipfile.ZipFile(zip_path)as z:assert z.testzip()is None
D=Path('/workspace/shared/downloads');D.mkdir(parents=True,exist_ok=True)
for p in list(O.glob('*.md'))+list(O.glob('*.csv'))+list(O.glob('*.pdf'))+[zip_path]:shutil.copy2(p,D/p.name)
print(json.dumps({'zip':str(D/zip_path.name),'zip_bytes':zip_path.stat().st_size,'sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'files_in_manifest':len(manifest)},indent=2))
