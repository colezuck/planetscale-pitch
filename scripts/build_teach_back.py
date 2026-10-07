"""Build the audience deck, or local presenter from the rehearsal source."""
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'decks/teach-back'
parser = argparse.ArgumentParser()
parser.add_argument('--presenter', action='store_true')
args = parser.parse_args()

if args.presenter:
    source = (ROOT / 'interview/teach-back/script-outline.md').read_text()
    sections = re.split(r'^## Slide \d+ — .*$', source, flags=re.M)[1:]
    slides = [slide for slide in json.loads((DECK / 'content.json').read_text()) if not slide.get('hidden', False)]
    if len(sections) != len(slides):
        raise SystemExit('Speaking outline needs one numbered section per slide')
    script = {}
    for slide, section in zip(slides, sections):
        section = section.split('\n## ', 1)[0]
        points = [re.sub(r'^[-*]\s+', '', re.sub(r'\*\*([^*]+)\*\*', r'\1', paragraph)).strip('“”')
                  for paragraph in re.split(r'\n\s*\n|\n(?=[-*]\s+)', section.strip()) if paragraph.strip()]
        script[slide['id']] = points
    (DECK / 'private').mkdir(exist_ok=True)
    (DECK / 'private/speaker-outline.json').write_text(json.dumps(script, ensure_ascii=False, indent=2) + '\n')

for name in ['build.py', 'package.py']:
    command = [sys.executable, str(DECK / name)]
    if args.presenter:
        command.append('--presenter')
    subprocess.run(command, check=True, cwd=ROOT)
