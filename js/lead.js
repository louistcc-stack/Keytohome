// Turns WhatsApp controls into wa.me links from js/site-config.js.
(function () {
  if (!window.SITE || !SITE.WA_NUMBER) return;

  function pageRef() {
    return (document.body.dataset && document.body.dataset.ref) || 'home';
  }

  function utmSource() {
    try { return sessionStorage.getItem('utm_source') || ''; } catch (e) { return ''; }
  }

  // Remember utm_source from the URL so later pages can append it.
  try {
    var q = new URLSearchParams(location.search);
    var src = (q.get('utm_source') || '').trim();
    if (src) sessionStorage.setItem('utm_source', src);
    ['utm_medium', 'utm_campaign'].forEach(function (key) {
      var v = (q.get(key) || '').trim();
      if (v) sessionStorage.setItem(key, v);
    });
  } catch (err) {}

  function messageFor(ref, custom) {
    var base = custom || (SITE.MESSAGES && SITE.MESSAGES[ref]) || SITE.MESSAGES.home;
    var line = base + '\n(ref: ' + ref + ')';
    var src = utmSource();
    if (src) line += '\n(utm_source: ' + src + ')';
    return line;
  }

  window.siteWaHref = function (ref, custom) {
    return 'https://wa.me/' + SITE.WA_NUMBER + '?text=' + encodeURIComponent(messageFor(ref || pageRef(), custom));
  };

  function arm(el, ref) {
    if (!el) return;
    el.href = siteWaHref(ref);
    el.target = '_blank';
    el.rel = 'noopener';
    el.dataset.wa = ref;
  }

  document.querySelectorAll('[data-wa]').forEach(function (el) {
    arm(el, el.dataset.wa);
  });

  var head = document.querySelector('header a.pill');
  if (head && /whatsapp/i.test(head.textContent)) {
    head.classList.remove('gold');
    head.classList.add('wa');
    if (!head.dataset.wa) arm(head, pageRef());
    else arm(head, head.dataset.wa);
  }

  document.querySelectorAll('a[href^="https://wa.me/"]').forEach(function (a) {
    if (a.dataset.wa) return;
    arm(a, pageRef());
  });

  var float = document.querySelector('.wa-float');
  if (float) {
    arm(float, pageRef());
    var label = float.querySelector('span');
    if (label) label.textContent = 'Chat with us';
    float.setAttribute('aria-label', 'Chat with us on WhatsApp');
  }

  function band(place) {
    var d = document.createElement('div');
    d.className = 'wa-band';
    d.dataset.waPlace = place;
    var p = document.createElement('p');
    p.textContent = 'WhatsApp me. I reply myself.';
    var a = document.createElement('a');
    a.className = 'pill wa';
    a.textContent = 'Chat on WhatsApp';
    arm(a, pageRef());
    d.appendChild(p);
    d.appendChild(a);
    return d;
  }

  var main = document.querySelector('main');
  if (main && !document.body.classList.contains('lp') && !main.querySelector('[data-wa-place]')) {
    var kids = Array.prototype.filter.call(main.children, function (n) {
      return n.tagName === 'SECTION' || n.tagName === 'DIV';
    });
    if (kids.length) {
      var mid = kids[Math.min(kids.length - 1, Math.floor(kids.length / 2))];
      mid.parentNode.insertBefore(band('mid'), mid);
    }
    main.appendChild(band('bottom'));
  }

  document.addEventListener('click', function (e) {
    var wa = e.target.closest('[data-wa], .wa-float');
    if (wa && window.trackEvent) {
      trackEvent('whatsapp_click', {ref: wa.dataset.wa || pageRef(), segment: document.body.dataset.segment || ''});
    }
  });
})();
