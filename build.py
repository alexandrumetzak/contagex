#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator pentru paginile secundare ale site-ului CONTAGEX SRL:
  - pagini de SEO local, per oraș (Huși, Vaslui, Bârlad, Iași)
  - blog / noutăți fiscale (index + articole)

Antetul și subsolul sunt definite o singură dată aici, ca să rămână
identice pe toate paginile. Rulează:  python3 build.py

Notă: linkurile interne sunt RELATIVE (folosind prefixul `R`), ca site-ul
să funcționeze și când e servit dintr-un subfolder (ex: GitHub Pages
project site la /contagex/), nu doar de la rădăcina domeniului.
Paginile din rădăcină folosesc R="" ; paginile din /blog/ folosesc R="../".
"""
import json, os, html

SITE   = "https://www.contagex.ro"
PHONE  = "+40743085632"
PHONE_DISPLAY = "+40 743 085 632"
EMAIL  = "georgica.aciobanitei@gmail.com"
ROOT   = os.path.dirname(os.path.abspath(__file__))

PHONE_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">'
             '<path fill="currentColor" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 '
             '1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.4 21 3 13.6 3 4c0-.6.4-1 1-1h3.5c.6 0 '
             '1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>')

ORG_ID = SITE + "/#organization"

# Nod reutilizabil pentru organizație (referențiat prin @id)
def org_node(area=None):
    node = {
        "@type": "AccountingService",
        "@id": ORG_ID,
        "name": "CONTAGEX SRL",
        "url": SITE + "/",
        "telephone": PHONE,
        "email": EMAIL,
        "foundingDate": "2004",
        "taxID": "16173016",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Str. 1 Decembrie nr. 6, bl. 6, sc. B, ap. 23",
            "addressLocality": "Huși", "addressRegion": "Vaslui",
            "postalCode": "735100", "addressCountry": "RO",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 46.6747, "longitude": 28.0606},
    }
    if area:
        node["areaServed"] = {"@type": "City", "name": area}
    return node

# BreadcrumbList pentru JSON-LD foloseste URL-uri ABSOLUTE (pentru SEO)
def breadcrumb(items):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             **({"item": SITE + url} if url else {})}
            for i, (name, url) in enumerate(items)
        ],
    }

def faqpage(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }

def ldjson(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + '\n</script>')

# ----------------------------------------------------------------------------
def head(title, desc, path, jsonld, R, og_image="/assets/og-image.png", robots="index, follow"):
    canonical = SITE + path
    blocks = "\n  ".join(ldjson(o) for o in jsonld)
    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <meta name="robots" content="{robots}, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="{canonical}" />
  <meta name="theme-color" content="#0d2a4a" />
  <meta name="geo.region" content="RO-VS" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="ro_RO" />
  <meta property="og:site_name" content="CONTAGEX SRL" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(title)}" />
  <meta name="twitter:description" content="{html.escape(desc)}" />
  <meta name="twitter:image" content="{SITE}{og_image}" />
  <link rel="icon" href="{R}assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="{R}assets/favicon.svg" />
  <link rel="manifest" href="{R}site.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{R}css/styles.css" />
  {blocks}
</head>
<body>"""

def header(R):
    return f"""
  <a class="skip-link" href="#main">Sari la conținut</a>
  <header class="site-header" id="top">
    <div class="container header-inner">
      <a href="{R}index.html" class="brand" aria-label="CONTAGEX SRL — acasă">
        <img class="brand-mark" src="{R}assets/emblem.svg" alt="" width="46" height="46" aria-hidden="true" />
        <span class="brand-text">
          <strong>CONTAGEX</strong>
          <small>Contabilitate &amp; Expertiză</small>
        </span>
      </a>
      <nav class="nav" aria-label="Navigare principală">
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Deschide meniul">
          <span></span><span></span><span></span>
        </button>
        <ul class="nav-menu" id="nav-menu">
          <li><a href="{R}index.html#servicii">Servicii</a></li>
          <li><a href="{R}index.html#despre">Despre noi</a></li>
          <li><a href="{R}index.html#zone">Zone deservite</a></li>
          <li><a href="{R}blog/">Noutăți</a></li>
          <li><a href="{R}index.html#faq">Întrebări</a></li>
          <li><a href="{R}index.html#contact" class="nav-cta">Contact</a></li>
        </ul>
      </nav>
      <a href="tel:{PHONE}" class="header-phone" aria-label="Sună la {PHONE_DISPLAY}">
        {PHONE_SVG}<span>{PHONE_DISPLAY}</span>
      </a>
    </div>
  </header>"""

