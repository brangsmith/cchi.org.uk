#!/usr/bin/env python3
"""Build one version of the website into dist/<site>/.

    python3 build.py cambridge      # or: classic
    python3 build.py --list

dist/<site>/ is a complete static site. Upload that folder as it is.

Every page gets its own real address and its own title, description and social
preview, so the pages can be found and shared one by one:

    /                 home                /news/            news
    /research/        research            /news/3/          a news item
    /research/scan/   a special interest group
    /mst/             the MSt             /people/  /cebc/  /contact/

Content (content/*.md) and images (img/) are shared by every version; each
version in sites/ supplies its own template, icons and settings (site.json).
"""
import html, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITES = ROOT / "sites"
SITE_NAME = "Cambridge Centre for Healthcare Innovation"

# page id in the template -> address, and the heading used for it in content/seo.md
PAGES = [
    ("home", "/", "Home"),
    ("research", "/research/", "Research"),
    ("education", "/mst/", "MSt"),
    ("cebc", "/cebc/", "Biomedical Campus site"),
    ("people", "/people/", "People"),
    ("news", "/news/", "News"),
    ("contact", "/contact/", "Contact"),
]


def available():
    return sorted(p.name for p in SITES.iterdir() if (p / "template.html").is_file())


def slugify(v):
    v = str(v or "").lower().replace("&", " and ")
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", v))


def parse_item(text):
    """First heading, then '- key: value' bullets, then the body (same shape the site reads)."""
    lines = text.replace("\r\n", "\n").split("\n")
    title = ""
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and re.match(r"^#{1,2}\s+", lines[i]):
        title = re.sub(r"^#{1,2}\s+", "", lines[i]).strip()
        i += 1
    keys, body = {}, []
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines):
        m = re.match(r"^- ([A-Za-z_]+):\s*(.*)$", lines[i])
        if not m:
            break
        keys[m.group(1).lower()] = m.group(2).strip()
        i += 1
        while i < len(lines) and re.match(r"^\s+- ", lines[i]):
            i += 1
    body = "\n".join(lines[i:]).strip()
    return title, keys, body


def plain(md, limit=155):
    """First paragraph of some markdown as plain text for a description."""
    for para in re.split(r"\n\s*\n", md):
        p = para.strip()
        if not p or p.startswith(("#", "!", "|", "- ", "* ", ">")):
            continue
        p = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", p)
        p = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", p)
        p = re.sub(r"[*_`]", "", p)
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            return p if len(p) <= limit else p[: limit - 1].rsplit(" ", 1)[0] + "…"
    return ""


def read_seo():
    out, cur = {}, None
    p = ROOT / "content" / "seo.md"
    if not p.is_file():
        return out
    for line in p.read_text().split("\n"):
        h = re.match(r"^##\s+(.*)$", line)
        if h:
            cur = h.group(1).strip()
            continue
        m = re.match(r"^- description:\s*(.*)$", line)
        if cur and m:
            out[cur] = m.group(1).strip()
    return out


def read_site_md():
    p = ROOT / "content" / "site.md"
    if not p.is_file():
        return {}
    return parse_item(p.read_text())[1]


def numbered(dirname):
    d = ROOT / "content" / dirname
    for f in sorted(d.glob("[0-9][0-9][0-9].md")):
        title, keys, body = parse_item(f.read_text())
        if title:
            yield int(f.stem), title, keys, body


def page_head(doc, title, desc, url, base, image, noindex=False, extra=""):
    q = lambda s: html.escape(s, quote=True)
    doc = re.sub(r"<title>.*?</title>", "<title>%s</title>" % html.escape(title), doc, count=1, flags=re.S)
    meta = [
        '<meta name="description" content="%s">' % q(desc),
        '<link rel="canonical" href="%s">' % q(base + url),
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="%s">' % q(SITE_NAME),
        '<meta property="og:title" content="%s">' % q(title),
        '<meta property="og:description" content="%s">' % q(desc),
        '<meta property="og:url" content="%s">' % q(base + url),
        '<meta property="og:image" content="%s">' % q(base + image),
        '<meta name="twitter:card" content="summary">',
    ]
    if noindex:
        meta.append('<meta name="robots" content="noindex">')
    marker = '<meta name="theme-color"'
    i = doc.index(marker); j = doc.index(">", i) + 1
    return doc[:j] + "\n" + "\n".join(meta) + extra + doc[j:]


