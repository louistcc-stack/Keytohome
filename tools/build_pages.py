"""Builds the calculator page, the guides hub and each guide. Run: python3 tools/build_pages.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pages import SITE, WA, AGENT, head, foot, crumbs_schema, article_schema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026-11-21"
TODAY_TEXT = "21 November 2026"


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def wa(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"


# ---------------------------------------------------------------- calculator
CALC_TITLE = "HDB Upgrade Calculator: what condo can you afford? | Key To Home"
CALC_DESC = "HDB upgrade calculator for Singapore: see your cash from the sale after CPF refund, your loan limit and a new launch budget in one minute."

calc_body = f"""<section class="page-intro">
<h1>What can your flat buy you?</h1>
<p class="lead">Put in your flat, your CPF and your income. The ledger shows what's left after the sale, what a bank would lend, and the condo budget that leaves you. It assumes you sell your flat first, then buy.</p>
</section>

<div class="calc">
<form id="calc-form" onsubmit="return false" novalidate>
<fieldset>
<legend>Your flat</legend>
<p class="hint">Not sure what it's worth? Use a recent transaction in your block, or <a href="valuation.html" style="color:#6E520C;text-decoration:underline">ask me for a price range</a>.</p>
<div class="field"><label for="c-sale">Expected sale price</label><div class="money"><input id="c-sale" type="text" inputmode="numeric" value="650,000"></div></div>
<div class="two">
<div class="field"><label for="c-loan">Outstanding home loan</label><div class="money"><input id="c-loan" type="text" inputmode="numeric" value="150,000"></div></div>
<div class="field"><label for="c-costs">Selling costs, % of price</label><input id="c-costs" type="number" step="0.1" min="0" max="5" value="2"></div>
</div>
</fieldset>

<fieldset>
<legend>Your CPF</legend>
<p class="hint">Total CPF you and your co-owner used for the flat, including any grants. You can see the exact figure, with interest, on the CPF website under your property.</p>
<div class="two">
<div class="field"><label for="c-cpf">CPF used for the flat</label><div class="money"><input id="c-cpf" type="text" inputmode="numeric" value="200,000"></div></div>
<div class="field"><label for="c-years">Years since you bought</label><input id="c-years" type="number" min="0" max="40" value="10"></div>
</div>
<div class="field"><label for="c-oa">CPF Ordinary Account balance today</label><div class="money"><input id="c-oa" type="text" inputmode="numeric" value="40,000"></div></div>
</fieldset>

<fieldset>
<legend>Your household</legend>
<div class="two">
<div class="field"><label for="c-income">Combined gross monthly income</label><div class="money"><input id="c-income" type="text" inputmode="numeric" value="12,000"></div></div>
<div class="field"><label for="c-debts">Other monthly loan payments</label><div class="money"><input id="c-debts" type="text" inputmode="numeric" value="0"></div></div>
</div>
<div class="two">
<div class="field"><label for="c-cash">Cash savings for the new home</label><div class="money"><input id="c-cash" type="text" inputmode="numeric" value="50,000"></div></div>
<div class="field"><label for="c-age">Age of the older buyer</label><input id="c-age" type="number" min="21" max="75" value="40"></div>
</div>
<details class="adv"><summary>Change the stress-test rate</summary>
<div class="field"><label for="c-rate">Interest rate banks test your loan at, % a year</label><input id="c-rate" type="number" step="0.1" min="1" max="8" value="4"></div>
</details>
</fieldset>
</form>

