#!/bin/zsh
set -eu
cd "${0:A:h}"
python3 - <<'PY'
from pathlib import Path
from urllib.request import urlopen
import subprocess
import sys
import time
import webbrowser

root = Path.cwd()
deck = 'Meridian-PlanetScale.html'
expected = (root / deck).read_bytes()
for port in range(8765, 8775):
    base = f'http://127.0.0.1:{port}'
    try:
        with urlopen(f'{base}/{deck}', timeout=1) as response:
            if response.read() == expected:
                break
        continue
    except Exception:
        process = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        for _ in range(20):
            time.sleep(.1)
            try:
                with urlopen(f'{base}/{deck}', timeout=1) as response:
                    if response.read() == expected:
                        break
            except Exception:
                continue
        else:
            continue
        break
else:
    raise SystemExit('No free presentation port found between 8765 and 8774.')
url = f'{base}/{deck}?cloud&present#/opening'
print(f'Presentation: {url}')
print('Press S in the slide window for presenter notes. Allow localhost popups.')
print('In Zoom, share only the slide window; keep the presenter window private.')
webbrowser.open(url)
PY