def footer(R):
    return f"""
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <div class="brand brand-footer">
          <img class="brand-mark" src="{R}assets/emblem.svg" alt="" width="46" height="46" aria-hidden="true" />
          <span class="brand-text"><strong>CONTAGEX SRL</strong><small>Contabilitate &amp; Expertiză</small></span>
        </div>
        <p class="footer-desc">Firmă de contabilitate din Huși, cu peste 22 de ani de experiență. Servicii contabile și expertiză contabilă extrajudiciară pentru Huși, Vaslui, Bârlad și Iași.</p>
      </div>
      <div>
        <h3>Navigare</h3>
        <ul>
          <li><a href="{R}index.html#servicii">Servicii</a></li>
          <li><a href="{R}index.html#despre">Despre noi</a></li>
          <li><a href="{R}index.html#legislatie">Legislație la zi</a></li>
          <li><a href="{R}blog/">Noutăți fiscale</a></li>
          <li><a href="{R}index.html#faq">Întrebări frecvente</a></li>
        </ul>
      </div>
      <div>
        <h3>Zone deservite</h3>
        <ul>
          <li><a href="{R}contabilitate-husi.html">Contabilitate Huși</a></li>
          <li><a href="{R}contabilitate-vaslui.html">Contabilitate Vaslui</a></li>
          <li><a href="{R}contabilitate-barlad.html">Contabilitate Bârlad</a></li>
          <li><a href="{R}contabilitate-iasi.html">Contabilitate Iași</a></li>
        </ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Str. 1 Decembrie nr. 6, Huși, jud. Vaslui</li>
          <li>CUI 16173016 · J37/126/2004</li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>&copy; <span id="year">2026</span> CONTAGEX SRL. Toate drepturile rezervate.</p>
      <p>Contabilitate Huși · Vaslui · Bârlad · Iași</p>
    </div>
  </footer>
  <a href="tel:{PHONE}" class="fab-call" aria-label="Sună la CONTAGEX">
    {PHONE_SVG.replace('width="18" height="18" ', '')}
  </a>
  <script src="{R}js/script.js" defer></script>
</body>
</html>"""

def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("scris:", path)

# ============================================================================
# SERVICII (rezumat reutilizat pe paginile de oraș)
SERVICES = [
    "Contabilitate financiară și de gestiune",
    "Expertiză contabilă extrajudiciară",
    "Consultanță fiscală și financiară",
    "Salarizare și administrare de personal",
    "Întocmirea și depunerea declarațiilor fiscale",
    "Înființări firme și consultanță de start-up",
]