<a class="calc-bar" href="#ledger">Your budget: <b id="o-bar">S$0</b><span>See the ledger</span></a>
<aside class="ledger" id="ledger" aria-live="polite" aria-label="Your upgrade ledger">
<h2>Your upgrade ledger</h2>
<div class="lrow"><span>Flat sale price</span><span id="o-sale"></span></div>
<div class="lrow minus"><span>Home loan repaid</span><span id="o-loan"></span></div>
<div class="lrow minus"><span>Selling costs</span><span id="o-costs"></span></div>
<div class="lrow minus"><span>CPF refund, with est. interest</span><span id="o-refund"></span></div>
<div class="lrow sum"><span>Cash in hand from the sale</span><span id="o-cashout"></span></div>
<div class="lrow"><span>Cash for the next home</span><span id="o-cash"></span></div>
<div class="lrow"><span>CPF for the next home</span><span id="o-cpf"></span></div>
<div class="lrow"><span>Loan a bank may allow</span><span id="o-loancap"></span></div>
<div class="lrow"><span>Loan tenure used</span><span id="o-tenure"></span></div>
<div class="big"><small>Indicative condo budget</small><output id="o-budget" for="calc-form"></output>
<p class="why" id="o-why"></p></div>
<div class="lrow"><span>Buyer's stamp duty at this price</span><span id="o-bsd"></span></div>
<div class="lrow"><span>Monthly repayment, at stress rate</span><span id="o-pmt"></span></div>
<p class="warn" id="o-warn" hidden></p>
<a class="pill gold" id="o-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">Ask Louis to check my numbers</a>
<p class="note">An estimate, not financial advice or a loan offer. It uses a 75% loan limit, at least 5% of the price in cash, a 55% debt limit on income, IRAS buyer's stamp duty rates and CPF interest of 2.5% a year. It leaves out ABSD, because selling first means you own one home when you buy. Banks, CPF and HDB have the final word.</p>
</aside>
</div>

<section class="calc-lead" id="calc-lead">
<div class="inner">
<div>
<h2>Want me to go through it with you?</h2>
<p>Send me these numbers. I'll check them against recent sales in your block, show you which new launches fit the budget, and tell you plainly if waiting a year makes more sense.</p>
<p>Prefer to read first? Start with <a href="guides/hdb-to-condo-upgrade.html" style="color:#6E520C;text-decoration:underline">the HDB to condo upgrade plan</a>.</p>
</div>
<form class="enquiry a88-lead" data-form="Upgrade calculator" data-subject="Upgrade calculator lead" novalidate>
<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
<input type="hidden" name="calc" id="c-snapshot">
<div class="field"><label for="l-name">Your name</label><input id="l-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="l-phone">Mobile number</label><input id="l-phone" name="phone" type="tel" required inputmode="tel" placeholder="8xxx xxxx" autocomplete="tel"></div>
<div class="field"><label for="l-time">When are you thinking of moving?</label><select id="l-time" name="timeline"><option>Within 6 months</option><option>6 to 12 months</option><option>1 to 2 years</option><option>Just planning</option></select></div>
<label class="consent"><input type="checkbox" name="consent" required> <span>I agree that Louis Tay (Huttons Asia Pte Ltd) may contact me about my enquiry and use my details in line with the PDPA.</span></label>
<button class="btn gold" type="submit">Send my numbers to Louis</button>
<p class="form-note" aria-live="polite"></p>
</form>
</div>
</section>
"""

calc_schema = [
    {"@context": "https://schema.org", "@type": "WebApplication", "name": "HDB Upgrade Calculator", "url": SITE + "/hdb-upgrade-calculator.html",
     "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SGD"},
     "creator": {"@id": SITE + "/#louis"}},
    crumbs_schema([("Home", ""), ("HDB upgrade calculator", "hdb-upgrade-calculator.html")]),
]
write("hdb-upgrade-calculator.html",
      head(CALC_TITLE, CALC_DESC, "hdb-upgrade-calculator.html", ("kth-guides.css",), calc_schema)
      + calc_body + foot("", ("kth-calc.js",)))


# ---------------------------------------------------------------- guides
GUIDES = []


def guide(slug, stage, title, h1, desc, lead, minutes, toc, body, faqs, sources, cta_text):
    path = f"guides/{slug}.html"
    GUIDES.append(dict(slug=slug, stage=stage, h1=h1, desc=desc, minutes=minutes))
    toc_html = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc)
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    src_html = "".join(f"<li>{s}</li>" for s in sources)
    schema = [
        article_schema(h1, desc, path, TODAY, TODAY),
        crumbs_schema([("Home", ""), ("Guides", "guides/"), (h1, path)]),
        dict(AGENT, **{"@context": "https://schema.org"}),
    ]
    html = head(title, desc, path, ("kth-guides.css",), schema, base="../") + f"""<article>
