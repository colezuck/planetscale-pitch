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
shutil.copyfile(ROOT / "assets/site-prism-color.svg", OUT / "assets/site-prism-color.svg")
shutil.copyfile(ROOT / "assets/planetscale-symbol-white.svg", OUT / "assets/planetscale-symbol-white.svg")

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
    body { margin: 0; min-height: 100vh; background: #08080a url('/assets/site-prism-color.svg') center / cover no-repeat; color: #fff; }
    main { display: flex; min-height: 100vh; width: min(100% - 48px, 1160px); margin: auto; padding: 48px 0; flex-direction: column; align-items: flex-start; justify-content: center; }
    .intro { background: #08080a; padding: 34px 40px 40px; max-width: 100%; }
    h1 { margin: 0 0 30px; font-size: clamp(42px, 6.5vw, 88px); font-weight: 700; letter-spacing: -.055em; line-height: 1.04; }
    h1 span { margin-left: .12em; font-weight: 450; }
    a { display: inline-flex; align-items: center; gap: 14px; min-height: 72px; padding: 10px 18px 10px 10px; background: #f9bf00; color: #08080a; text-decoration: none; font-size: 18px; font-weight: 700; line-height: 1.2; transition: background .18s, transform .18s; }
    a:hover { background: #ffe800; transform: translateY(-3px); }
    a:focus-visible { outline: 3px solid #fff; outline-offset: 4px; }
    .brand-mark { display: grid; place-items: center; width: 52px; height: 52px; flex: none; background: #08080a; }
    .brand-mark img { display: block; width: 31px; height: 31px; }
    .arrow { margin-left: 14px; font-size: 25px; line-height: 1; }
    @media (max-width: 600px) { main { width: min(100% - 32px, 1160px); } .intro { padding: 28px 24px 24px; } h1 { font-size: clamp(38px, 10vw, 62px); } a { font-size: 16px; } .arrow { margin-left: 2px; } }
  </style>
</head>
<body>
  <main>
    <div class="intro">
      <h1>Cole Zuckowsky <span>| GTM</span></h1>
      <a href="/planetscale/">
        <span class="brand-mark"><img src="/assets/planetscale-symbol-white.svg" alt=""></span>
        PlanetScale Pitch Deck <span class="arrow" aria-hidden="true">↗</span>
      </a>
    </div>
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
