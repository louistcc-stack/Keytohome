# Key To Home

Personal site for Louis Tay, a Singapore property agent with Huttons Asia Pte Ltd (CEA R000567G, agency licence L3008899K).

Static files at the repo root. No build step.

Preview locally:

```bash
python3 -m http.server 8765
```

Then open http://127.0.0.1:8765/

Live at https://keytohomes.sg (GitHub Pages, custom domain set by the CNAME file).

## Growth engine (calculator, guides, SEO)

- `hdb-upgrade-calculator.html` + `js/kth-calc.js`: lead magnet. Leads go to WhatsApp with a calculator snapshot.
- `guides/`: pillar guides for HDB upgraders. Edit content in `tools/build_pages.py`, then run `python3 tools/build_pages.py`.
- `tools/go-live.py --domain yourdomain.sg`: switches canonicals to your domain, removes `noindex`, writes `CNAME`, `robots.txt` and `sitemap.xml`. Run `python3 tools/go-live.py` after adding pages to refresh the sitemap.