# ============================================================================
# PAGINI PER ORAȘ
CITIES = [
  {
    "slug": "contabilitate-husi", "city": "Huși",
    "title": "Contabilitate Huși — CONTAGEX SRL | Servicii contabile & expertiză contabilă",
    "desc": "Firmă de contabilitate în Huși cu peste 22 de ani de experiență. Servicii contabile complete și expertiză contabilă extrajudiciară, cu sediu în centrul orașului și relație directă cu expertul contabil.",
    "h1": "Contabilitate în Huși — firma ta locală, cu peste 22 de ani de experiență",
    "lead": "CONTAGEX SRL este firma de contabilitate din Huși la care antreprenorii apelează când vor seriozitate și o relație directă cu expertul contabil. Sediul nostru este în centrul orașului, pe Str. 1 Decembrie.",
    "intro": [
      "Huși este orașul în care activăm din anul 2004. Cunoaștem mediul de afaceri local și înțelegem nevoile reale ale firmelor de aici — de la magazine și firme de servicii, până la activități din agricultură, transport sau construcții.",
      "Pentru clienții din Huși, colaborarea înseamnă întâlniri față în față, ori de câte ori e nevoie, și un singur om de contact: expertul contabil care îți cunoaște afacerea, nu un call-center.",
    ],
    "why": [
      ("Sediu în Huși", "Ne poți vizita la birou, pe Str. 1 Decembrie, pentru a discuta și a preda documentele direct."),
      ("Cunoaștem piața locală", "Peste 22 de ani de activitate neîntreruptă în Huși înseamnă experiență cu specificul firmelor din zonă."),
      ("Relație directă", "Comunici direct cu expertul contabil, nu cu un operator. Răspuns rapid și sfaturi pe înțelesul tău."),
      ("Confidențialitate totală", "Datele financiare ale firmei tale sunt tratate cu maximă discreție și responsabilitate."),
    ],
    "coverage": "Pentru firmele din Huși, documentele pot fi predate la sediu sau transmise electronic — alegi varianta care îți este mai comodă. Indiferent de metodă, evidența contabilă este ținută la zi și conformă cu legislația în vigoare.",
    "faq": [
      ("Unde se află biroul vostru de contabilitate din Huși?",
       "Sediul CONTAGEX SRL este în Huși, pe Str. 1 Decembrie nr. 6. Ne poți contacta telefonic la " + PHONE_DISPLAY + " pentru a stabili o întâlnire."),
      ("Pot veni cu documentele direct la sediu?",
       "Da. Clienții din Huși pot preda documentele direct la birou. Alternativ, le poți transmite electronic, dacă îți este mai comod."),
      ("Lucrați cu PFA și microîntreprinderi din Huși?",
       "Da, lucrăm cu PFA, microîntreprinderi și societăți de toate dimensiunile din Huși și din zona limitrofă."),
    ],
  },
  {
    "slug": "contabilitate-vaslui", "city": "Vaslui",
    "title": "Contabilitate Vaslui — CONTAGEX SRL | Servicii contabile pentru firme",
    "desc": "Servicii de contabilitate pentru firme din Vaslui și din întreg județul. Peste 22 de ani de experiență, consultanță fiscală și expertiză contabilă extrajudiciară. Colaborare la sediu sau online.",
    "h1": "Contabilitate în Vaslui — servicii contabile pentru reședința de județ",
    "lead": "CONTAGEX SRL oferă servicii complete de contabilitate firmelor din municipiul Vaslui și din întreg județul, îmbinând experiența de peste 22 de ani cu o colaborare modernă, eficientă.",
    "intro": [
      "Ca firmă din județul Vaslui, înțelegem realitățile economice locale și suntem aproape de antreprenorii din reședința de județ. Colaborarea se desfășoară confortabil prin transmiterea documentelor în format electronic, completată de întâlniri periodice atunci când este nevoie.",
      "De la microîntreprinderi la societăți cu activitate complexă, ținem evidența contabilă corect și la termen, astfel încât tu să te poți concentra pe dezvoltarea afacerii.",
    ],
    "why": [
      ("Experiență la nivel de județ", "Cunoaștem specificul firmelor din Vaslui și colaborăm cu clienți din toate domeniile."),
      ("Colaborare online eficientă", "Transmiți documentele electronic, fără deplasări inutile, cu aceeași rigoare și promptitudine."),
      ("Conformitate fiscală", "Urmărim modificările legislative și aplicăm regulile noi înainte de termenele ANAF."),
      ("Expertiză extrajudiciară", "Analize independente pentru litigii comerciale și verificarea corectitudinii contabile."),
    ],
    "coverage": "Distanța nu este o problemă: majoritatea colaborărilor cu firmele din Vaslui se desfășoară online, prin e-mail și documente scanate, completate de discuții telefonice și întâlniri ocazionale. Primești același nivel de atenție ca un client de la sediu.",
    "faq": [
      ("Lucrați cu firme din Vaslui dacă sediul vostru este în Huși?",
       "Da. Colaborăm cu numeroase firme din Vaslui preponderent online — documentele se transmit electronic, iar comunicarea este permanentă prin telefon și e-mail."),
      ("Cât de des trebuie să ne întâlnim fizic?",
       "În general nu este necesar să ne întâlnim des. Majoritatea operațiunilor se rezolvă la distanță; întâlnirile se programează doar atunci când este cu adevărat util."),
      ("Oferiți și consultanță fiscală pentru firmele din Vaslui?",
       "Da, oferim consultanță fiscală și financiară completă, inclusiv pentru alegerea regimului de impozitare potrivit."),
    ],
  },
  {
    "slug": "contabilitate-barlad", "city": "Bârlad",
    "title": "Contabilitate Bârlad — CONTAGEX SRL | Servicii contabile & expertiză",
    "desc": "Contabilitate pentru firme din Bârlad: servicii contabile complete, consultanță fiscală și expertiză contabilă extrajudiciară. Peste 22 de ani de experiență, colaborare online sau la sediu.",
    "h1": "Contabilitate în Bârlad — partener contabil pentru cel mai mare oraș al județului",
    "lead": "Bârlad are una dintre cele mai dinamice scene de afaceri din județul Vaslui. CONTAGEX SRL sprijină firmele de aici cu servicii contabile complete și expertiză contabilă extrajudiciară.",
    "intro": [
      "Fiind cel mai mare oraș al județului, Bârlad găzduiește numeroase firme de comerț, producție și servicii. Pentru fiecare dintre ele, o contabilitate corectă și la zi este esențială — exact ce oferim de peste 22 de ani.",
      "Colaborarea cu firmele din Bârlad se desfășoară simplu și eficient, preponderent online, fără a sacrifica atenția personală și promptitudinea care ne definesc.",
    ],
    "why": [
      ("Experiență cu firme diverse", "Comerț, producție, servicii — adaptăm evidența contabilă specificului fiecărei afaceri din Bârlad."),
      ("Proces simplu, online", "Transmiți documentele electronic și primești situațiile la timp, fără bătăi de cap."),
      ("Specialiști în expertiză", "Expertiza contabilă extrajudiciară este una dintre competențele noastre de bază."),
      ("Termene respectate", "Declarațiile și raportările sunt depuse la timp, ferindu-te de penalități."),
    ],
    "coverage": "Pentru firmele din Bârlad, colaborarea online este rapidă și sigură: documentele se transmit electronic, iar comunicarea este constantă. Atunci când o situație necesită o discuție față în față, programăm o întâlnire.",
    "faq": [
      ("Pot colabora cu voi dacă firma mea este în Bârlad?",
       "Desigur. Lucrăm cu firme din Bârlad în principal online, cu aceeași rigoare și disponibilitate ca pentru clienții de la sediu."),
      ("Ce servicii oferiți firmelor din Bârlad?",
       "Oferim contabilitate completă, salarizare, declarații fiscale, consultanță fiscală și expertiză contabilă extrajudiciară."),
      ("Cum trimit documentele dacă lucrăm la distanță?",
       "Documentele pot fi transmise scanate, prin e-mail sau alte mijloace electronice agreate, în deplină siguranță."),
    ],
  },
  {
    "slug": "contabilitate-iasi", "city": "Iași",
    "title": "Contabilitate Iași — CONTAGEX SRL | Colaborare modernă, 100% online",
    "desc": "Servicii de contabilitate pentru firme din Iași, cu o colaborare modernă, 100% online. Peste 22 de ani de experiență, atenție personală și expertiză contabilă extrajudiciară.",
    "h1": "Contabilitate în Iași — colaborare modernă, 100% online",
    "lead": "Pentru firmele din Iași care caută un contabil dedicat și accesibil, CONTAGEX SRL oferă o colaborare modernă, integral online, cu atenția personală pe care firmele mari rareori o oferă.",
    "intro": [
      "Iași este capitala economică a Moldovei, cu mii de firme active. Multe dintre ele caută un partener contabil care să le răspundă prompt și să le cunoască afacerea — nu un birou aglomerat în care sunt doar un număr.",
      "Colaborăm cu firmele din Iași 100% online: documente electronice, comunicare prin e-mail și telefon, totul rapid și organizat. Beneficiezi de experiența de peste 22 de ani a unui expert contabil, indiferent de distanță.",
    ],
    "why": [
      ("Colaborare 100% online", "Documente electronice și comunicare digitală — fără deplasări, fără timp pierdut."),
      ("Atenție personală", "Vorbești direct cu expertul contabil, care îți cunoaște afacerea în detaliu."),
      ("Experiență solidă", "Peste 22 de ani de practică în contabilitate, la dispoziția firmei tale din Iași."),
      ("Conformitate la zi", "Urmărim permanent modificările legislative și îți ținem firma în regulă."),
    ],
    "coverage": "Pentru clienții din Iași, nu este nevoie de nicio deplasare. Documentele se transmit electronic, iar întreaga colaborare se desfășoară online — eficient, transparent și sigur.",
    "faq": [
      ("Cum funcționează colaborarea la distanță cu o firmă din Iași?",
       "Simplu: ne transmiți documentele în format electronic, comunicăm prin telefon și e-mail, iar noi ținem evidența contabilă la zi. Totul se desfășoară 100% online."),
      ("Trebuie să mă deplasez la Huși?",
       "Nu. Colaborarea cu firmele din Iași este integral online, fără nevoia vreunei deplasări."),
      ("De ce să aleg o firmă din afara Iașiului?",
       "Pentru atenția personală și relația directă cu expertul contabil — combinate cu peste 22 de ani de experiență și tarife competitive."),
    ],
  },
]