def write(out, url, text):
    d = out / url.strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(text)


def build(name):
    src = SITES / name
    if name not in available():
        sys.exit(f"Unknown site '{name}'. Choose one of: {', '.join(available())}")
    cfg = json.loads((src / "site.json").read_text())
    base = cfg["base_url"].rstrip("/")
    logo = (ROOT / "src" / "chi-logo.b64").read_text().strip()

    template = (src / "template.html").read_text()
    if template.count("__CHI__") != 1:
        sys.exit("template.html must contain __CHI__ exactly once")
    page = template.replace("__CHI__", logo)

    # template = head (title, fonts, style) + the app markup that starts at <div id="app"
    i = page.index('<div id="app"')
    head, body = page[:i], page[i:]
    base_doc = (
        '<!doctype html>\n<html lang="en-GB" data-theme="%s">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">\n'
        '<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">\n'
        '<meta name="theme-color" content="%s">\n'
    ) % (cfg["data_theme"], cfg["theme_color"])
    base_doc += head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n"

    # titles of the fixed pages come from the template, descriptions from content/seo.md
    titles = dict((m.group(1), m.group(2)) for m in re.finditer(r'<section id="p-([a-z0-9]+)" data-page="[^"]*" data-title="([^"]*)"', template))
    seo = read_seo()
    image = "/img/icon-512.png"
    site = read_site_md()

    out = ROOT / "dist" / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT / "img", out / "img")
    shutil.copytree(src / "icons", out / "img", dirs_exist_ok=True)
    shutil.copytree(ROOT / "content", out / "content", ignore=shutil.ignore_patterns("README.md", "seo.md"))

    urls = []
    for pid, url, seo_key in PAGES:
        desc = seo.get(seo_key, "")
        title = SITE_NAME if pid == "home" else "%s · %s" % (titles.get(pid, seo_key), SITE_NAME)
        extra = ""
        if pid == "home":
            org = {"@context": "https://schema.org", "@type": "Organization", "name": SITE_NAME, "url": base + "/",
                   "logo": base + image, "parentOrganization": {"@type": "Organization", "name": "Engineering Design Centre, Department of Engineering, University of Cambridge"}}
            same = [u for u in (site.get("linkedin", ""), site.get("x", "")) if re.match(r"^https?://[^/]+/.+", u)]
            if same:
                org["sameAs"] = same
            extra = '\n<script type="application/ld+json">%s</script>' % json.dumps(org, ensure_ascii=False).replace("</", "<\\/")
        text = page_head(base_doc, title, desc, url, base, image, extra=extra)
        if pid == "home":
            (out / "index.html").write_text(text)
        else:
            write(out, url, text)
        urls.append(url)

    for n, title, keys, body in numbered("news"):
        if keys.get("hidden", "").lower() == "true" or keys.get("link"):
            continue  # hidden items and items that link elsewhere have no page of their own
        url = "/news/%d/" % n
        desc = keys.get("summary") or plain(body) or seo.get("News", "")
        write(out, url, page_head(base_doc, "%s · %s" % (title, SITE_NAME), desc, url, base, image))
        urls.append(url)

    for n, title, keys, body in numbered("sigs"):
        url = "/research/%s/" % slugify(keys.get("short") or title)
        desc = keys.get("summary") or plain(body) or seo.get("Research", "")
        write(out, url, page_head(base_doc, "%s · %s" % (title, SITE_NAME), desc, url, base, image))
        urls.append(url)

    # a page for addresses that don't exist (point the host's "404 page" setting at /404.html)
    (out / "404.html").write_text(page_head(base_doc, "Page not found · " + SITE_NAME, "That address doesn't match anything on this site.", "/404.html", base, image, noindex=True))

    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join("  <url><loc>%s</loc></url>\n" % html.escape(base + u) for u in urls) + "</urlset>\n")
    (out / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base)
    print("built dist/%s  (%d pages, %s)" % (name, len(urls) + 1, base))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    if sys.argv[1] == "--list":
        print("\n".join(available()))
    else:
        build(sys.argv[1])
