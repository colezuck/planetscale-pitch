"""Embed the local runtime and static assets into portable HTML; no PDF export."""
from pathlib import Path
import argparse
import base64
import mimetypes
import re

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--presenter', action='store_true')
args = parser.parse_args()
asset_root = (ROOT / 'assets').resolve()
asset_pattern = re.compile(r'assets/[A-Za-z0-9_./%+@-]+\.(?:svg|png|jpe?g|webp|gif|woff2|woff)(?![A-Za-z0-9_.-])', re.I)

def embed_assets(text):
    def replace(match):
        path = (ROOT / match.group()).resolve()
        if asset_root not in path.parents or not path.is_file():
            raise SystemExit(f'Missing or outside asset: {match.group()}')
        mime = {'svg': 'image/svg+xml', 'woff2': 'font/woff2', 'woff': 'font/woff'}.get(path.suffix[1:].lower()) or mimetypes.guess_type(str(path))[0]
        return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()
    result = asset_pattern.sub(replace, text)
    if 'assets/' in result:
        raise SystemExit('Unresolved asset reference; use static assets/filename.ext paths without spaces or dynamic expressions')
    return result

html = (ROOT / 'index.html').read_text()
for filename in re.findall(r'<link rel="stylesheet" href="([^"]+)">', html):
    css = embed_assets((ROOT / filename).read_text())
    html = html.replace(f'<link rel="stylesheet" href="{filename}">', '<style>' + css + '</style>')
if not args.presenter:
    html = html.replace('<script src="vendor/notes.js"></script>', '')
    html = re.sub(r'<button id="notes".*?</button>', '', html)
    html = re.sub(r'<dialog id="notes-dialog".*?</dialog>', '', html, flags=re.S)
    html = html.replace('S &nbsp; Speaker view with notes and timer', '')
    html = re.sub(r'(?m)^[ \t]+$', '', html)
for filename in re.findall(r'<script src="([^"]+)"></script>', html):
    source = ROOT / ('private/slides.js' if args.presenter and filename == 'slides.js' else filename)
    code = embed_assets(source.read_text())
    if filename == 'slides.js' and not args.presenter and '"notes":' in code:
        raise SystemExit('Audience slide data must not contain notes')
    code = re.sub(r'</script', lambda match: '<\\/script', code, flags=re.I)
    html = html.replace(f'<script src="{filename}"></script>', '<script>' + code + '</script>')
html = embed_assets(html)
# Remaining network/outside media dependencies would defeat the portable artifact.
for reference in re.findall(r'(?:src|href)=[\\]?"([^"\\]+)', html):
    if reference.startswith(('data:', '#', '?')):
        continue
    # User-facing links are fine; unresolved source/stylesheet dependencies are not.
    if re.search(r'(?:\.(?:svg|png|jpe?g|webp|gif|woff2?|js|css))(?:[?#]|$)', reference, re.I):
        raise SystemExit(f'Unembedded dependency: {reference}')
output = ROOT / ('private/Presenter.html' if args.presenter else 'Audience.html')
output.parent.mkdir(exist_ok=True)
output.write_text(html)
print(f'Packaged {output.name}')
