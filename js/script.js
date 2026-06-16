/* ============================================================
   CONTAGEX SRL — Interacțiuni: meniu mobil, formular, an footer
============================================================ */
(function () {
  'use strict';

  // ---- An curent în footer ----
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---- Meniu mobil ----
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Închide meniul la click pe un link
    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ---- Formular de contact (Formspree, fără reîncărcarea paginii) ----
  var form = document.getElementById('contactForm');
  var status = document.getElementById('formStatus');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Validare nativă
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var originalText = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Se trimite…'; }
      setStatus('', '');

      // Dacă ID-ul Formspree nu a fost configurat încă, oferim mailto ca rezervă
      if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
        sendViaMailto();
        if (btn) { btn.disabled = false; btn.textContent = originalText; }
        return;
      }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            setStatus('Mulțumim! Mesajul a fost trimis. Vă vom contacta în cel mai scurt timp.', 'ok');
          } else {
            return res.json().then(function (data) {
              var msg = (data && data.errors)
                ? data.errors.map(function (x) { return x.message; }).join(', ')
                : 'A apărut o eroare. Încercați din nou sau sunați-ne.';
              setStatus(msg, 'err');
            });
          }
        })
        .catch(function () {
          setStatus('Conexiune eșuată. Vă rugăm sunați la +40 743 085 632.', 'err');
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = originalText; }
        });
    });
  }

  function setStatus(msg, type) {
    if (!status) return;
    status.textContent = msg;
    status.className = 'form-status' + (type ? ' ' + type : '');
  }

  function sendViaMailto() {
    var nume = encodeURIComponent((form.nume && form.nume.value) || '');
    var email = encodeURIComponent((form.email && form.email.value) || '');
    var telefon = encodeURIComponent((form.telefon && form.telefon.value) || '');
    var serviciu = encodeURIComponent((form.serviciu && form.serviciu.value) || '');
    var mesaj = encodeURIComponent((form.mesaj && form.mesaj.value) || '');
    var body =
      'Nume: ' + decodeURIComponent(nume) + '%0D%0A' +
      'Email: ' + decodeURIComponent(email) + '%0D%0A' +
      'Telefon: ' + decodeURIComponent(telefon) + '%0D%0A' +
      'Serviciu: ' + decodeURIComponent(serviciu) + '%0D%0A%0D%0A' +
      decodeURIComponent(mesaj);
    window.location.href =
      'mailto:georgica.aciobanitei@gmail.com?subject=Solicitare%20de%20pe%20site%20CONTAGEX&body=' + body;
    setStatus('Se deschide aplicația de email pentru a trimite mesajul…', 'ok');
  }
})();
