"""Build audience or local presenter slide data from content.json."""
from pathlib import Path
import argparse
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--presenter', action='store_true')
args = parser.parse_args()
shared = ROOT.parents[1] / 'shared/presentation'
if shared.is_dir():
    (ROOT / 'runtime').mkdir(exist_ok=True)
    for filename in ['diagram_scene.py', 'diagram-motion.js', 'diagram-motion.css']:
        shutil.copyfile(shared / filename, ROOT / 'runtime' / filename)
sys.path.insert(0, str(ROOT / 'runtime'))
from diagram_scene import compile_scene

records = json.loads((ROOT / 'content.json').read_text())
if not isinstance(records, list) or not records:
    raise SystemExit('content.json must contain a nonempty slide array')
# Hidden slides remain editable in the source, but never enter either deliverable.
records = [record for record in records if not record.get('hidden', False)]
slides = []
ids = set()
scene_ids = set()
for record in records:
    if not all(isinstance(record.get(key), str) and record[key].strip() for key in ['id', 'label', 'theme']):
        raise SystemExit('Each slide needs nonempty id, label, and theme strings')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', record['id']) or record['id'] in ids:
        raise SystemExit('Slide IDs must be unique lowercase URL-safe names')
    ids.add(record['id'])
    if ('html' in record) == ('diagramFile' in record):
        raise SystemExit('Provide either html or diagramFile, exclusively')
    slide = {key: record[key] for key in ['id', 'label', 'theme']}
    if 'diagramFile' in record:
        source = (ROOT / record['diagramFile']).resolve()
        if ROOT not in source.parents:
            raise SystemExit('Diagram source must be inside the deck')
        scene = json.loads(source.read_text())
        if scene['id'] in scene_ids:
            raise SystemExit('Diagram IDs must be unique across the deck')
        scene_ids.add(scene['id'])
        slide['html'] = record.get('beforeHtml', '') + compile_scene(scene) + record.get('afterHtml', '')
    else:
        if not isinstance(record['html'], str) or not record['html'].strip():
            raise SystemExit('Slide html must be nonempty')
        slide['html'] = record['html']
        for token, asset in {'{{METAL_PATH}}': 'metal-path.svg', '{{DEPOT_LATENCY}}': 'depot-latency.svg'}.items():
            if token in slide['html']:
                slide['html'] = slide['html'].replace(token, (ROOT / 'assets' / asset).read_text())
    slides.append(slide)
output = ROOT
if args.presenter:
    script = json.loads((ROOT / 'private/speaker-outline.json').read_text())
    if set(script) != ids or not all(isinstance(points, list) and all(isinstance(point, str) for point in points) for points in script.values()):
        raise SystemExit('Presenter outline must map every slide ID to an array of strings')
    for slide in slides:
        slide['notes'] = '\n'.join('• ' + point for point in script[slide['id']])
    output = ROOT / 'private'
    output.mkdir(exist_ok=True)
(output / 'slides.js').write_text('window.PITCH_SLIDES = ' + json.dumps(slides, ensure_ascii=False, indent=2) + ';\n')
print(f'Built {len(slides)} slides: {"presenter" if args.presenter else "audience"}')