<div class="art">
<p class="crumbs"><a href="../index.html">Home</a> / <a href="./">Guides</a></p>
<header class="art-head">
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="byline"><img src="../assets/kth/louis-tay.jpg" alt="" width="44" height="44"><span>By <b>Louis Tay</b>, Huttons Asia, 16 years in property. Updated {TODAY_TEXT}. {minutes} min read.</span></div>
</header>
<div class="art-grid">
<div class="prose">
{body}
<h2 id="faq">Questions people ask me</h2>
<div class="faq">{faq_html}</div>
<h2 id="sources">Sources</h2>
<ol class="sources">{src_html}</ol>
<p class="compliance">This guide is general information, not financial, legal or tax advice. Rules change. Check the official pages above, and speak to your bank, CPF Board, HDB or a lawyer for your own case. Written by Louis Tay, CEA R000567G, Huttons Asia Pte Ltd (L3008899K), +65 8166 8767.</p>
</div>
<aside class="rail">
<nav class="toc" aria-label="On this page"><b>On this page</b><ol>{toc_html}</ol></nav>
<div class="rail-cta"><b>Run your own numbers</b><p>Cash from your sale, loan limit and condo budget in one minute.</p>
<a class="pill gold" href="../hdb-upgrade-calculator.html">Open the calculator</a>
<a class="pill ghost" href="{wa(cta_text)}" target="_blank" rel="noopener">WhatsApp Louis</a></div>
</aside>
</div>
</div>
</article>
<section class="art-end">
<div class="end-card">
<div><h2>Want this worked out for your flat?</h2><p>Tell me your block and unit type. I'll send an honest price range and what it means for your next home. No hard sell.</p></div>
<div class="btns"><a class="pill gold" href="../valuation.html">Get my free assessment</a><a class="pill ghost" href="{wa(cta_text)}" target="_blank" rel="noopener">WhatsApp me</a></div>
</div>
</section>
""" + foot("../")
    write(path, html)


SRC_BSD = 'Buyer\'s Stamp Duty (BSD), IRAS, accessed 21 Nov 2026, <a href="https://www.iras.gov.sg/taxes/stamp-duty/for-property/buying-or-acquiring-property/buyer\'s-stamp-duty-(bsd)" rel="noopener">iras.gov.sg</a>'
SRC_ABSD = 'Additional Buyer\'s Stamp Duty (ABSD), IRAS, accessed 21 Nov 2026, <a href="https://www.iras.gov.sg/taxes/stamp-duty/for-property/buying-or-acquiring-property/additional-buyer\'s-stamp-duty-(ABSD)" rel="noopener">iras.gov.sg</a>'
SRC_REMIT = 'Remission of ABSD for a married couple, IRAS, accessed 21 Nov 2026, <a href="https://www.iras.gov.sg/taxes/stamp-duty/for-property/appeals-refunds-reliefs-and-remissions/common-stamp-duty-remissions-and-reliefs-for-property/remission-of-absd-for-a-married-couple" rel="noopener">iras.gov.sg</a>'
SRC_MAS = 'Macroprudential policies in Singapore (LTV, TDSR, MSR), Monetary Authority of Singapore, accessed 21 Nov 2026, <a href="https://www.mas.gov.sg/publications/macroprudential-policies-in-singapore" rel="noopener">mas.gov.sg</a>'
SRC_MONEY = 'Buying a property: how much can you afford?, MoneySense, accessed 21 Nov 2026, <a href="https://www.moneysense.gov.sg/buying-a-property-how-much-can-you-afford/" rel="noopener">moneysense.gov.sg</a>'
SRC_TEOS = 'Request for temporary extension of stay, HDB, terms dated 19 Feb 2026, <a href="https://www.hdb.gov.sg/residential/selling-a-flat/resale-application/request-for-temporary-extension-of-stay" rel="noopener">hdb.gov.sg</a>'
SRC_VHR = '3 reasons why you should consider making a voluntary housing refund, CPF Board, 29 May 2026, <a href="https://www.cpf.gov.sg/member/infohub/educational-resources/3-reasons-why-you-should-consider-making-a-voluntary-housing-refund" rel="noopener">cpf.gov.sg</a>'

# --- Guide 1: the pillar
guide(
    "hdb-to-condo-upgrade", "Plan",
    "HDB to condo upgrade: the 6-step plan for Singapore families | Key To Home",
    "HDB to condo upgrade: the 6-step plan",
    "Upgrading from HDB to a condo in Singapore? The 6 steps in order: MOP, cash from your sale, loan limit, sell or buy first, new launch vs resale, hidden costs.",
    "Most families I meet start by looking at showflats. I'd start with the maths. Here is the order I walk every upgrader through, with real numbers.",
    9,
    [("s1", "Check you can buy"), ("s2", "Work out your real cash"), ("s3", "Know your loan limit"), ("s4", "Sell first or buy first"),
     ("s5", "New launch or resale condo"), ("s6", "Count the costs people forget"), ("faq", "Questions")],
    """
