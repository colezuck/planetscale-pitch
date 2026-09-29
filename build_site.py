"""Build the audience-only Cloudflare Pages upload folder."""

from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
DECK = OUT / "planetscale"
PDF_NAME = "PlanetScale-Postgres-on-Metal.pdf"
PDF_URL = f"/planetscale/{PDF_NAME}"

page = (ROOT / "Meridian-PlanetScale.html").read_text()
assert '"notes":' not in page and 'id="notes"' not in page
page = re.sub(r'<button id="notes".*?</button>', "", page)
page = re.sub(r'<dialog id="notes-dialog".*?</dialog>', "", page, flags=re.S)
page = page.replace(
    'For speaker view, serve this folder locally. For a PDF, open <a href="?print-pdf">print layout</a> and print in landscape with background graphics enabled.',
    f'Use the arrow keys to move through the slides. <a href="{PDF_URL}" download>Download the PDF</a>.',
)
page = page.replace(
    '<button id="fullscreen"',
    f'<a href="{PDF_URL}" download style="color:inherit;text-decoration:none;padding:5px 8px">PDF ↓</a><button id="fullscreen"',
)

if OUT.exists():
    shutil.rmtree(OUT)
DECK.mkdir(parents=True)

(DECK / "index.html").write_text(page)
(DECK / "Meridian-PlanetScale.html").write_text(page)
shutil.copyfile(ROOT / "output/pdf" / PDF_NAME, DECK / PDF_NAME)

(OUT / "index.html").write_text("""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cole Zuckowsky</title>
  <meta name="description" content="Selected work by Cole Zuckowsky.">
  <style>
    :root { color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; background: #111; color: #fafafa; }
    main { width: min(100% - 48px, 920px); margin: auto; padding: clamp(72px, 14vh, 150px) 0; }
    h1 { margin: 0 0 96px; font-size: clamp(42px, 7vw, 80px); letter-spacing: -.05em; line-height: 1; }
    h2 { margin: 0 0 24px; color: #a5a5a5; font-size: 13px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; }
    a { display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 24px 0; border-top: 1px solid #4a4a4a; color: inherit; text-decoration: none; font-size: clamp(20px, 3vw, 30px); }
    a:hover, a:focus-visible { color: #f35815; }
    small { display: block; margin-top: 8px; color: #a5a5a5; font-size: 14px; font-weight: 400; letter-spacing: 0; }
    .arrow { color: #f35815; }
  </style>
</head>
<body>
  <main>
    <h1>Cole Zuckowsky</h1>
    <h2>Selected work</h2>
    <a href="/planetscale/">
      <span>PlanetScale pitch deck<small>Postgres on Metal · Interactive presentation</small></span>
      <span class="arrow" aria-hidden="true">↗</span>
    </a>
  </main>
</body>
</html>
""")

(OUT / "_redirects").write_text(
    "/Meridian-PlanetScale.html /planetscale/Meridian-PlanetScale.html 301\n"
    f"/{PDF_NAME} {PDF_URL} 301\n"
)
(OUT / "_headers").write_text(
    "/\n  Cache-Control: no-cache\n"
    "/*.html\n  Cache-Control: no-cache\n"
    "/*\n  X-Content-Type-Options: nosniff\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
)
print("Built dist/: landing page, audience deck, and PDF; no speaker scripts or notes.")
