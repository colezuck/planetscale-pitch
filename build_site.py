"""Build the audience-only Cloudflare Pages upload folder."""
from pathlib import Path
import re, shutil
root=Path(__file__).resolve().parent
out=root/'dist';out.mkdir(exist_ok=True)
page=(root/'Meridian-PlanetScale.html').read_text()
assert '"notes":' not in page and 'id="notes"' not in page
page=re.sub(r'<button id="notes".*?</button>', '', page)
page=re.sub(r'<dialog id="notes-dialog".*?</dialog>', '', page, flags=re.S)
page=page.replace('S &nbsp; Speaker view with notes and timer','PDF &nbsp; Download a copy')
page=page.replace('For speaker view, serve this folder locally. For a PDF, open <a href="?print-pdf">print layout</a> and print in landscape with background graphics enabled.', 'Use the arrow keys to move through the slides. <a href="/PlanetScale-Postgres-on-Metal.pdf" download>Download the PDF</a>.')
page=page.replace('<button id="fullscreen"', '<a href="/PlanetScale-Postgres-on-Metal.pdf" download style="color:inherit;text-decoration:none;padding:5px 8px">PDF ↓</a><button id="fullscreen"')
(out/'index.html').write_text(page)
(out/'Meridian-PlanetScale.html').write_text(page)
shutil.copyfile(root/'output/pdf/PlanetScale-Postgres-on-Metal.pdf',out/'PlanetScale-Postgres-on-Metal.pdf')
(out/'_headers').write_text('/\n  Cache-Control: no-cache\n/*.html\n  Cache-Control: no-cache\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n')
print('Built dist/: audience deck + PDF, no speaker scripts or notes.')
