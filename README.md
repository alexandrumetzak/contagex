# Site CONTAGEX SRL

Site de prezentare pentru **CONTAGEX SRL** — firmă de contabilitate din Huși, jud. Vaslui.
Static (HTML/CSS/JS), rapid, optimizat din start pentru **SEO** și **AEO** (Answer Engine Optimization).

- **CUI:** 16173016 · **Nr. Reg. Com.:** J37/126/2004
- **Telefon:** +40 743 085 632 · **E-mail:** georgica.aciobanitei@gmail.com
- **Sediu:** Str. 1 Decembrie nr. 6, bl. 6, sc. B, ap. 23, Mun. Huși, jud. Vaslui

---

## 📁 Structura proiectului

```
.
├── index.html            # Pagina principală (toate secțiunile + date structurate)
├── 404.html              # Pagină de eroare
├── robots.txt            # Reguli crawlere (inclusiv crawlere AI pentru AEO)
├── sitemap.xml           # Harta site-ului pentru motoare de căutare
├── site.webmanifest      # Manifest PWA
├── build.py              # Generator pentru paginile de oraș și blog (vezi mai jos)
│
├── contabilitate-husi.html      # Pagini SEO local (generate cu build.py)
├── contabilitate-vaslui.html
├── contabilitate-barlad.html
├── contabilitate-iasi.html
│
├── blog/                 # Noutăți fiscale (generate cu build.py)
│   ├── index.html        # Lista articolelor
│   ├── microintreprindere-sau-impozit-pe-profit.html
│   ├── documente-necesare-contabilitate-firma.html
│   └── expertiza-contabila-extrajudiciara-ghid.html
│
├── css/styles.css        # Stiluri
├── js/script.js          # Meniu mobil + formular de contact
└── assets/
    ├── favicon.svg
    ├── emblem.svg                    # Emblema (logo-ul folosit în antet/subsol)
    ├── logo.svg / logo.png
    └── og-image.svg / og-image.png   # Imagine pentru distribuire pe rețele sociale
```

---

## 🏙️ Pagini per oraș și 📰 Blog (generate cu `build.py`)

Pentru un SEO local mai puternic, site-ul are pagini dedicate fiecărui oraș
(Huși, Vaslui, Bârlad, Iași), fiecare cu conținut **unic** și date structurate
`AccountingService` + `FAQPage`. Blogul (`/blog/`) aduce conținut proaspăt,
care ajută la poziționarea în Google și la AEO.

Aceste pagini sunt **generate automat** dintr-un singur loc, ca să rămână
consecvente (antet, subsol, stiluri identice). Pentru a le re-genera după modificări:

```bash
python3 build.py
```

**Cum adaugi un oraș nou:** în `build.py`, adaugă o intrare în lista `CITIES`
(slug, titlu, descriere, conținut, întrebări) și rulează din nou scriptul.

**Cum adaugi un articol nou pe blog:** adaugă o intrare în lista `ARTICLES`
din `build.py` (slug, titlu, categorie, dată, text) și rulează scriptul. Apoi
adaugă URL-ul în `sitemap.xml` și, opțional, un card în secțiunea „Noutăți" din `index.html`.

> După generare, paginile sunt fișiere HTML statice obișnuite — `build.py` nu
> este necesar pe server, ci doar la editarea conținutului.

---

## ▶️ Testare locală

Deschide un terminal în acest folder și rulează:

```bash
python3 -m http.server 8000
```

Apoi accesează **http://localhost:8000** în browser.
(Deschiderea directă a fișierului `index.html` funcționează, dar serverul local reproduce fidel căile absolute `/css`, `/js`, `/assets`.)

---

## ✉️ Activarea formularului de contact (Formspree)

Formularul folosește **Formspree** ca să trimită mesajele pe e-mailul directorului. Pași:

