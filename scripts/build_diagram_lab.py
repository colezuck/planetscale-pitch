"""Build the diagram lab from the canonical example and shared deck templates."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'decks/diagram-lab'
(LAB / 'diagrams').mkdir(exist_ok=True)
STARTER = ROOT / '.agents/skills/planetscale-pitch-design/assets/starter'
for name in ['build.py', 'package.py']:
    shutil.copyfile(STARTER / name, LAB / name)
shutil.copyfile(ROOT / 'shared/presentation/examples/capacity-model.json', LAB / 'diagrams/capacity-model.json')
for name in ['build.py', 'package.py']:
    subprocess.run([sys.executable, str(LAB / name)], check=True, cwd=ROOT)
