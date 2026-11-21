# Key To Home

Personal site for Louis Tay, a Singapore property agent with Huttons Asia Pte Ltd (CEA R000567G, agency licence L3008899K).

Static files at the repo root. No build step.

Preview locally:

```bash
python3 -m http.server 8765
```

Then open http://127.0.0.1:8765/

While this is a preview, every page sends `noindex`.

## Tracking setup

Paste IDs in `js/site-config.js`. Leave a value as `''` until you have it. `js/analytics.js` does not load GA4, the Meta Pixel or Google Ads unless that ID is set.

| Setting | What to paste |
| --- | --- |
| `GA4_ID` | GA4 measurement ID, such as `G-XXXXXXXX` |
| `META_PIXEL_ID` | Meta Pixel ID |
| `GADS_ID` | Google Ads ID, such as `AW-XXXXXXXX` |
| `GADS_LABELS.whatsapp` | Conversion label for a WhatsApp click |
| `GADS_LABELS.call` | Conversion label for a phone click |
| `GADS_LABELS.form` | Conversion label for a form submit |
| `GADS_LABELS.book` | Conversion label for a booking click |
| `BOOKING_URL` | Booking link. "Book a consult" stays hidden while this is empty. |
| `WA_NUMBER` | Already Louis's WhatsApp number. Do not change it. |

Events, and the Meta standard event each one maps to:

- `whatsapp_click` — Contact
- `call_click` — Contact
- `form_submit` — Lead
- `book_click` — Schedule

Every event includes `page`, `segment`, `ref`, `utm_source`, `utm_medium` and `utm_campaign`. Those UTM values are kept in `sessionStorage`. Meta events also send an `eventID`.

Meta CAPI comes later. The browser pixel cannot send server events by itself. A later step can use Meta's CAPI Gateway, or a small server, and pass the same `eventID` so the click and the server event count once.
