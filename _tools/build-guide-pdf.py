"""Build assets/Recert-Getting-Started.pdf from getting-started.md.

Run from anywhere: python _tools/build-guide-pdf.py
Needs: pip install markdown; Google Chrome installed (headless print-to-PDF).
Jekyll ignores _tools/, so nothing here is published except the PDF it writes.
"""
import re
import subprocess
import tempfile
from pathlib import Path

import markdown

SITE = Path(__file__).resolve().parent.parent
SRC = SITE / "getting-started.md"
OUT = SITE / "assets" / "Recert-Getting-Started.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
@page { size: 11in 8.5in; margin: 0.45in 0.6in 0.5in; }
body { font-family: "Segoe UI", Arial, sans-serif; color: #172b4d; font-size: 11pt; line-height: 1.35; margin: 0; }
h1 { font-size: 30pt; margin: 1.6in 0 10pt; }
h2 { font-size: 19pt; margin: 0 0 8pt; break-before: page; color: #0c3e8a; }
p, li { margin: 0 0 3pt; }
ol, ul { margin: 0 0 8pt; padding-left: 22pt; }
ol > li::marker { color: #de350b; font-weight: 700; }
code { font-family: Consolas, monospace; background: #f1f2f4; padding: 0 3pt; }
a { color: #0c66e4; text-decoration: none; }
.shot img { display: block; max-width: 100%; max-height: 4.9in; margin: 6pt 0 8pt;
            border: 1px solid #d0d4da; border-radius: 4px; }
.grp { break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 10.5pt; }
th, td { text-align: left; vertical-align: top; padding: 5pt 7pt; border-bottom: 1px solid #dcdfe4; }
th { background: #f1f2f4; }
"""


def main():
    text = SRC.read_text(encoding="utf-8")
    text = re.sub(r"\A---.*?---\s*", "", text, flags=re.S)          # front matter
    text = re.sub(r"<style>.*?</style>\s*", "", text, flags=re.S)    # page-only CSS
    text = re.sub(r'<a class="pdf".*?</a>\s*', "", text)             # link to itself
    # the demo video cannot live in a PDF; leave a pointer to it instead
    text = re.sub(r'<div class="demo".*?</div>\s*', "", text, flags=re.S)
    text = text.replace(
        "**How to read the pictures.**",
        "**A one-minute demo video** of the whole flow is at "
        "https://recert.dev/getting-started.html#demo\n\n**How to read the pictures.**",
    )
    # kramdown's {:start="N"} is not python-markdown syntax; mark it and fix after
    text = re.sub(r'\{:start="(\d+)"\}\n', r"OLSTART\1\n\n", text)
    # site-relative links become absolute, so they work from a downloaded PDF
    text = re.sub(r"\]\((?!https?:|#|assets/)([^)]+)\)", r"](https://recert.dev/\1)", text)
    # python-markdown needs 4-space indents for nested lists; kramdown accepts 3
    text = re.sub(r"^   - ", "    - ", text, flags=re.M)
    text = re.sub(r"^     (?=\S)", "      ", text, flags=re.M)

    html = markdown.markdown(text, extensions=["tables"])
    html = re.sub(r"<p>OLSTART(\d+)</p>\s*<ol>", r'<ol start="\1">', html)
    # keep each picture with the numbered steps under it, so pages break between groups
    html = re.sub(r'(<p><a class="shot".*?</p>\s*<ol.*?</ol>)', r'<div class="grp">\1</div>', html, flags=re.S)
    html = html.replace('src="assets/', f'src="{(SITE / "assets").as_uri()}/')
    html = html.replace("<h2>Reminders", '<h2 style="break-before: page">Reminders')
    # keep the three short closing sections together instead of one page each
    for heading in ("Where the data lives", "Troubleshooting"):
        html = html.replace(f"<h2>{heading}", f'<h2 style="break-before: auto; margin-top: 16pt">{heading}')

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Recert — Getting started</title><style>{CSS}</style></head><body>
{html}
</body></html>"""

    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "guide.html"
        page.write_text(doc, encoding="utf-8")
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={Path(tmp) / 'prof'}",
            f"--print-to-pdf={OUT}", page.as_uri(),
        ], check=True, capture_output=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
