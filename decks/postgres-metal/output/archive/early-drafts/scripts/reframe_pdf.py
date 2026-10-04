from pathlib import Path
import io
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject
from reportlab.pdfgen import canvas
folder=Path(__file__).resolve().parents[1]
source=folder/'PlanetScale-Pitch-Original-Export.pdf'
target=folder/'PlanetScale-Pitch-Full.pdf'
if not source.exists(): source.write_bytes(target.read_bytes())
reader=PdfReader(source)
writer=PdfWriter()
bg=io.BytesIO()
c=canvas.Canvas(bg,pagesize=(960,540));c.setFillColorRGB(17/255,17/255,17/255);c.rect(0,0,960,540,fill=1,stroke=0);c.showPage();c.save()
for page in reader.pages:
 page.cropbox=RectangleObject((1,1,959,539))
 framed=PdfReader(io.BytesIO(bg.getvalue())).pages[0]
 framed.merge_transformed_page(page,Transformation().scale(.96).translate(19.2,-16))
 writer.add_page(framed)
for i,label in enumerate(['Postgres on Metal','Convex','Vitalize','Autumn','Cluster architecture','Why Metal','Metal benchmarks','Neki architecture','Neki scale','Cloud deployment','Migration']):writer.add_outline_item(label,i)
writer.add_metadata({'/Title':'PlanetScale — Full Pitch Deck','/Author':'Cole Zuckowsky'})
writer.write(target)
assert len(PdfReader(target).pages)==11
print(target)