<h2 id="s1">1. Check you can buy</h2>
<p>You can only buy private property once your flat has met its minimum occupation period (MOP). For most flats that is 5 years from the day you got the keys. Flats sold under the newer Plus and Prime models carry a 10-year MOP, so check your own flat's terms on the HDB website.</p>
<p>After MOP you can buy a condo and keep the flat. Owning two homes brings ABSD into play, which step 4 covers.</p>

<h2 id="s2">2. Work out your real cash</h2>
<p>Your sale price is not your cash. Three things come off the top before you see a cent:</p>
<ol>
<li><strong>The rest of your home loan</strong>, paid to the bank or HDB.</li>
<li><strong>Your CPF refund.</strong> Every dollar of CPF you used for the flat goes back into your Ordinary Account, plus 2.5% a year in accrued interest.</li>
<li><strong>Selling costs</strong>, such as agent and legal fees.</li>
</ol>
<p>Here is a typical case: a flat that sells for S$650,000 with S$150,000 of loan left, and S$200,000 of CPF used over 10 years.</p>
<table>
<tr><th>Line</th><th class="n">Amount</th></tr>
<tr><td>Sale price</td><td class="n">S$650,000</td></tr>
<tr><td>Loan repaid</td><td class="n">− S$150,000</td></tr>
<tr><td>CPF refund: S$200,000 plus about S$56,000 interest</td><td class="n">− S$256,000</td></tr>
<tr><td>Selling costs at 2%</td><td class="n">− S$13,000</td></tr>
<tr><td><strong>Cash in hand</strong></td><td class="n"><strong>S$231,000</strong></td></tr>
</table>
<p>The good news: the S$256,000 going back to CPF is still yours. You can use it again for the next downpayment and stamp duty. The <a href="cpf-accrued-interest-hdb-sale.html">CPF accrued interest guide</a> explains how the refund works.</p>