def render_city(c):
    R = ""  # paginile de oraș sunt în rădăcină
    path = "/" + c["slug"] + ".html"
    jsonld = [
        org_node(area=c["city"]),
        breadcrumb([("Acasă", "/"), ("Zone deservite", "/#zone"), ("Contabilitate " + c["city"], None)]),
        faqpage(c["faq"]),
    ]
    intro = "\n          ".join(f"<p>{p}</p>" for p in c["intro"])
    why = "\n          ".join(
        f'<article class="card"><h3>{h}</h3><p>{p}</p></article>' for h, p in c["why"])
    services = "\n            ".join(f"<li>{s}</li>" for s in SERVICES)
    faq = "\n          ".join(
        f'<details class="faq-item"><summary>{q}</summary><div class="faq-body"><p>{a}</p></div></details>'
        for q, a in c["faq"])

    body = f"""
  <main id="main">
    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="{R}index.html">Acasă</a><span class="sep">›</span>
          <a href="{R}index.html#zone">Zone deservite</a><span class="sep">›</span>
          Contabilitate {c['city']}
        </nav>
        <p class="eyebrow">Servicii de contabilitate · {c['city']}</p>
        <h1>{c['h1']}</h1>
        <p class="lead">{c['lead']}</p>
        <div class="hero-actions">
          <a href="{R}index.html#contact" class="btn btn-primary">Solicită o ofertă</a>
          <a href="tel:{PHONE}" class="btn btn-ghost">{PHONE_SVG} Sună acum</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container container-narrow">
        {intro}
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">De ce CONTAGEX</p>
          <h2>De ce să alegi CONTAGEX pentru contabilitate în {c['city']}</h2>
        </header>
        <div class="cards">
          {why}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container container-narrow">
        <header class="section-head">
          <p class="eyebrow">Servicii</p>
          <h2>Ce oferim firmelor din {c['city']}</h2>
        </header>
        <ul class="check-list">
            {services}
        </ul>
        <p style="margin-top:18px"><a href="{R}index.html#servicii">Vezi toate serviciile în detaliu →</a></p>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container container-narrow">
        <header class="section-head">
          <p class="eyebrow">Cum lucrăm</p>
          <h2>Colaborarea cu firmele din {c['city']}</h2>
        </header>
        <p>{c['coverage']}</p>
      </div>
    </section>

    <section class="section">
      <div class="container container-narrow">
        <header class="section-head">
          <p class="eyebrow">Întrebări frecvente</p>
          <h2>Contabilitate {c['city']} — întrebări frecvente</h2>
        </header>
        <div class="faq">
          {faq}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>Cauți un contabil de încredere în {c['city']}?</h2>
            <p>Solicită o ofertă personalizată, fără obligații. Îți răspundem rapid.</p>
          </div>
          <a href="{R}index.html#contact" class="btn btn-primary">Contactează-ne</a>
        </div>
      </div>
    </section>
  </main>"""
    write(path, head(c["title"], c["desc"], path, jsonld, R) + header(R) + body + footer(R))

