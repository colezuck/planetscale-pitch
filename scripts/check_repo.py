"""Check repository navigation and presentation file boundaries using the standard library."""
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'decks/postgres-metal'
errors = []
excluded = {'node_modules', '.git', '.wrangler', 'dist', 'private', 'references'}
for document in ROOT.rglob('*.md'):
    if excluded.intersection(document.relative_to(ROOT).parts):
        continue
    for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
        target = raw.strip().split(' "', 1)[0].strip('<>')
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        target = unquote(target.split('#', 1)[0].split('?', 1)[0])
        if target and not (document.parent / target).exists():
            errors.append(f'{document.relative_to(ROOT)}: missing link {target}')

for deck in (ROOT / 'decks').iterdir():
    if not (deck / 'index.html').is_file():
        continue
    for target in re.findall(r'(?:src|href)="([^"]+)"', (deck / 'index.html').read_text()):
        if not target.startswith(('?', '#', 'http:', 'https:', 'data:')) and not (deck / target).is_file():
            errors.append(f'{deck.name} index: missing {target}')
    public = deck / 'slides.js'
    if not public.is_file() or '"notes":' in public.read_text():
        errors.append(f'{deck.name}: audience data missing or contains presenter notes')

site = ROOT / 'dist'
if site.exists():
    for path in site.rglob('*'):
        if path.is_file() and (path.name in {'Presenter.html', 'speaker-outline.json', 'speaker-notes.md'} or 'private' in path.relative_to(site).parts):
            errors.append(f'Presenter file in deployment: {path.relative_to(ROOT)}')
        if path.suffix == '.html' and ('"notes":' in path.read_text() or 'id="notes"' in path.read_text()):
            errors.append(f'Presenter content in deployment: {path.relative_to(ROOT)}')
    for target in ['index.html', 'planetscale/index.html', 'planetscale/Meridian-PlanetScale.html', 'planetscale/PlanetScale-Postgres-on-Metal.pdf', '_redirects', '_headers']:
        if not (site / target).is_file():
            errors.append(f'Missing deployment artifact: {target}')

if errors:
    raise SystemExit('\n'.join(errors))
print('Repository links, deck dependencies, and audience/presenter boundaries checked.')
