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
(OUT / "assets").mkdir()

(DECK / "index.html").write_text(page)
(DECK / "Meridian-PlanetScale.html").write_text(page)
shutil.copyfile(ROOT / "output/pdf" / PDF_NAME, DECK / PDF_NAME)
shutil.copyfile(ROOT / "assets/site-background.webp", OUT / "assets/site-background.webp")

(OUT / "index.html").write_text("""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cole Zuckowsky | GTM</title>
  <meta name="description" content="Cole Zuckowsky | GTM">
  <style>
    :root { font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; background: #182641 url('/assets/site-background.webp') center / 100% 100% no-repeat; color: #fff; }
    body::before { content: ''; position: fixed; inset: 0; background: linear-gradient(90deg, rgba(9, 14, 30, .48), rgba(9, 14, 30, .04) 80%), linear-gradient(0deg, rgba(9, 14, 30, .22), transparent 60%); pointer-events: none; }
    main { position: relative; display: flex; min-height: 100vh; width: min(100% - 48px, 1100px); margin: auto; padding: 56px 0; flex-direction: column; align-items: flex-start; justify-content: center; }
    h1 { margin: 0 0 34px; font-size: clamp(44px, 7vw, 96px); font-weight: 700; letter-spacing: -.055em; line-height: 1.02; text-shadow: 0 2px 24px rgba(0, 0, 0, .25); }
    h1 span { margin-left: .12em; font-weight: 450; }
    a { display: inline-flex; align-items: center; gap: 26px; padding: 17px 24px; border-radius: 999px; background: rgba(255, 255, 255, .92); color: #101827; text-decoration: none; font-size: 17px; font-weight: 650; box-shadow: 0 10px 40px rgba(10, 14, 30, .18); transition: background .18s, transform .18s; }
    a:hover { background: #fff; transform: translateY(-2px); }
    a:focus-visible { outline: 3px solid #fff; outline-offset: 4px; }
    @media (max-width: 600px) { h1 { font-size: clamp(40px, 10vw, 64px); } a { font-size: 16px; } }
  </style>
</head>
<body>
  <main>
    <h1>Cole Zuckowsky <span>| GTM</span></h1>
    <a href="/planetscale/">
      PlanetScale Pitch Deck <span aria-hidden="true">↗</span>
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
