"""Town pages: 'Selling your HDB flat in <town>'. Run: python3 tools/build_towns.py

Deals come from data/kth/transactions.json, so new deals in a town appear the next time you run this.
Add a town by adding one entry to TOWNS below. Only add towns where you have real deals.
"""
import json, os, sys
from html import escape
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from pages import SITE, WA, AGENT, head, foot, crumbs_schema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS = json.load(open(os.path.join(ROOT, "data/kth/transactions.json")))["transactions"]

SRC_LEASE = 'How much CPF savings can I use if the lease does not cover the youngest buyer to age 95?, CPF Board, accessed 22 Nov 2026, <a href="https://www.cpf.gov.sg/service/article/how-much-cpf-savings-can-i-use-to-buy-a-property-if-its-lease-does-not-cover-the-youngest-buyer-to-age-95" rel="noopener">cpf.gov.sg</a>'
SRC_ITS = 'Intent to Sell, HDB, accessed 22 Nov 2026, <a href="https://www.hdb.gov.sg/cs/infoweb/residential/selling-a-flat/plan-source-and-contract/intent-to-sell" rel="noopener">hdb.gov.sg</a>'
SRC_OTP = 'Option to Purchase, HDB, accessed 22 Nov 2026, <a href="https://www.hdb.gov.sg/cs/infoweb/residential/selling-a-flat/plan-source-and-contract/option-to-purchase" rel="noopener">hdb.gov.sg</a>'

TOWNS = [
    dict(
        town="Toa Payoh", slug="sell-hdb-toa-payoh",
        title="Selling your HDB flat in Toa Payoh | Louis Tay, Key To Home",
        desc="Selling your HDB flat in Toa Payoh? See the Toa Payoh homes Louis Tay has sold, what buyers ask about, and get an honest price range.",
        lead="I've helped families sell and buy flats from Lorong 1 to Toa Payoh Central and Alkaff Crescent. Here is what I've learned about selling in this estate, and how to get a fair price range for yours.",
        buyers="""
<p>Toa Payoh is one of Singapore's oldest HDB towns, and buyers here weigh three things more than anywhere else.</p>
<ul>
<li><strong>The remaining lease.</strong> Many blocks date back decades. A buyer can use their CPF in full, and take the full HDB loan, only if the lease left covers the youngest buyer to age 95. If it doesn't, their CPF use is pro-rated. That changes who can afford your flat, so I check this before we set a price.</li>
<li><strong>Getting around.</strong> Buyers ask how far the block is from Toa Payoh, Braddell or Caldecott MRT, and from the bus interchange at Toa Payoh Central.</li>
<li><strong>Condition and layout.</strong> Older flats are often bigger. Good photos of the space, and an honest note on what needs work, bring in serious viewers instead of bargain hunters.</li>
</ul>""",
        take="In Toa Payoh the lease conversation decides the price. I'd rather we price for the buyers who can actually get a loan than wait three months for one who can't.",
        faqs=[
            ("How much is my HDB flat in Toa Payoh worth?", "It depends on the block, floor, lease left, size and condition. Recent sales in the same block are the best guide. Send me your block and unit type and I'll give you an honest price range based on recent transactions, free."),
            ("Do older Toa Payoh flats still sell?", "Yes. The buyer pool is different. Buyers whose age and the lease left don't reach 95 can only use part of their CPF, so they need more cash. Pricing with that in mind is what gets an older flat sold."),
            ("How long does it take to sell an HDB flat in Toa Payoh?", "You register an Intent to Sell and wait 7 days before you can grant an option. After that it depends on price and demand. Then HDB processes the resale application. I'll give you a timeline for your block when we talk."),
            ("Can I sell my Toa Payoh flat and upgrade to a condo?", "Yes, once your flat has met its minimum occupation period. Work out your cash from the sale first. My HDB upgrade calculator shows it in a minute, and my guides cover whether to sell first or buy first."),
        ],
    ),
]


def card(t):
    img = t["photos"][0]
    tag = "tr-tag tr-tag-buy" if t.get("side") == "buyer" else "tr-tag"
    return (f'<article class="tr-card"><div class="tr-car"><img src="{img}" alt="{escape(t["title"])}" width="1200" height="900" loading="lazy" '
            f'style="width:100%;height:100%;object-fit:cover"><span class="{tag}">{t["status"].upper()}</span></div>'
            f'<div class="tr-body"><h3>{escape(t["title"])}</h3><p>{escape(t["area"])} · HDB resale · {"Buyer" if t.get("side") == "buyer" else "Seller"} side</p></div></article>')