# ============================================================================
# BLOG
ARTICLES = [
  {
    "slug": "microintreprindere-sau-impozit-pe-profit",
    "cat": "Fiscalitate", "date_iso": "2026-05-20", "date_ro": "20 mai 2026",
    "title": "Microîntreprindere sau impozit pe profit? Cum alegi regimul fiscal potrivit",
    "desc": "Ghid practic despre diferența dintre regimul de microîntreprindere și impozitul pe profit și despre factorii care contează atunci când alegi forma de impozitare a firmei tale.",
    "excerpt": "Alegerea între regimul de microîntreprindere și impozitul pe profit influențează direct cât plătești statului. Iată factorii care contează cu adevărat.",
    "body": """
<p>Una dintre cele mai importante decizii fiscale pentru orice firmă este alegerea regimului de impozitare. În România, societățile pot fi, în general, fie microîntreprinderi, fie plătitoare de impozit pe profit. Alegerea corectă poate însemna economii semnificative — sau, dimpotrivă, costuri inutile.</p>

<h2>Ce este o microîntreprindere</h2>
<p>Regimul de microîntreprindere presupune impozitarea veniturilor firmei (cifra de afaceri), nu a profitului. Este, de regulă, simplu de administrat și avantajos pentru firmele cu cheltuieli relativ mici raportate la încasări. Există însă condiții de eligibilitate — legate de cifra de afaceri, numărul de salariați și domeniul de activitate — care se modifică frecvent prin lege.</p>

<h2>Ce înseamnă impozitul pe profit</h2>
<p>În acest regim, firma plătește impozit pe profit, adică pe diferența dintre venituri și cheltuielile deductibile. Devine avantajos atunci când firma are cheltuieli semnificative (marfă, salarii, investiții), pentru că impozitul se aplică doar pe ce rămâne efectiv ca profit.</p>

<h2>Factorii care contează în decizie</h2>
<ul>
  <li><strong>Marja afacerii:</strong> firmele cu marje mari și cheltuieli mici tind să fie avantajate de regimul de microîntreprindere; cele cu cheltuieli mari, de impozitul pe profit.</li>
  <li><strong>Cifra de afaceri:</strong> peste anumite praguri, regimul de microîntreprindere nu mai este permis.</li>
  <li><strong>Numărul de salariați:</strong> influențează atât eligibilitatea, cât și cota aplicabilă.</li>
  <li><strong>Domeniul de activitate:</strong> anumite activități au reguli speciale.</li>
  <li><strong>Planurile de dezvoltare:</strong> dacă firma crește rapid, regimul potrivit azi poate să nu mai fie potrivit la anul.</li>
</ul>

<blockquote>Nu există un răspuns universal valabil. Regimul optim depinde de cifrele concrete ale fiecărei firme și de obiectivele ei de dezvoltare.</blockquote>

<h2>De ce e bine să decizi împreună cu un expert contabil</h2>
<p>Pragurile, cotele și condițiile de eligibilitate se schimbă des în legislația românească. O analiză făcută de un expert contabil, pe baza cifrelor reale ale firmei tale, te ajută să eviți greșeli costisitoare și să alegi varianta care îți lasă mai mulți bani în firmă — în mod legal.</p>
""",
  },
  {
    "slug": "documente-necesare-contabilitate-firma",
    "cat": "Ghid practic", "date_iso": "2026-04-15", "date_ro": "15 aprilie 2026",
    "title": "Ce documente îți trebuie pentru o contabilitate corectă și fără stres",
    "desc": "Lista documentelor pe care orice firmă ar trebui să le predea contabilului lunar și sfaturi practice pentru o evidență contabilă ordonată și conformă.",
    "excerpt": "O contabilitate corectă începe cu documente complete și predate la timp. Iată ce ar trebui să pregătești lunar pentru contabilul tău.",
    "body": """
<p>Multe probleme contabile pornesc de la documente lipsă sau predate cu întârziere. O evidență ordonată îți economisește timp, bani și stresul penalităților. Iată ce documente ar trebui să ajungă, de regulă, la contabilul tău.</p>

<h2>Documente lunare uzuale</h2>
<ul>
  <li><strong>Facturi de vânzare</strong> emise către clienți.</li>
  <li><strong>Facturi de achiziție</strong> de la furnizori, cu toate elementele obligatorii.</li>
  <li><strong>Extrasele de cont bancare</strong> pentru toate conturile firmei.</li>
  <li><strong>Documente de casă:</strong> chitanțe, bonuri fiscale, registrul de casă.</li>
  <li><strong>Contracte</strong> noi sau modificate (clienți, furnizori, chirii, leasing).</li>
  <li><strong>Documente de personal:</strong> pontaje, concedii, modificări de contracte.</li>
  <li><strong>Documente de stoc:</strong> NIR-uri, avize, dacă firma lucrează cu marfă.</li>
</ul>

<h2>Bune practici care îți ușurează viața</h2>
<ul>
  <li>Strânge documentele pe măsură ce apar, nu la final de lună.</li>
  <li>Digitalizează: scanează sau fotografiază documentele și păstrează-le organizat pe luni.</li>
  <li>Verifică datele de pe facturi (denumire, CUI, sumă) înainte de a le accepta.</li>
  <li>Respectă termenele de predare stabilite cu contabilul, pentru a evita aglomerarea.</li>
</ul>

<blockquote>Regula de aur: cu cât documentele sunt mai complete și mai ordonate, cu atât contabilitatea este mai rapidă, mai ieftină și mai sigură.</blockquote>

<h2>Ce câștigi dintr-o evidență ordonată</h2>
<p>O firmă cu documente la zi își cunoaște în orice moment situația reală, depune declarațiile la timp și este pregătită pentru orice control. În plus, contabilul îți poate oferi sfaturi utile atunci când are o imagine clară și completă a activității.</p>
""",
  },
  {
    "slug": "expertiza-contabila-extrajudiciara-ghid",
    "cat": "Expertiză contabilă", "date_iso": "2026-03-10", "date_ro": "10 martie 2026",
    "title": "Expertiza contabilă extrajudiciară: ce este și când ai nevoie de ea",
    "desc": "Ce este expertiza contabilă extrajudiciară, cu ce diferă de cea judiciară și în ce situații te poate ajuta o analiză contabilă independentă realizată de un expert contabil.",
    "excerpt": "Înainte ca o neînțelegere financiară să ajungă în instanță, o expertiză contabilă extrajudiciară îți poate clarifica situația — rapid și obiectiv.",
    "body": """
<p>Expertiza contabilă extrajudiciară este una dintre competențele de bază ale CONTAGEX SRL. Mulți antreprenori nu știu însă exact ce presupune și când le poate fi de folos. Iată un ghid clar.</p>

<h2>Ce este, mai exact</h2>
<p>Este o analiză tehnică și independentă a unor aspecte contabile sau financiare, realizată de un expert contabil <strong>în afara unui proces judiciar</strong>. Spre deosebire de expertiza judiciară (dispusă de instanță), cea extrajudiciară este solicitată direct de o parte interesată — o firmă, un asociat, un creditor.</p>

<h2>În ce situații te ajută</h2>
<ul>
  <li><strong>Litigii comerciale:</strong> pentru a clarifica o situație financiară înainte de a ajunge în instanță.</li>
  <li><strong>Neînțelegeri între asociați:</strong> verificarea corectitudinii înregistrărilor și a distribuirii rezultatelor.</li>
  <li><strong>Verificarea unei afaceri:</strong> înainte de a cumpăra sau a prelua o firmă (due diligence).</li>
  <li><strong>Control intern:</strong> când vrei o opinie independentă asupra propriei contabilități.</li>
  <li><strong>Negocieri:</strong> un raport obiectiv întărește poziția ta la masa discuțiilor.</li>
</ul>

<h2>Cum decurge</h2>
<p>Expertul contabil analizează documentele puse la dispoziție, verifică înregistrările și întocmește un raport clar, motivat, cu concluzii obiective. Acest raport poate fi folosit în negocieri, în relația cu partenerii sau ca bază pentru o eventuală acțiune ulterioară.</p>

<blockquote>O expertiză extrajudiciară poate preveni un proces lung și costisitor, oferind din timp o imagine clară și imparțială asupra situației.</blockquote>

<h2>Cine o poate realiza</h2>
<p>Expertiza contabilă este realizată de un expert contabil cu experiență, capabil să analizeze situații complexe și să le prezinte într-o formă pe înțelesul tuturor. Dacă te confrunți cu o situație în care ai nevoie de o opinie financiară independentă, te putem ajuta.</p>
""",
  },
]

