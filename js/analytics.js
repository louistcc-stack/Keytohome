// Sends whatsapp_click, call_click, form_submit and book_click.
// A vendor script is added only when js/site-config.js has that ID.
(function () {
  if (!window.SITE) return;
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign'];

  try {
    var q = new URLSearchParams(location.search);
    UTM_KEYS.forEach(function (key) {
      var v = (q.get(key) || '').trim();
      if (v) sessionStorage.setItem(key, v);
    });
  } catch (err) {}

  function utm(key) {
    try { return sessionStorage.getItem(key) || ''; } catch (e) { return ''; }
  }

  function loadScript(src) {
    var s = document.createElement('script');
    s.async = true;
    s.src = src;
    document.head.appendChild(s);
  }

  var ga = SITE.GA4_ID || '';
  var ads = SITE.GADS_ID || '';
  if (ga || ads) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    gtag('js', new Date());
    loadScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(ga || ads));
    if (ga) gtag('config', ga);
    if (ads) gtag('config', ads);
  }

  var pixel = SITE.META_PIXEL_ID || '';
  if (pixel) {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = '2.0';
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', pixel);
    fbq('track', 'PageView');
  }

  function eventId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'evt-' + Date.now() + '-' + Math.floor(Math.random() * 1e6);
  }

  var META = {whatsapp_click:'Contact', call_click:'Contact', form_submit:'Lead', book_click:'Schedule'};
  var ADS = {whatsapp_click:'whatsapp', call_click:'call', form_submit:'form', book_click:'book'};

  window.trackEvent = function (name, extra) {
    var page = location.pathname.split('/').pop() || 'index.html';
    var params = {
      page: page,
      segment: (extra && extra.segment) || (document.body.dataset && document.body.dataset.segment) || '',
      ref: (extra && extra.ref) || (document.body.dataset && document.body.dataset.ref) || '',
      utm_source: utm('utm_source'),
      utm_medium: utm('utm_medium'),
      utm_campaign: utm('utm_campaign')
    };
    if (window.gtag && ga) gtag('event', name, params);
    var labels = SITE.GADS_LABELS || {};
    var label = ADS[name] && labels[ADS[name]];
    if (window.gtag && ads && label) gtag('event', 'conversion', {send_to: ads + '/' + label});
    if (window.fbq && pixel && META[name]) fbq('track', META[name], params, {eventID: eventId()});
    return params;
  };
})();