<h2 id="s3">3. Know your loan limit</h2>
<p>Banks lend on two tests, and the lower one wins.</p>
<ul>
<li><strong>Loan-to-value (LTV).</strong> For your first housing loan, a bank lends up to 75% of the price. At least 5% must be paid in cash. The other 20% can be cash or CPF.</li>
<li><strong>Total debt servicing ratio (TDSR).</strong> All your monthly loan payments together can't go over 55% of your gross monthly income. Banks test this at a higher interest rate than you'll pay. I use 4% a year.</li>
</ul>
<p>To get the full 75%, the loan has to end by age 65 and run no more than 30 years for private property. Older buyers often get a shorter tenure, which cuts the loan.</p>
<p>A couple earning S$12,000 a month with no other loans can borrow roughly S$1.38 million on the TDSR test over 30 years. The cash test often bites first. <a href="../hdb-upgrade-calculator.html">The calculator</a> shows which one limits you.</p>

<h2 id="s4">4. Sell first or buy first</h2>
<p>This is the biggest decision in the whole plan, and the one people rush.</p>
<ul>
<li><strong>Sell first:</strong> no ABSD, and you know your cash exactly. You need somewhere to stay between homes.</li>
<li><strong>Buy first:</strong> you move once. A married couple pays 20% ABSD upfront and gets it back only if they sell the flat in time.</li>
</ul>
<p>I've written a full comparison with the timelines: <a href="sell-first-or-buy-first.html">sell first or buy first when upgrading from HDB</a>.</p>

<h2 id="s5">5. New launch or resale condo</h2>
<p>A new launch is paid in stages while it's being built. You pay 5% when you book and the rest of the 20% downpayment when you sign the sale and purchase agreement. The loan is drawn down as construction moves along, so early instalments are small.</p>
<p>A resale condo is paid in full at completion, usually 8 to 12 weeks after you exercise the option. You move in sooner and see exactly what you're buying.</p>
<p>For buy-first couples, a new launch has one more draw. The ABSD clock runs from the project's TOP, so you can live in your flat for the years it takes to build. The catch is that the 20% ABSD sits with IRAS for that whole time.</p>

<h2 id="s6">6. Count the costs people forget</h2>
<ul>
<li><strong>Buyer's stamp duty:</strong> about S$49,600 on a S$1.6 million condo, payable within 14 days of signing.</li>
<li><strong>Legal fees</strong> on both the sale and the purchase.</li>
<li><strong>Renovation and furniture</strong> for the new place.</li>
<li><strong>Rent</strong> if you sell first and the new home isn't ready.</li>
<li><strong>Interest during the gap</strong> if you buy first and service two loans.</li>
</ul>

<div class="take"><p>"The families who upgrade well aren't the ones who find the cheapest unit. They're the ones who knew their cash number before they walked into a showflat."</p><cite>Louis Tay</cite></div>
""",
    [
        ("How long after MOP can I buy a condo?", "Straight away. Once your flat has met its MOP, you can buy private property and keep the flat. If you still own the flat when you buy, ABSD applies on the condo. Married couples can claim it back if they sell the flat within the time IRAS allows."),
        ("How much cash do I need to upgrade from HDB to a condo?", "At least 5% of the condo price in cash, plus up to 20% more in cash or CPF, plus buyer's stamp duty. On a S$1.6 million condo that is S$80,000 cash, S$320,000 cash or CPF, and about S$49,600 in stamp duty. Legal fees and renovation come on top."),
        ("Can I use my CPF refund for the new condo?", "Yes. The CPF refund from your flat sale goes back into your Ordinary Account. You can use it for the condo downpayment, stamp duty and monthly instalments, within CPF's usage limits for private property."),
        ("Is it better to upgrade to a new launch or a resale condo?", "It depends on your timeline and cash. A new launch is paid in stages and gives buy-first couples time to sell their flat. A resale condo lets you move in within months and see the actual unit. Many of my clients compare both before deciding."),
        ("What income do I need to upgrade from HDB?", "It depends on the price, your age and your other loans. Banks cap all loan payments at 55% of gross income, tested at a higher rate. Put your figures into the HDB upgrade calculator on this site for a quick estimate."),
    ],
    [SRC_MAS, SRC_MONEY, SRC_BSD, SRC_ABSD, SRC_REMIT],
    "Hi Louis, I read your HDB to condo upgrade guide. Could you help me plan my upgrade?",
)

# --- Guide 2
guide(
    "sell-first-or-buy-first", "Decide",
    "Sell first or buy first when upgrading from HDB? | Key To Home",
    "Sell first or buy first when upgrading from HDB?",
    "Sell first or buy first when upgrading from HDB? Compare ABSD, cash flow and where you live in between, with the IRAS and HDB timelines.",
    "Both work. They fail in different ways. Here is how each one plays out, and the questions I ask before I recommend one.",
    7,
    [("t1", "The short answer"), ("t2", "Sell first"), ("t3", "Buy first"), ("t4", "Side by side"), ("t5", "How I decide with clients"), ("faq", "Questions")],
    """