def article_card(a, R):
    return f"""<article class="post-card">
            <div class="post-thumb"></div>
            <div class="post-card-body">
              <span class="post-cat">{a['cat']}</span>
              <h3><a href="{R}blog/{a['slug']}.html">{a['title']}</a></h3>
              <p>{a['excerpt']}</p>
              <div class="post-meta">{a['date_ro']}</div>
              <a class="post-link" href="{R}blog/{a['slug']}.html">Citește articolul →</a>
            </div>
          </article>"""

def render_article(a, others):
    R = "../"  # articolele sunt în /blog/
    path = "/blog/" + a["slug"] + ".html"
    url = SITE + path
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": a["title"], "description": a["desc"],
            "datePublished": a["date_iso"], "dateModified": a["date_iso"],
            "inLanguage": "ro-RO",
            "image": SITE + "/assets/og-image.png",
            "articleSection": a["cat"],
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "author": {"@type": "Organization", "name": "CONTAGEX SRL", "url": SITE + "/"},
            "publisher": {
                "@type": "Organization", "name": "CONTAGEX SRL",
                "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.png"},
            },
        },
        breadcrumb([("Acasă", "/"), ("Noutăți", "/blog/"), (a["title"], None)]),
    ]
    related = "\n          ".join(article_card(o, R) for o in others)
    body = f"""
  <main id="main">
    <article class="article">
      <section class="page-hero">
        <div class="container container-narrow">
          <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="{R}index.html">Acasă</a><span class="sep">›</span>
            <a href="{R}blog/">Noutăți</a><span class="sep">›</span>
            {a['cat']}
          </nav>
          <p class="eyebrow">{a['cat']} · {a['date_ro']}</p>
          <h1>{a['title']}</h1>
        </div>
      </section>

      <section class="section">
        <div class="container container-narrow">
          <div class="article-body">
            {a['body'].strip()}
            <p class="article-disclaimer"><strong>Notă:</strong> Acest articol are caracter informativ general. Legislația fiscală din România se modifică frecvent, iar fiecare situație are particularitățile ei. Pentru o analiză aplicată firmei tale, contactează-ne la <a href="tel:{PHONE}">{PHONE_DISPLAY}</a> sau prin <a href="{R}index.html#contact">formularul de contact</a>.</p>
          </div>

          <div class="related">
            <h2>Alte articole</h2>
            <div class="blog-grid" style="margin-top:22px">
          {related}
            </div>
          </div>
        </div>
      </section>

      <section class="section section-alt">
        <div class="container">
          <div class="cta-band">
            <div>
              <h2>Ai o întrebare despre contabilitatea firmei tale?</h2>
              <p>Vorbește direct cu un expert contabil cu peste 22 de ani de experiență.</p>
            </div>
            <a href="{R}index.html#contact" class="btn btn-primary">Solicită o ofertă</a>
          </div>
        </div>
      </section>
    </article>
  </main>"""
    write(path, head(a["title"], a["desc"], path, jsonld, R, robots="index, follow") + header(R) + body + footer(R))

