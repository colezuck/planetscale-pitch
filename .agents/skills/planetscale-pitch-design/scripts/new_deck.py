"""Create a clean Reveal.js deck using the repository's proven visual shell."""
from pathlib import Path
import argparse
import html
import json
import re
import shutil

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True, help='Lowercase hyphenated folder name under decks/')
parser.add_argument('--title', required=True)
parser.add_argument('--root', type=Path, default=REPO, help='Output repository root; useful for isolated previews')
args = parser.parse_args()
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.name):
    raise SystemExit('Use a lowercase hyphenated deck name')
reference = REPO / 'decks/postgres-metal'
target = args.root.resolve() / 'decks' / args.name
# Existing planning README is allowed; any implementation or unexpected content is not.
if target.exists() and any(p.name != 'README.md' for p in target.iterdir()):
    raise SystemExit(f'Refusing to overwrite existing deck: {target}')
css = (reference / 'theme.css').read_text()
base = css.split('/* Opening hero:', 1)[0]
cover = '/* Opening hero:' + css.split('/* Opening hero:', 1)[1].split('/* Nexus:', 1)[0]
controls = '/* Presentation UI is outside the slide canvas. */' + css.split('/* Presentation UI is outside the slide canvas. */', 1)[1].split('/* Customer proof:', 1)[0]
app = (reference / 'app.js').read_text()
app = app.replace('deck.initialize().then(()=>{updatePosition();updateNexusState();updateIntercomState();});', 'deck.initialize().then(updatePosition);')
app = '\n'.join(line for line in app.splitlines() if not line.startswith(('const optionalSlides', 'function updateNexusState', 'function updateIntercomState')) and not ('deck.on(' in line and ('updateNexusState' in line or 'updateIntercomState' in line))) + '\n'
app = re.sub(r'^const slides = .*?;$', 'const slides = window.PITCH_SLIDES;', app, flags=re.M)
if 'updateNexusState' in app or 'updateIntercomState' in app or 'optionalSlides' in app:
    raise SystemExit('Reference runtime changed; update shell extraction before creating a deck')
app = app.replace('plugins:hasNotes ? [RevealNotes] : []', 'plugins:[PlanetScaleDiagrams.createPlugin(), ...(hasNotes ? [RevealNotes] : [])]')
# Keep Previous/Next usable when the first or last slide still has fragment steps.
app = app.replace("document.getElementById('previous').disabled=i===0;document.getElementById('next').disabled=i===slides.length-1;", "const f=deck.availableFragments();document.getElementById('previous').disabled=i===0&&!f.prev;document.getElementById('next').disabled=i===slides.length-1&&!f.next;")
app += "deck.on('fragmentshown',updatePosition);\ndeck.on('fragmenthidden',updatePosition);\n"
index = (reference / 'index.html').read_text()
index = index.replace('<link rel="stylesheet" href="theme.css">', '<link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="runtime/diagram-motion.css">')
index = index.replace('<script src="app.js"></script>', '<script src="runtime/diagram-motion.js"></script><script src="app.js"></script>')
index = re.sub(r'<title>.*?</title>', '<title>' + html.escape(args.title) + '</title>', index)
target.mkdir(parents=True, exist_ok=True)
(target / 'assets').mkdir()
(target / 'vendor').mkdir()
(target / 'runtime').mkdir()
for filename in ['diagram_scene.py', 'diagram-motion.js', 'diagram-motion.css']:
    shutil.copyfile(REPO / 'shared/presentation' / filename, target / 'runtime' / filename)
for filename in ['inter.woff2', 'Inter-LICENSE.txt', 'planetscale-white.svg', 'planetscale-black.svg', 'planetscale-symbol-white.svg', 'postgresql.svg']:
    shutil.copyfile(reference / 'assets' / filename, target / 'assets' / filename)
for filename in ['reveal.js', 'reveal.css', 'notes.js', 'LICENSE']:
    shutil.copyfile(reference / 'vendor' / filename, target / 'vendor' / filename)
for filename in ['build.py', 'package.py']:
    shutil.copyfile(SKILL / 'assets/starter' / filename, target / filename)
(target / 'index.html').write_text(index)
(target / 'app.js').write_text(app)
(target / 'theme.css').write_text((base + cover + controls).rstrip() + '\n')
(target / 'content.json').write_text(json.dumps([{'id':'opening', 'label':args.title, 'theme':'opening', 'html':'<div class="opening-hero"><div class="cover-brand"><img src="assets/planetscale-white.svg" alt="PlanetScale"></div><h1>' + html.escape(args.title) + '</h1></div>'}], ensure_ascii=False, indent=2) + '\n')
readme = target / 'README.md'
if not readme.exists():
    readme.write_text(f'# {args.title}\n\nGenerated visual shell. Author the slide plan and content before presenting.\n\nRun `python3 build.py` and `python3 package.py` from this folder. Edit `content.json`, `theme.css`, `app.js`, and `assets/`. Generated audience data is `slides.js`; portable output is `Audience.html`. Presenter scripts belong in ignored `private/`. This deck is not deployed automatically.\n')
print(f'Created clean deck shell: {target}')
