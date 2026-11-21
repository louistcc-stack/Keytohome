"""Shared page shell for Key To Home's calculator and guide pages.

Run from the repo root:  python3 tools/build_pages.py
Edit the content in tools/build_pages.py, then re-run. The output is plain HTML, no build step on the server.
"""
import json

SITE = "https://keytohomes.sg"   # tools/go-live.py rewrites this to your own domain
WA = "6581668767"
AGENT = {
    "@type": "RealEstateAgent",
    "@id": SITE + "/#louis",
    "name": "Louis Tay",
    "url": SITE + "/",
    "image": SITE + "/assets/kth/louis-tay.jpg",
    "telephone": "+65 8166 8767",
    "email": "louistcc@gmail.com",
    "areaServed": {"@type": "Country", "name": "Singapore"},
    "parentOrganization": {"@type": "Organization", "name": "Huttons Asia Pte Ltd"},
    "identifier": [
        {"@type": "PropertyValue", "name": "CEA registration", "value": "R000567G"},
        {"@type": "PropertyValue", "name": "Agency licence", "value": "L3008899K"},
    ],
    "sameAs": [
        "https://www.instagram.com/louisisrealtor/",
        "https://www.propertyguru.com.sg/agent/louis-tay-104613",
    ],
}


def head(title, desc, path, extra_css=(), schema=(), base=""):
    url = SITE + "/" + path
    blocks = "".join(
        '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>\n" for s in schema
    )
    css = "".join(f'<link rel="stylesheet" href="{base}css/{c}">\n' for c in ("kth-base.css", "kth-beige.css", "kth-pages.css", *extra_css))
    return f"""<!doctype html>
<html lang="en-SG" data-theme="beige" data-base="{base}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F3ECE0">
<meta property="og:site_name" content="Key To Home">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{'article' if path.startswith('guides/') and path != 'guides/' else 'website'}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/kth/logo-key-to-home-charcoal-gold.png">
<meta property="og:locale" content="en_SG">
<link rel="canonical" href="{url}">
<link rel="icon" href="{base}assets/kth/logo-key-to-home-charcoal-gold.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;700;800&family=Cormorant+Garamond:ital,wght@1,500&display=swap">
{css}{blocks}</head>
<body>
<header class="nav">
<a class="brand" href="{base}index.html"><img src="{base}assets/kth/logo-key-to-home-charcoal-gold.png" alt="Key To Home" height="44"></a>
<div class="nav-right">
<button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
<nav id="nav" aria-label="Main"></nav>
<a class="pill gold" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a>
</div>
</header>
<main>
"""


def foot(base="", scripts=()):
    js = "".join(f'<script src="{base}js/{s}"></script>\n' for s in ("kth-config.js", "kth-main.js", *scripts))
    return f"""</main>
<footer>
<div class="fl"><img src="{base}assets/kth/logo-key-to-home-gold.png" alt="Key To Home"><p class="kth-tag" style="margin:10px 0 0;font-size:20px">Every key unlocks a new beginning.</p></div>
<p class="legal kth-legal">Louis Tay · CEA R000567G · Huttons Asia Pte Ltd (L3008899K) · +65 8166 8767<br><a href="mailto:louistcc@gmail.com">louistcc@gmail.com</a></p>
</footer>
{js}</body>
</html>
"""


def crumbs_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + p} for i, (n, p) in enumerate(items)
        ],
    }


def article_schema(title, desc, path, published, modified):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "mainEntityOfPage": SITE + "/" + path,
        "datePublished": published,
        "dateModified": modified,
        "author": {"@type": "Person", "name": "Louis Tay", "url": SITE + "/about.html", "jobTitle": "Property agent, Huttons Asia Pte Ltd (CEA R000567G)"},
        "publisher": {"@type": "Organization", "name": "Key To Home", "logo": {"@type": "ImageObject", "url": SITE + "/assets/kth/logo-key-to-home-charcoal-gold.png"}},
        "image": SITE + "/assets/kth/hero-living-room.webp",
    }
