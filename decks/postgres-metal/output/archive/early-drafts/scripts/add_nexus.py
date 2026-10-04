from pathlib import Path
import sys,io,re,argparse,xml.etree.ElementTree as ET
sys.path.insert(0,'/private/tmp/ps-pdf-libs')
from fontTools.ttLib import TTFont as FontFile
from fontTools.varLib.instancer import instantiateVariableFont
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
root=Path('/Users/colezuckowsky/Documents/ChatGPT/GTM/planetscale-pitch')
folder=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Render the Nexus as vectors and replace page 2 of the full deck.')
parser.add_argument('--step',type=int,choices=(0,1,2),default=2,help='Number of visible reveals.')
parser.add_argument('--preview-only',action='store_true',help='Render one page without replacing the full deck.')
args=parser.parse_args()
font=FontFile(root/'assets/inter.woff2');font.flavor=None
font=instantiateVariableFont(font,{'wght':500},inplace=True)
fontpath=Path('/private/tmp/ps-nexus-inter.ttf');font.save(fontpath)
pdfmetrics.registerFont(TTFont('DeckInter',str(fontpath)))
pdfmetrics.registerFont(TTFont('DeckMono','/System/Library/Fonts/Menlo.ttc',subfontIndex=0))
pdfmetrics.registerFontFamily('DeckInter',normal='DeckInter',bold='DeckInter',italic='DeckInter',boldItalic='DeckInter')
pdfmetrics.registerFontFamily('DeckMono',normal='DeckMono',bold='DeckMono',italic='DeckMono',boldItalic='DeckMono')
s=(root/'assets/nexus.svg').read_text()
s=re.sub(r'font-family="[^"]*monospace[^"]*"','font-family="DeckMono"',s)
s=re.sub(r'font-family="Inter[^"]*"','font-family="DeckInter"',s)
s=s.replace('font-weight="500"','font-weight="normal"')
ns='http://www.w3.org/2000/svg';tree=ET.fromstring(s)
patterns={'url(#nexus-volume-dots)':'#747474','url(#nexus-problem-dots)':'#6b321d'}
for parent in tree.iter():
 for e in list(parent):
  index=e.get('data-fragment-index')
  if index is not None and int(index)>=args.step:
   parent.remove(e)
for e in tree.iter():
 if e.tag.endswith('g') and e.get('fill') in patterns:
  fill=e.get('fill')
  for child in e:
   if child.tag.endswith('rect') and child.get('fill') is None:child.set('fill',fill)
  e.set('fill','#111111')
for parent in tree.iter():
 for e in list(parent):
  if e.get('fill') in patterns:
   color=patterns[e.get('fill')]
   e.set('fill','#111111');dots=ET.Element('{'+ns+'}g',stroke='none')
   x,y,w,h=(float(e.get(a)) for a in ['x','y','width','height'])
   for xx in range(int(x)+2,int(x+w)-1,7):
    for yy in range(int(y)+2,int(y+h)-2,7):
     ET.SubElement(dots,'{'+ns+'}rect',x=str(xx),y=str(yy),width='1.2',height='2',fill=color,stroke='none')
   parent.insert(list(parent).index(e)+1,dots)
d=svg2rlg(io.BytesIO(ET.tostring(tree)))
single=folder/(f'PlanetScale-Nexus-Step-{args.step}.pdf' if args.preview_only else 'PlanetScale-Nexus.pdf')
c=canvas.Canvas(str(single),pagesize=(960,540))
c.setFillColorRGB(17/255,17/255,17/255);c.rect(0,0,960,540,fill=1,stroke=0)
if args.step<2:
 t=c.beginText(64*2/3,540-108*2/3);t.setFont('DeckInter',54*2/3);t.setCharSpace(-2.4*2/3)
 t.setFillColorRGB(250/255,250/255,250/255);t.textOut('How ')
 t.setFillColorRGB(243/255,88/255,21/255);t.textOut('Postgres')
 t.setFillColorRGB(250/255,250/255,250/255);t.textOut(' typically runs and scales in the cloud');c.drawText(t)
else:
 t=c.beginText(64*2/3,540-108*2/3);t.setFont('DeckInter',54*2/3);t.setCharSpace(-2.4*2/3)
 t.setFillColorRGB(250/255,250/255,250/255);t.textOut('More resources won’t fix ')
 t.setFillColorRGB(243/255,88/255,21/255);t.textOut('the Postgres bottleneck');c.drawText(t)
scale=(1312*2/3)/d.width
c.saveState();c.translate(64*2/3,540-239.36*2/3-d.height*scale);c.scale(scale,scale);renderPDF.draw(d,c,0,0);c.restoreState()
c.showPage();c.save()
if args.preview_only:
 print(single)
 sys.exit(0)
assert args.step==2, 'Only the final reveal may be merged into the deck.'
reader=PdfReader(folder/'PlanetScale-Pitch-Full.pdf');nexus=PdfReader(folder/'PlanetScale-Nexus.pdf')
assert len(reader.pages) in (11,12)
remaining=reader.pages[1:] if len(reader.pages)==11 else reader.pages[2:]
writer=PdfWriter();writer.add_page(reader.pages[0]);writer.add_page(nexus.pages[0])
for p in remaining:writer.add_page(p)
labels=['Postgres on Metal','Nexus: the common cloud Postgres capacity model','Convex','Vitalize','Autumn','Cluster architecture','Why Metal','Metal benchmarks','Neki architecture','Neki scale','Cloud deployment','Migration']
for i,label in enumerate(labels):writer.add_outline_item(label,i)
writer.add_metadata({'/Title':'PlanetScale — Full Pitch Deck','/Author':'Cole Zuckowsky'})
result=folder/'PlanetScale-Pitch-Nexus-Capacity.pdf';writer.write(result)
(folder/'PlanetScale-Pitch-Nexus.pdf').write_bytes(result.read_bytes())
(folder/'PlanetScale-Pitch-Full.pdf').write_bytes(result.read_bytes())
check=PdfReader(result);assert len(check.pages)==12
assert 'Storage I/O' in check.pages[1].extract_text()
assert 'Local NVMe SSD' in check.pages[6].extract_text()
print(result, '12 pages, Nexus second, local NVMe diagram seventh.')