<h2 id="t1">The short answer</h2>
<p>Sell first if your cash is tight or you're buying as a single. Buy first if you're a married couple, you have the cash for 20% ABSD upfront, and you're confident your flat will sell inside the deadline.</p>

<h2 id="t2">Sell first, then buy</h2>
<p>You sell the flat, then buy the condo while you own nothing else. No ABSD applies to Singapore citizens buying their only home.</p>
<h3>What goes well</h3>
<ul>
<li>You know your exact cash and CPF before you choose a unit.</li>
<li>No ABSD, so no large sum tied up with IRAS.</li>
<li>One home loan at a time.</li>
</ul>
<h3>What can go wrong</h3>
<ul>
<li><strong>The gap.</strong> HDB lets a seller who has bought a completed home stay up to 3 months after resale completion, if the buyer agrees. Beyond that you rent or stay with family.</li>
<li><strong>Price moves.</strong> If condo prices rise while you sell, your budget buys less.</li>
</ul>

<h2 id="t3">Buy first, then sell</h2>
<p>You buy the condo while you still own the flat. A Singapore citizen buying a second home pays 20% ABSD on top of buyer's stamp duty, within 14 days.</p>
<p>A married couple with at least one Singapore citizen can claim that ABSD back if they sell the flat in time. IRAS counts 6 months from the purchase date for a completed condo. For a new launch, it counts 6 months from TOP or CSC, whichever comes first. IRAS says it will not extend this timeline.</p>
<h3>What goes well</h3>
<ul>
<li>You move once, straight into the new home.</li>
<li>With a new launch, you can stay in the flat during construction.</li>
</ul>
<h3>What can go wrong</h3>
<ul>
<li><strong>Cash flow.</strong> On a S$1.6 million condo, 20% ABSD is S$320,000, payable before your flat sale brings in a cent.</li>
<li><strong>The deadline.</strong> Miss it and the ABSD is not refunded.</li>
<li><strong>Two loans.</strong> The flat's loan counts in your TDSR, which shrinks the condo loan.</li>
<li><strong>Singles</strong> can't claim the refund at all.</li>
</ul>

<h2 id="t4">Side by side</h2>
<table>
<tr><th></th><th>Sell first</th><th>Buy first</th></tr>
<tr><td>ABSD</td><td>None for a citizen's only home</td><td>20% upfront, refundable for married couples who sell in time</td></tr>
<tr><td>Cash certainty</td><td>High</td><td>You estimate your sale proceeds</td></tr>
<tr><td>Where you live</td><td>Up to 3 months' extension, then rent</td><td>Stay put until the new home is ready</td></tr>
<tr><td>Loan size</td><td>Full TDSR available</td><td>Reduced by the flat's loan</td></tr>
<tr><td>Fits best</td><td>Singles, tight cash, resale condo buyers</td><td>Couples with spare cash, new launch buyers</td></tr>
</table>