def render_blog_index():
    R = "../"  # /blog/index.html este în /blog/
    path = "/blog/"
    cards = "\n          ".join(article_card(a, R) for a in ARTICLES)
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "Blog",
            "@id": SITE + "/blog/#blog", "name": "Noutăți fiscale — CONTAGEX SRL",
            "description": "Articole și noutăți despre contabilitate, fiscalitate și expertiză contabilă, de la CONTAGEX SRL.",
            "inLanguage": "ro-RO", "publisher": {"@id": ORG_ID},
            "blogPost": [
                {"@type": "BlogPosting", "headline": a["title"],
                 "url": SITE + "/blog/" + a["slug"] + ".html",
                 "datePublished": a["date_iso"]} for a in ARTICLES
            ],
        },
        breadcrumb([("Acasă", "/"), ("Noutăți", None)]),
    ]
    body = f"""
  <main id="main">
    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="{R}index.html">Acasă</a><span class="sep">›</span>Noutăți fiscale
        </nav>
        <p class="eyebrow">Blog · Noutăți fiscale</p>
        <h1>Noutăți și articole despre contabilitate și fiscalitate</h1>
        <p class="lead">Informații utile pentru antreprenori, explicate pe înțelesul tuturor. Legislația fiscală din România se schimbă des — aici găsești repere clare și actuale.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="blog-grid">
          {cards}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>Ai nevoie de un sfat aplicat firmei tale?</h2>
            <p>Articolele sunt un punct de plecare. Pentru situația ta concretă, vorbește cu un expert.</p>
          </div>
          <a href="{R}index.html#contact" class="btn btn-primary">Contactează-ne</a>
        </div>
      </div>
    </section>
  </main>"""
    write(path + "index.html", head(
        "Noutăți fiscale — CONTAGEX SRL | Blog contabilitate și fiscalitate",
        "Articole și noutăți despre contabilitate, fiscalitate și expertiză contabilă pentru antreprenori, de la CONTAGEX SRL — firmă de contabilitate din Huși.",
        "/blog/", jsonld, R) + header(R) + body + footer(R))

# ============================================================================
if __name__ == "__main__":
    for c in CITIES:
        render_city(c)
    render_blog_index()
    for a in ARTICLES:
        others = [o for o in ARTICLES if o["slug"] != a["slug"]]
        render_article(a, others)
    print("\nGata. Pagini generate.")
