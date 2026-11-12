// Maketou checkout (Vercel serverless function).
// The API key and the product id live in Vercel environment variables, never in the site code:
//   MAKETOU_API_KEY     secret key from Maketou (store > Autres > Clés API)
//   MAKETOU_PRODUCT_ID  public id of the course product (product page > Partager > Identifiant public)
// GET  /api/checkout -> { enabled }            the site uses Maketou only when both are set
// POST /api/checkout -> { url }                creates a cart and returns the Maketou payment page
const API = 'https://api.maketou.net/api/v1/stores/cart/checkout';
const RETURN_URL = 'https://www.rogerboujieka.com/?paiement=merci';

const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const key = process.env.MAKETOU_API_KEY, product = process.env.MAKETOU_PRODUCT_ID;
  const enabled = !!(key && product);

  if (req.method === 'GET') return res.status(200).json({ enabled });
  if (req.method !== 'POST') { res.setHeader('Allow', 'GET, POST'); return res.status(405).json({ error: 'method_not_allowed' }); }
  if (!enabled) return res.status(503).json({ error: 'not_configured' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'invalid_body' });

  const firstName = clean(body.firstName, 60), lastName = clean(body.lastName, 60);
  const email = clean(body.email, 120).toLowerCase(), phone = clean(body.phone, 24).replace(/[^\d+]/g, '');
  if (!firstName || !lastName) return res.status(400).json({ error: 'name_required' });
  if (!EMAIL.test(email)) return res.status(400).json({ error: 'invalid_email' });

  const payload = { productDocumentId: product, email, firstName, lastName, redirectURL: RETURN_URL, meta: { source: 'rogerboujieka.com' } };
  if (phone.length >= 8) payload.phone = phone;

  try {
    const r = await fetch(API, {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(15000)
    });
    const data = await r.json().catch(() => null);
    const url = data && data.redirectUrl;
    if (!r.ok || typeof url !== 'string' || !/^https:\/\//.test(url)) {
      // log the Maketou status only, never the key or the buyer's details
      console.error('maketou checkout failed', r.status, data && (data.code || data.error || data.message));
      return res.status(502).json({ error: 'checkout_failed' });
    }
    return res.status(200).json({ url });
  } catch (e) {
    console.error('maketou unreachable', e && e.name);
    return res.status(502).json({ error: 'checkout_unreachable' });
  }
};
