"""Package the editable sources as a portable HTML file and a static PDF backup.

Run after capturing the final 16:9 slide PNGs through the browser QA workflow.
The PDF is a visual snapshot with slide bookmarks.
"""
from pathlib import Path
import base64
import json
import re

ROOT = Path(__file__).resolve().parent

def data_uri(relative):
    path = ROOT / relative
    mime = {'svg': 'image/svg+xml', 'woff2': 'font/woff2', 'png': 'image/png'}[path.suffix[1:]]
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()

html = (ROOT / 'index.html').read_text()
css = (ROOT / 'theme.css').read_text().replace('assets/inter.woff2', data_uri('assets/inter.woff2'))
html = html.replace('<link rel="stylesheet" href="vendor/reveal.css">', '<style>' + (ROOT / 'vendor/reveal.css').read_text() + '</style>')
html = html.replace('<link rel="stylesheet" href="theme.css">', '<style>' + css + '</style>')
for filename in ['vendor/reveal.js', 'vendor/notes.js', 'slides.js', 'app.js']:
    code = (ROOT / filename).read_text()
    if filename == 'app.js':
        dynamic = "assets/planetscale-${light?'black':'white'}.svg"
        replacement = "${light ? '" + data_uri('assets/planetscale-black.svg') + "' : '" + data_uri('assets/planetscale-white.svg') + "'}"
        code = code.replace(dynamic, replacement)
    for image in ['postgresql.svg', 'planetscale-black.svg', 'planetscale-white.svg', 'cash-app.svg', 'neki-cat.svg', 'vitalize.svg', 'planetscale-white.png', 'vitalize-query-latency.png', 'convex-white.svg', 'autumn.svg', 'convex-symbol-color.svg', 'convex-wordmark-white.svg', 'convex-original-results.png', 'vitalize-symbol.svg']:
        code = code.replace('assets/' + image, data_uri('assets/' + image))
    code = re.sub(r'</script', r'<\\/script', code, flags=re.I)
    html = html.replace(f'<script src="{filename}"></script>', '<script>' + code + '</script>')
html = html.replace('assets/postgresql.svg', data_uri('assets/postgresql.svg'))
(ROOT / 'Meridian-PlanetScale.html').write_text(html)

import sys
if '--html-only' in sys.argv:
    print('Packaged portable HTML.')
    sys.exit(0)

from reportlab.pdfgen import canvas
from pypdf import PdfReader

slides = json.loads((ROOT / 'qa/content.json').read_text())
links = json.loads((ROOT / 'qa/links.json').read_text())
pdf = ROOT / 'Meridian-PlanetScale.pdf'
c = canvas.Canvas(str(pdf), pagesize=(960, 540))
c.setTitle('PlanetScale — Postgres on Metal')
c.setAuthor('Cole Zuckowsky — independent interview sample')
c.setSubject('Fictional B2B sales pitch. Static snapshot of the interactive HTML deck.')
for i, slide in enumerate(slides, 1):
    png = ROOT / f'qa/slide-{i:02}.png'
    if not png.exists():
        raise FileNotFoundError(png)
    c.drawImage(str(png), 0, 0, width=960, height=540)
    c.bookmarkPage(slide['id'])
    c.addOutlineEntry(f'{i:02}. {slide["label"]}', slide['id'])
    for link in links.get(slide['id'], []):
        x, y, w, h = (link[k] * 2 / 3 for k in ('x', 'y', 'w', 'h'))
        c.linkURL(link['url'], (x, 540-y-h, x+w, 540-y), relative=0, thickness=0)
    c.showPage()
c.save()
reader = PdfReader(str(pdf))
assert len(reader.pages) == len(slides)
assert all(float(p.mediabox.width) == 960 and float(p.mediabox.height) == 540 for p in reader.pages)
print(f'Packaged {len(slides)} slides. PDF: {pdf.stat().st_size:,} bytes. HTML: {len(html):,} characters.')
