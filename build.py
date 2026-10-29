#!/usr/bin/env python3
"""Build one version of the website into dist/<site>/.

    python3 build.py cambridge      # or: classic
    python3 build.py --list

dist/<site>/ is a complete static site (index.html, img/, content/). Upload that
folder as it is. Content (content/*.md) and images (img/) are shared by every
version; each version in sites/ only supplies its own template, icons and settings.
"""
import json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITES = ROOT / "sites"


def available():
    return sorted(p.name for p in SITES.iterdir() if (p / "template.html").is_file())


def build(name):
    src = SITES / name
    if name not in available():
        sys.exit(f"Unknown site '{name}'. Choose one of: {', '.join(available())}")
    cfg = json.loads((src / "site.json").read_text())
    logo = (ROOT / "src" / "chi-logo.b64").read_text().strip()

    template = (src / "template.html").read_text()
    if template.count("__CHI__") != 1:
        sys.exit("template.html must contain __CHI__ exactly once")
    page = template.replace("__CHI__", logo)

    # template = head (title, fonts, style) + the app markup that starts at <div id="app"
    i = page.index('<div id="app"')
    head, body = page[:i], page[i:]
    doc = (
        '<!doctype html>\n<html lang="en-GB" data-theme="%s">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<link rel="icon" href="img/favicon.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png">\n'
        '<link rel="apple-touch-icon" href="img/apple-touch-icon.png">\n'
        '<meta name="theme-color" content="%s">\n'
    ) % (cfg["data_theme"], cfg["theme_color"])
    doc += head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n"

    out = ROOT / "dist" / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "index.html").write_text(doc)
    shutil.copytree(ROOT / "img", out / "img")
    shutil.copytree(src / "icons", out / "img", dirs_exist_ok=True)
    # editor notes stay in the repo and are not published
    shutil.copytree(ROOT / "content", out / "content", ignore=shutil.ignore_patterns("README.md"))
    print(f"built dist/{name}  ({len(doc):,} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    if sys.argv[1] == "--list":
        print("\n".join(available()))
    else:
        build(sys.argv[1])
