"""Switch the site from preview to live, and keep the sitemap current.

  python3 tools/go-live.py --domain keytohomes.sg     # first time: set domain, allow indexing
  python3 tools/go-live.py                             # later: just refresh sitemap.xml

What it does:
  1. Rewrites every canonical / og:url / schema link from the old base URL to https://<domain>.
  2. Removes <meta name="robots" content="noindex"> from every page (only with --domain or --index).
  3. Writes CNAME (GitHub Pages custom domain), robots.txt and sitemap.xml.
"""
import argparse, datetime, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_BASES = ["https://louistcc-stack.github.io/Keytohome"]
PAGES_PY = os.path.join(ROOT, "tools", "pages.py")


def html_files():
    for d, _, files in os.walk(ROOT):
        if "/.git" in d or "/tools" in d:
            continue
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def current_base():
    m = re.search(r'^SITE = "([^"]+)"', open(PAGES_PY).read(), re.M)
    return m.group(1)


def lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", help="your own domain, e.g. keytohomes.sg")
    ap.add_argument("--index", action="store_true", help="allow indexing without changing the domain")
    a = ap.parse_args()

    base = current_base()
    if a.domain:
        new = "https://" + a.domain.strip().strip("/").removeprefix("https://").removeprefix("http://")
        for f in list(html_files()) + [PAGES_PY]:
            s = open(f, encoding="utf-8").read()
            for old in OLD_BASES + [base]:
                s = s.replace(old, new)
            open(f, "w", encoding="utf-8").write(s)
        open(os.path.join(ROOT, "CNAME"), "w").write(new.removeprefix("https://") + "\n")
        base = new
        print("domain set to", new)

    if a.domain or a.index:
        n = 0
        for f in html_files():
            s = open(f, encoding="utf-8").read()
            t = re.sub(r'<meta name="robots" content="noindex">\n?', "", s)
            if t != s:
                open(f, "w", encoding="utf-8").write(t)
                n += 1
        print("indexing allowed on", n, "pages (remember to also update tools/pages.py if you rebuild)")
        s = open(PAGES_PY).read().replace('<meta name="robots" content="noindex">\n', "")
        open(PAGES_PY, "w").write(s)

    urls = []
    for f in sorted(html_files()):
        s = open(f, encoding="utf-8").read()
        if 'content="noindex"' in s and not (a.domain or a.index):
            pass  # preview: list anyway so the sitemap is ready on launch day
        m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not m:
            continue
        urls.append((m.group(1), lastmod(f)))
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")
    print("sitemap.xml:", len(urls), "urls; robots.txt written")


if __name__ == "__main__":
    main()