<h2 id="t5">How I decide with clients</h2>
<p>I ask four questions:</p>
<ol>
<li>Can you pay 20% ABSD in cash or CPF today without touching your emergency fund?</li>
<li>How fast are flats like yours selling in your block right now?</li>
<li>Is the condo completed or still under construction?</li>
<li>If the flat took 6 months longer to sell, what would you do?</li>
</ol>
<p>If the answer to the last one is "I don't know", we sell first.</p>
<div class="take"><p>"Buy first sounds easier because you move once. It only works when the 20% won't keep you up at night."</p><cite>Louis Tay</cite></div>
""",
    [
        ("Do I pay ABSD if I buy a condo before selling my HDB?", "Yes, if you still own the flat when you buy. A Singapore citizen pays 20% ABSD on a second residential property. Married couples with at least one Singapore citizen can apply for a refund if they sell the flat within the IRAS deadline."),
        ("How long can I stay in my HDB flat after selling it?", "If you have bought a completed home, HDB allows a temporary extension of stay of up to 3 months after resale completion, with the buyer's agreement. It ends on its own after 3 months. Any payment for the stay is agreed between you and the buyer."),
        ("What if I can't sell my HDB within 6 months?", "The ABSD you paid will not be refunded. IRAS states there is no extension of the 6-month timeline. That's why I price the flat to sell and line up buyers before the deadline gets close."),
        ("Can singles buy first and claim back ABSD?", "No. The ABSD refund for selling your first home applies to married couples with at least one Singapore citizen. Singles who buy a second home pay ABSD with no refund, so selling first is usually the safer route."),
        ("Is buy first better for new launches?", "Often, for couples. The refund clock for an uncompleted project starts at TOP or CSC, so you can stay in the flat during construction. You still need the 20% ABSD in cash or CPF at the start."),
    ],
    [SRC_ABSD, SRC_REMIT, SRC_TEOS, SRC_MAS, SRC_BSD],
    "Hi Louis, I read your sell first or buy first guide. Which one suits my situation?",
)

# --- Guide 3
guide(
    "cpf-accrued-interest-hdb-sale", "Prepare",
    "CPF accrued interest: how much cash will your HDB sale leave you? | Key To Home",
    "CPF accrued interest: how much cash will your HDB sale leave you?",
    "CPF accrued interest explained for HDB sellers: how the refund works, worked examples at 5, 10 and 15 years, and how to check your exact figure.",
    "Every month you pay your flat with CPF, a refund grows in the background. Most sellers only see it at the end. Here is how to see it now.",
    6,
    [("c1", "What accrued interest is"), ("c2", "Worked examples"), ("c3", "When the sale doesn't cover it"), ("c4", "Check your exact figure"), ("c5", "Should you refund early?"), ("faq", "Questions")],
    """
<h2 id="c1">What accrued interest is</h2>
<p>When you use CPF for your flat, the money leaves your Ordinary Account. CPF keeps track of the interest it would have earned there, at 2.5% a year. When you sell, the principal you used plus that interest goes back into your CPF account. That total is your CPF refund.</p>
<p>Any housing grant you received is refunded the same way, with interest.</p>
<p>The refund isn't a fee. It goes back to your own CPF, ready for your next home. It does mean less cash in hand.</p>

<h2 id="c2">Worked examples</h2>
<p>Take S$200,000 of CPF used. Here is roughly what you'd refund at sale. The interest is my estimate, compounded yearly.</p>
<table>
<tr><th>Years since purchase</th><th class="n">Accrued interest</th><th class="n">Total CPF refund</th></tr>
<tr><td>5 years</td><td class="n">about S$26,300</td><td class="n">about S$226,300</td></tr>
<tr><td>10 years</td><td class="n">about S$56,000</td><td class="n">about S$256,000</td></tr>
<tr><td>15 years</td><td class="n">about S$89,700</td><td class="n">about S$289,700</td></tr>
</table>
<p>In real life the CPF you used builds up month by month, so your figure will differ. The point stands: the longer you've owned, the more of your sale price heads back to CPF.</p>

