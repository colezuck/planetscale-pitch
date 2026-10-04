from pathlib import Path
import io,sys
sys.path.insert(0,'/private/tmp/ps-pdf-libs')
from fontTools.ttLib import TTFont as FontFile
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from pypdf import PdfReader,PdfWriter
root=Path('/Users/colezuckowsky/Documents/ChatGPT/GTM/planetscale-pitch')
folder=Path(__file__).resolve().parents[1]
font=FontFile(root/'assets/inter.woff2');font.flavor=None
font=instantiateVariableFont(font,{'wght':500},inplace=True)
fontpath=Path('/private/tmp/ps-hero-inter.ttf');font.save(fontpath)
pdfmetrics.registerFont(TTFont('HeroInter',str(fontpath)))
c=canvas.Canvas(str(folder/'PlanetScale-Hero.pdf'),pagesize=(960,540))
c.setFillColorRGB(17/255,17/255,17/255);c.rect(0,0,960,540,stroke=0,fill=1)
logo=svg2rlg(str(root/'assets/planetscale-white.svg'))
c.saveState();c.translate(360,306.42);c.scale(240/logo.width,240/logo.width);renderPDF.draw(logo,c,0,0);c.restoreState()
size=112*2/3
first='Postgres on ';last='Metal'
tracking=-5.2*2/3
width=pdfmetrics.stringWidth(first+last,'HeroInter',size)+tracking*(len(first+last)-1)
x=(960-width)/2
y=206.73
t=c.beginText(x,y);t.setFont('HeroInter',size);t.setCharSpace(tracking)
t.setFillColorRGB(250/255,250/255,250/255);t.textOut(first)
t.setFillColorRGB(243/255,88/255,21/255);t.textOut(last);c.drawText(t)
c.showPage();c.save()
reader=PdfReader(folder/'PlanetScale-Pitch-Full.pdf');hero=PdfReader(folder/'PlanetScale-Hero.pdf')
writer=PdfWriter();writer.add_page(hero.pages[0])
for p in reader.pages[1:]:writer.add_page(p)
labels=['Postgres on Metal','Convex','Vitalize','Autumn','Cluster architecture','Why Metal','Metal benchmarks','Neki architecture','Neki scale','Cloud deployment','Migration']
for i,label in enumerate(labels):writer.add_outline_item(label,i)
writer.add_metadata({'/Title':'PlanetScale — Full Pitch Deck','/Author':'Cole Zuckowsky'})
result=folder/'PlanetScale-Pitch-Hero.pdf';writer.write(result)
(folder/'PlanetScale-Pitch-Full.pdf').write_bytes(result.read_bytes())
check=PdfReader(result)
assert len(check.pages)==11
assert 'Local NVMe SSD' in check.pages[5].extract_text()
assert 'Neki' not in check.pages[0].extract_text()
print(result, '11 pages, local NVMe artwork present on page 6.')
