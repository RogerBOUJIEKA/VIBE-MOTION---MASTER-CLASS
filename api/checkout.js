// SasPay checkout (Vercel serverless function).
// Secrets live in Vercel environment variables, never in the site code:
//   SASPAY_SECRET_KEY   secret API key from SasPay (dashboard > Développeur), sk_live_... (scope PAYIN)
//   COURSE_ACCESS_URL   link to the course, shown only after SasPay confirms the payment
//   COURSE_GROUP_URL    WhatsApp group of the students, shown only after a confirmed payment
//   SASPAY_AMOUNT       optional, price in FCFA (default 5500)
//   SASPAY_CURRENCY     optional, ISO currency (default XOF)
// GET  /api/checkout              -> { enabled }
// POST /api/checkout              -> { url, id }   creates a hosted SasPay checkout session
// GET  /api/checkout?session=<id> -> { paid, access? }   asks SasPay for the real status
const API = 'https://api.saspay.me/api/v1';
const RETURN_URL = 'https://www.rogerboujieka.com/?paiement=merci';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

async function call(key, path, init) {
  const r = await fetch(API + path, Object.assign({}, init, {
    headers: Object.assign({ Authorization: 'Bearer ' + key, Accept: 'application/json' }, init && init.body ? { 'Content-Type': 'application/json' } : {}),
    signal: AbortSignal.timeout(15000)
  }));
  const j = await r.json().catch(() => null);
  // SasPay wraps results as { success, data, code }; accept the bare object too
  const data = j && j.data && typeof j.data === 'object' ? j.data : j;
  return { ok: r.ok, status: r.status, data, err: j && j.error };
}
const errCode = e => (e && (e.code || Object.keys(e).join(','))) || '';

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const key = process.env.SASPAY_SECRET_KEY;
  const enabled = !!key;
  const q = req.query || {};

  if (req.method === 'GET' && !q.session) return res.status(200).json({ enabled });
  if (!enabled) return res.status(503).json({ error: 'not_configured' });

  // payment check after the buyer comes back from SasPay
  if (req.method === 'GET') {
    const id = String(q.session);
    if (!UUID.test(id)) return res.status(400).json({ error: 'invalid_session' });
    try {
      const r = await call(key, '/checkout-sessions/' + id + '/status/');
      if (r.status === 404) return res.status(404).json({ error: 'not_found' });
      if (!r.ok || !r.data) { console.error('saspay status failed', r.status, errCode(r.err)); return res.status(502).json({ error: 'status_failed' }); }
      const paid = r.data.status === 'PAID' && r.data.transaction_status === 'SUCCESS';
      const out = { paid, status: r.data.status || '' };
      if (paid) { out.access = process.env.COURSE_ACCESS_URL || ''; out.group = process.env.COURSE_GROUP_URL || ''; }
      return res.status(200).json(out);
    } catch (e) {
      console.error('saspay unreachable', e && e.name);
      return res.status(502).json({ error: 'status_unreachable' });
    }
  }

  if (req.method !== 'POST') { res.setHeader('Allow', 'GET, POST'); return res.status(405).json({ error: 'method_not_allowed' }); }

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'invalid_body' });

  const firstName = clean(body.firstName, 60), lastName = clean(body.lastName, 60);
  const email = clean(body.email, 120).toLowerCase(), phone = clean(body.phone, 24).replace(/[^\d+]/g, '');
  if (!firstName || !lastName) return res.status(400).json({ error: 'name_required' });
  if (!EMAIL.test(email)) return res.status(400).json({ error: 'invalid_email' });

  // the price is set here on the server, never taken from the browser
  const amount = (Number(process.env.SASPAY_AMOUNT) > 0 ? Number(process.env.SASPAY_AMOUNT) : 5500).toFixed(2);
  const payload = {
    amount, currency: (process.env.SASPAY_CURRENCY || 'XOF').toUpperCase().slice(0, 3),
    description: 'Formation Vibe Motion',
    customer_email: email, customer_name: firstName + ' ' + lastName,
    return_url: RETURN_URL, metadata: { source: 'rogerboujieka.com' }
  };
  if (phone.length >= 8) payload.customer_phone = phone;

  try {
    const r = await call(key, '/checkout-sessions/', { method: 'POST', body: JSON.stringify(payload) });
    const url = r.data && r.data.checkout_url, id = r.data && r.data.id;
    if (!r.ok || typeof url !== 'string' || !/^https:\/\//.test(url) || !UUID.test(String(id))) {
      // log the SasPay status only, never the key or the buyer's details
      console.error('saspay checkout failed', r.status, errCode(r.err));
      return res.status(502).json({ error: 'checkout_failed' });
    }
    return res.status(200).json({ url, id });
  } catch (e) {
    console.error('saspay unreachable', e && e.name);
    return res.status(502).json({ error: 'checkout_unreachable' });
  }
};
