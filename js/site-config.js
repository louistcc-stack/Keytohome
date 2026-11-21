// Key To Home settings. Paste real IDs only. Leave a value '' until you have it.
// js/analytics.js loads a vendor script only when its ID is set.
var SITE = {
  // Louis's own WhatsApp. Country code + number, no + or spaces.
  WA_NUMBER: '6581668767',
  PHONE_DISPLAY: '+65 8166 8767',
  PHONE_TEL: '+6581668767',
  GA4_ID: '',
  META_PIXEL_ID: '',
  GADS_ID: '',
  GADS_LABELS: {whatsapp:'', call:'', form:'', book:''},
  BOOKING_URL: '',
  FORMSUBMIT: 'https://formsubmit.co/ajax/louistcc@gmail.com'
};

// Pre-filled WhatsApp openers. lead.js appends (ref: …) and utm_source when set.
SITE.MESSAGES = {
  home: "Hi Louis, I saw the Key To Home site and would like to chat.",
  about: "Hi Louis, I'd like a free consultation",
  'track-record': "Hi Louis, I saw your track record and would like to chat about my home.",
  reviews: "Hi Louis, I read your reviews and would like to chat about my home.",
  launches: "Hi Louis, I'm an HDB owner thinking of upgrading",
  valuation: "Hi Louis, I'd like an indicative valuation of my HDB",
  octa: "Hi Louis, I'd like an Octa Score on a home I'm looking at.",
  contact: "Hi Louis, I'd like a free consultation",
  'hdb-upgrader': "Hi Louis, I'm an HDB owner thinking of upgrading",
  'hdb-valuation': "Hi Louis, I'd like an indicative valuation of my HDB",
  'condo-valuation': "Hi Louis, I'd like an indicative valuation of my condo",
  'free-consultation': "Hi Louis, I'd like a free consultation"
};

// Older scripts still read these names. The number always comes from SITE.
var KTH_WHATSAPP = SITE.WA_NUMBER;
var KTH_EMAIL = '';
