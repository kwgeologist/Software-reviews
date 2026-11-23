from pathlib import Path
import re,html,hashlib,json,shutil,zipfile,csv
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
B=Path('/workspace/audit-v0.9.72-full');O=B/'deliverables';N='OandG_Workbench_v0.9.72_Full_Audit'
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
 cols=len(data[0]);widths=([49,44,236,190]if cols==4 else([52,85,382]if cols==3 else([165,354]if cols==2 else[519/cols]*cols)))
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
 c.setFont('DV',6.5);c.drawString(38,22,'O&G Workbench v0.9.72 | Read-only pre-v1.0 audit | 23 November 2026');c.drawRightString(557,22,str(d.page))
SimpleDocTemplate(str(O/(N+'.pdf')),pagesize=(595,842),leftMargin=38,rightMargin=38,topMargin=35,bottomMargin=40,title='O&G Workbench v0.9.72 Comprehensive Audit',author='Independent code review').build(story,onFirstPage=footer,onLaterPages=footer)

print('Rendered v0.9.72 audit PDF')
