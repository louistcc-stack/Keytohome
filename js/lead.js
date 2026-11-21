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
      return;
    }
    var tel = e.target.closest('a[href^="tel:"]');
    if (tel && window.trackEvent) {
      trackEvent('call_click', {ref: pageRef(), segment: document.body.dataset.segment || ''});
      return;
    }
    var book = e.target.closest('[data-book]');
    if (book && SITE.BOOKING_URL && window.trackEvent) {
      trackEvent('book_click', {ref: pageRef(), segment: document.body.dataset.segment || ''});
    }
  });

  document.querySelectorAll('[data-book]').forEach(function (a) {
    if (SITE.BOOKING_URL) {
      a.hidden = false;
      a.href = SITE.BOOKING_URL;
      a.target = '_blank';
      a.rel = 'noopener';
    } else {
      a.hidden = true;
    }
  });

  window.LEAD_HANDLES_FORMS = true;

  function say(note, text, color) {
    if (!note) return;
    note.hidden = false;
    note.textContent = text;
    note.style.color = color;
  }

  document.querySelectorAll('form.a88-lead').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      e.stopImmediatePropagation();
      var d = new FormData(f);
      var note = f.querySelector('.form-note');
      var name = (d.get('name') || '').toString().trim();
      var phone = (d.get('phone') || '').toString().trim();
      if (!name || !/^[+\d][\d\s-]{6,}$/.test(phone)) {
        say(note, 'Please add your name and a valid mobile number.', '#b42318');
        return;
      }
      if (!d.get('consent')) {
        say(note, 'Please tick the consent box so I can contact you.', '#b42318');
        return;
      }
      if ((d.get('_honey') || '').toString().trim()) return;
      var ref = f.dataset.ref || pageRef();
      var pick = function (key) { return (d.get(key) || '').toString().trim(); };
      var lines = ['Name: ' + name, 'Mobile: ' + phone];
      var timeline = pick('timeline');
      var sell = pick('sell_first');
      var goal = pick('goal');
      var type = pick('type');
      var topic = pick('topic');
      var address = pick('address');
      var unit = pick('unit');
      var project = pick('project');
      var intent = pick('intent');
      var message = pick('message');
      if (timeline) lines.push('When do you plan to move?: ' + timeline);
      if (sell) lines.push('Do you need to sell before you buy?: ' + sell);
      if (goal) lines.push('Goal: ' + (goal === 'sell' ? "What's my home worth?" : 'Planning an HDB upgrade'));
      if (type) lines.push('Property type: ' + type);
      if (topic) lines.push('Interested in: ' + topic);
      if (address) lines.push('Property address: ' + address);
      if (unit) lines.push('Unit no.: ' + unit);
      if (project) lines.push('Project / address: ' + project);
      if (intent) lines.push('Buying, selling or upgrading: ' + intent);
      if (message) lines.push('Message: ' + message);
      var intro = (SITE.MESSAGES && SITE.MESSAGES[ref]) || SITE.MESSAGES.home;
      window.open(siteWaHref(ref, intro + '\n' + lines.join('\n')), '_blank');
      if (window.trackEvent) trackEvent('form_submit', {ref: ref, segment: f.dataset.segment || document.body.dataset.segment || ''});
      if (!f.classList.contains('lp-lead')) {
        say(note, 'Thanks, ' + name + '! WhatsApp should have opened with your details. Just tap send.', '#3fae6a');
        f.reset();
        return;
      }
      say(note, 'Sending...', '#5C554C');
      var payload = {
        _subject: (f.dataset.subject || 'Key To Home lead') + ' [' + ref + ']',
        _template: 'table',
        _captcha: 'false',
        name: name,
        phone: phone,
        page: location.pathname,
        ref: ref,
        timeline: timeline,
        sell_first: sell,
        goal: goal,
        type: type,
        topic: topic,
        address: address,
        unit: unit,
        project: project,
        intent: intent,
        message: message
      };
      fetch(SITE.FORMSUBMIT, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', Accept: 'application/json'},
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (!r.ok) throw 0;
        say(note, 'Thanks, ' + name + '! WhatsApp should have opened, and I have your details.', '#3fae6a');
        f.reset();
      }).catch(function () {
        say(note, 'Thanks, ' + name + '! WhatsApp should have opened with your details. Just tap send.', '#3fae6a');
      });
    }, true);
  });
})();