def build(c):
    town, path = c["town"], c["slug"] + ".html"
    deals = [t for t in DEALS if t["area"] == town]
    sold = sum(1 for t in deals if t.get("side") != "buyer")
    bought = len(deals) - sold
    count_line = f"{sold} sold" + (f" and {bought} bought" if bought else "")
    wa_text = quote(f"Hi Louis, I'm thinking of selling my HDB flat in {town}. Could I get a price range?")
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faqs"])
    schema = [crumbs_schema([("Home", ""), ("Track record", "track-record.html"), (f"Sell HDB in {town}", path)]),
              dict(AGENT, **{"@context": "https://schema.org"})]
    html = head(c["title"], c["desc"], path, ("kth-track-record.css", "kth-guides.css"), schema) + f"""<div class="art">
<p class="crumbs"><a href="index.html">Home</a> / <a href="track-record.html">Track record</a></p>
<header class="art-head">
<h1>Selling your HDB flat in {town}</h1>
<p class="lead">{c["lead"]}</p>
<div class="byline"><img src="assets/kth/louis-tay.jpg" alt="" width="44" height="44"><span><b>Louis Tay</b>, Huttons Asia, 16 years in property. {count_line} in {town}.</span></div>
</header>
</div>

<section class="tr-sec" aria-label="{town} homes I've helped move">
<h2>{town} homes I've helped move</h2>
<div class="tr-grid">{"".join(card(t) for t in deals)}</div>
<p style="margin-top:18px"><a class="pill ghost" href="track-record.html">See all my deals</a></p>
</section>

<div class="art">
<div class="art-grid">
<div class="prose">
<h2 id="buyers">What {town} buyers ask about</h2>
{c["buyers"]}
<div class="take"><p>"{c["take"]}"</p><cite>Louis Tay</cite></div>

<h2 id="steps">How selling your flat works</h2>
<ol>
<li><strong>Get a price range.</strong> Check recent resale prices for your block on the HDB Flat Portal, or send me your block and I'll do it for you.</li>
<li><strong>Register your Intent to Sell</strong> on the HDB Flat Portal. It stays valid for 12 months.</li>
<li><strong>Wait 7 days.</strong> HDB requires this before you can grant an Option to Purchase. We use the time for photos and listing.</li>
<li><strong>Grant the option</strong> to a buyer who holds a valid HDB Flat Eligibility letter.</li>
<li><strong>Submit the resale application</strong> together with the buyer, and HDB takes it from there to completion.</li>
</ol>
<p>Thinking of upgrading after the sale? <a href="hdb-upgrade-calculator.html">The HDB upgrade calculator</a> shows your cash from the sale after the CPF refund, and <a href="guides/sell-first-or-buy-first.html">this guide</a> covers whether to sell first or buy first.</p>

<h2 id="faq">Questions {town} owners ask me</h2>
<div class="faq">{faq_html}</div>
<h2 id="sources">Sources</h2>
<ol class="sources"><li>{SRC_LEASE}</li><li>{SRC_ITS}</li><li>{SRC_OTP}</li></ol>
<p class="compliance">General information, not financial or legal advice. Louis Tay, CEA R000567G, Huttons Asia Pte Ltd (L3008899K), +65 8166 8767.</p>
</div>
<aside class="rail">
<div class="rail-cta"><b>What's your {town} flat worth?</b><p>Send your block and unit type. I'll reply with an honest price range.</p>
<a class="pill gold" href="#town-form">Get my price range</a>
<a class="pill ghost" href="https://wa.me/{WA}?text={wa_text}" target="_blank" rel="noopener">WhatsApp Louis</a></div>
</aside>
</div>
</div>

<section class="calc-lead" id="town-form">
<div class="inner">
<div>
<h2>Get a price range for your {town} flat</h2>
<p>I'll check recent sales in your block and nearby, and tell you what I'd list at and why. Free, and no obligation to sell through me.</p>
</div>
<form class="enquiry a88-lead" data-form="{town} town page" data-subject="{town} HDB valuation" novalidate>
<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
<input type="hidden" name="town" value="{town}">
<div class="field"><label for="t-name">Your name</label><input id="t-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="t-phone">Mobile number</label><input id="t-phone" name="phone" type="tel" required inputmode="tel" placeholder="8xxx xxxx" autocomplete="tel"></div>
<div class="field"><label for="t-addr">Block and street</label><input id="t-addr" name="address" placeholder="e.g. Blk 130A Lorong 1 Toa Payoh"></div>
<div class="field"><label for="t-type">Flat type</label><select id="t-type" name="hdbType"><option>3-room</option><option>4-room</option><option>5-room</option><option>Executive</option><option>Not sure</option></select></div>
<label class="consent"><input type="checkbox" name="consent" required> <span>I agree that Louis Tay (Huttons Asia Pte Ltd) may contact me about my enquiry and use my details in line with the PDPA.</span></label>
<button class="btn gold" type="submit">Get my price range</button>
<p class="form-note" aria-live="polite"></p>
</form>
</div>
</section>
""" + foot()
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path, f"({len(deals)} deals)")


for c in TOWNS:
    build(c)