<h2 id="c3">When the sale doesn't cover it</h2>
<p>Sometimes the sale price, minus the loan, is less than the CPF refund. People call this a negative sale. CPF takes back what the proceeds can cover and you don't top up the gap in cash. You do walk away with no cash from the sale.</p>
<p>For an upgrader, this changes the plan: your next downpayment has to come from savings and your CPF balance.</p>

<h2 id="c4">Check your exact figure</h2>
<ol>
<li>Log in to the CPF website with Singpass.</li>
<li>Go to your home ownership details and open the property.</li>
<li>Note the principal withdrawn and the accrued interest for each owner.</li>
<li>Add them up for all owners. That is your CPF refund.</li>
</ol>
<p>Then put the number into <a href="../hdb-upgrade-calculator.html">the HDB upgrade calculator</a> in place of the estimate.</p>

<h2 id="c5">Should you refund early?</h2>
<p>CPF lets you make a voluntary housing refund before you sell. It puts cash back into your CPF now, where it earns interest for you. It doesn't add to your cash at sale, so I only suggest it to clients with spare cash and no near-term plan to upgrade.</p>
<div class="take"><p>"I pull the CPF statement before I quote anyone a 'cash from sale' number. It's the one figure that surprises people most."</p><cite>Louis Tay</cite></div>
""",
    [
        ("Do I lose my CPF accrued interest when I sell my HDB?", "No. The principal and accrued interest go back into your own CPF account. You can use them again for your next home, or keep them for retirement. What you lose is that part of the sale price as cash in hand."),
        ("What rate is CPF accrued interest?", "2.5% a year, the Ordinary Account rate, on the CPF you used for the property. My examples compound it yearly as an estimate. Your CPF account shows the exact figure."),
        ("Do I need to refund housing grants when I sell my HDB?", "Yes. CPF housing grants you received for the flat are refunded to your CPF account, with accrued interest, when you sell."),
        ("What happens if my HDB sale price is too low to cover the CPF refund?", "CPF takes back what the sale proceeds can cover after the loan is repaid. You don't have to top up the gap in cash, but you'll receive no cash from the sale."),
        ("Can I reduce my CPF accrued interest?", "A voluntary housing refund puts money back into CPF earlier, which slows how fast the accrued interest grows. It doesn't increase the cash you receive at sale, so it suits people with spare cash who aren't upgrading soon."),
    ],
    [SRC_VHR, 'CPF housing usage and refund pages, CPF Board, accessed 21 Nov 2026, <a href="https://www.cpf.gov.sg/member/home-ownership" rel="noopener">cpf.gov.sg</a>', SRC_MONEY],
    "Hi Louis, I read your CPF accrued interest guide. Could you help me work out my cash from sale?",
)

# ---------------------------------------------------------------- hub
items = "".join(
    f"""<div class="g-item"><span class="stage">{g['stage']}</span><div><h2><a href="{g['slug']}.html">{g['h1']}</a></h2><p>{g['desc']}</p></div><span class="meta">{g['minutes']} min read</span></div>"""
    for g in GUIDES
)
hub_desc = "Plain-English guides for HDB upgraders in Singapore: the upgrade plan, sell first or buy first, and CPF accrued interest. By Louis Tay, Huttons."
hub = head("Guides for HDB upgraders | Key To Home", hub_desc, "guides/", ("kth-guides.css",),
           [crumbs_schema([("Home", ""), ("Guides", "guides/")]), dict(AGENT, **{"@context": "https://schema.org"})], base="../") + f"""<section class="page-intro">
<h1>Guides for HDB upgraders.</h1>
<p class="lead">The questions I answer every week, written down properly. Read them in order if you're just starting.</p>
</section>
<section class="g-list">{items}</section>
<section class="art-end"><div class="end-card"><div><h2>Rather see your own numbers?</h2><p>The calculator shows your cash from the sale, your loan limit and a condo budget.</p></div><div class="btns"><a class="pill gold" href="../hdb-upgrade-calculator.html">Open the calculator</a></div></div></section>
""" + foot("../")
write("guides/index.html", hub)