1. Creează un cont gratuit pe **https://formspree.io** folosind adresa `georgica.aciobanitei@gmail.com`.
2. Creează un formular nou („New form") — vei primi un endpoint de forma:
   `https://formspree.io/f/abcdwxyz`
3. În `index.html`, înlocuiește `YOUR_FORM_ID` din linia:
   ```html
   <form ... action="https://formspree.io/f/YOUR_FORM_ID" method="POST" ...>
   ```
   cu ID-ul real (ex.: `https://formspree.io/f/abcdwxyz`).
4. Trimite un mesaj de test și confirmă adresa de e-mail (Formspree cere o confirmare la prima trimitere).

> Până la configurare, formularul deschide automat aplicația de e-mail a vizitatorului (fallback `mailto:`), deci nu rămâne nefuncțional.

---

## 🌐 Site live (GitHub Pages)

Site-ul este publicat automat prin GitHub Pages:

- **Repo:** https://github.com/alexandrumetzak/contagex
- **URL public (accesibil de pe orice dispozitiv):** https://alexandrumetzak.github.io/contagex/

**Cum actualizezi site-ul live:** orice modificare urcată pe branch-ul `main`
declanșează automat re-publicarea (în ~1-2 minute):

```bash
# după ce ai editat fișierele (și, dacă e cazul, ai rulat: python3 build.py)
git add -A
git commit -m "Descriere modificare"
git push
```

> Căile interne sunt relative tocmai pentru ca site-ul să funcționeze corect
> servit din subfolderul `/contagex/`. Când vei conecta domeniul `contagex.ro`,
> site-ul va funcționa identic (relativ = merge și la rădăcină, și în subfolder).

---

## 🚀 Publicare pe alt hosting (opțional)

### Opțiunea A — Netlify (recomandat, gratuit)
1. Cont pe https://netlify.com → „Add new site" → „Deploy manually".
2. Trage tot folderul în zona de upload. Gata.
3. Adaugă domeniul `contagex.ro` din „Domain settings".

### Opțiunea B — Hosting clasic (cPanel / FTP)
Încarcă **tot conținutul** folderului în `public_html/` (sau rădăcina domeniului). Nu necesită PHP/baze de date.

### Opțiunea C — GitHub Pages
Urcă fișierele într-un repo și activează Pages din Settings → Pages.

---

## 🔧 După publicare — înlocuiește domeniul

Site-ul folosește `https://www.contagex.ro/` ca domeniu canonic. Dacă domeniul final diferă,
caută și înlocuiește `www.contagex.ro` în: `index.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`.

---

## 📈 Checklist SEO + AEO (de făcut după lansare)

Site-ul vine deja cu: titluri și meta descrieri optimizate, date structurate JSON-LD
(`AccountingService`, `WebSite`, `FAQPage`), meta geo, Open Graph, `robots.txt`, `sitemap.xml`,
HTML semantic, design responsive și conținut local (Huși/Vaslui/Bârlad/Iași). Pași externi:

- [ ] **Google Business Profile** — creează/revendică fișa firmei (cel mai important pas pentru vizibilitate locală). Folosește EXACT aceeași denumire, adresă și telefon (NAP) ca pe site.
- [ ] **Google Search Console** — adaugă proprietatea, verifică-o și trimite `sitemap.xml`.
- [ ] **Bing Webmaster Tools** — adaugă site-ul (Bing alimentează și răspunsurile AI).
- [ ] **Test date structurate** — verifică în https://search.google.com/test/rich-results
- [ ] **Recenzii Google** — încurajează clienții să lase recenzii (semnal puternic de ranking local).
- [ ] Înscriere în directoare locale (Pagini Aurii, hartă Google).
- [ ] Verifică viteza în PageSpeed Insights (site-ul este deja foarte ușor).

### Despre AEO (Answer Engine Optimization)
Secțiunea **Întrebări frecvente** + datele `FAQPage` sunt scrise în format întrebare-răspuns,
exact ce „citează" Google (featured snippets) și asistenții AI (ChatGPT, Perplexity, Gemini).
`robots.txt` permite explicit crawlerele AI (`GPTBot`, `ClaudeBot`, `PerplexityBot` etc.).
Pentru rezultate mai bune în timp, adaugă periodic noi întrebări reale ale clienților.

---

## 🔄 Actualizări legislative / conținut

Pentru a păstra site-ul „la zi" (cum cere și mesajul firmei):
- Actualizează periodic secțiunea **FAQ** cu întrebări reale ale clienților.
- La modificări fiscale importante, poți adăuga o secțiune scurtă de noutăți/articole — acest lucru ajută și SEO-ul (conținut proaspăt).
- Actualizează `lastmod` în `sitemap.xml` când modifici conținutul.

---

© CONTAGEX SRL. Site realizat ca site static, fără costuri de mentenanță server.
