// Unit test of api/checkout.js (SasPay) with a fake fetch: no real SasPay call, dummy key
const fn = require('../../api/checkout.js');
const ok = (c, m) => console.log((c ? 'OK  ' : 'FAIL') + ' ' + m);
function res() { const r = { code: 0, body: null, headers: {} }; r.status = c => { r.code = c; return r; }; r.json = b => { r.body = b; return r; }; r.setHeader = (k, v) => { r.headers[k] = v; }; return r; }
const SID = 'c9a17e2c-4b1a-4f0e-9c3d-2a1b3c4d5e6f';
(async () => {
  let sent = null, statusReply = null;
  global.fetch = async (url, init) => {
    sent = { url, init, body: init.body ? JSON.parse(init.body) : null };
    if (url.endsWith('/status/')) return statusReply;
    return { ok: true, status: 201, json: async () => ({ success: true, code: 201, data: { id: SID, checkout_url: 'https://pay.saspay.me/checkout/abc==', status: 'PENDING' } }) };
  };
  delete process.env.SASPAY_SECRET_KEY; delete process.env.COURSE_ACCESS_URL; delete process.env.SASPAY_AMOUNT;
  let r = res(); await fn({ method: 'GET', query: {} }, r); ok(r.code === 200 && r.body.enabled === false, 'GET without key -> disabled');
  r = res(); await fn({ method: 'POST', body: {} }, r); ok(r.code === 503, 'POST without key -> 503');

  process.env.SASPAY_SECRET_KEY = 'sk_test_dummy'; process.env.COURSE_ACCESS_URL = 'https://course.example/acces';
  r = res(); await fn({ method: 'GET', query: {} }, r); ok(r.body.enabled === true, 'GET with key -> enabled');
  r = res(); await fn({ method: 'POST', body: { firstName: 'A', lastName: 'N', email: 'bad' } }, r); ok(r.code === 400 && r.body.error === 'invalid_email', 'bad email rejected');
  r = res(); await fn({ method: 'POST', body: { firstName: '', lastName: 'N', email: 'a@b.cm' } }, r); ok(r.code === 400, 'missing name rejected');
  r = res(); await fn({ method: 'POST', body: JSON.stringify({ firstName: ' Aïcha ', lastName: 'Ngo', email: 'Aicha@Mail.CM', phone: '+237 6 78 59 42 47', amount: '1' }) }, r);
  ok(r.code === 200 && r.body.url === 'https://pay.saspay.me/checkout/abc==' && r.body.id === SID, 'returns SasPay page + session id (envelope unwrapped)');
  ok(sent.url === 'https://api.saspay.me/api/v1/checkout-sessions/' && sent.init.method === 'POST', 'calls POST /checkout-sessions/');
  ok(sent.init.headers.Authorization === 'Bearer sk_test_dummy', 'Bearer key header');
  const b = sent.body;
  ok(b.amount === '5500.00' && b.currency === 'XOF' && b.customer_name === 'Aïcha Ngo' && b.customer_email === 'aicha@mail.cm' && b.customer_phone === '+237678594247' && b.return_url.startsWith('https://www.rogerboujieka.com/?paiement=merci'), 'payload ' + JSON.stringify(b));
  ok(!JSON.stringify(r.body).includes('sk_test_dummy'), 'key never returned to the browser');
  process.env.SASPAY_AMOUNT = '7000';
  r = res(); await fn({ method: 'POST', body: { firstName: 'A', lastName: 'B', email: 'a@b.cm' } }, r); ok(sent.body.amount === '7000.00', 'price comes from SASPAY_AMOUNT, not the browser');

  // status check
  statusReply = { ok: true, status: 200, json: async () => ({ success: true, data: { id: SID, status: 'PAID', transaction_status: 'SUCCESS' } }) };
  r = res(); await fn({ method: 'GET', query: { session: SID } }, r);
  ok(r.body.paid === true && r.body.access === 'https://course.example/acces' && sent.url.endsWith('/checkout-sessions/' + SID + '/status/'), 'paid session -> access link');
  statusReply = { ok: true, status: 200, json: async () => ({ success: true, data: { id: SID, status: 'PENDING', transaction_status: 'PENDING' } }) };
  r = res(); await fn({ method: 'GET', query: { session: SID } }, r); ok(r.body.paid === false && !('access' in r.body), 'pending session -> no access link');
  statusReply = { ok: true, status: 200, json: async () => ({ data: { status: 'PAID', transaction_status: 'FAILED' } }) };
  r = res(); await fn({ method: 'GET', query: { session: SID } }, r); ok(r.body.paid === false && !r.body.access, 'failed transaction -> no access');
  r = res(); await fn({ method: 'GET', query: { session: '../users/' } }, r); ok(r.code === 400, 'malformed session id refused');
  statusReply = { ok: false, status: 404, json: async () => ({ success: false, error: { code: 'not_found' } }) };
  r = res(); await fn({ method: 'GET', query: { session: SID } }, r); ok(r.code === 404, 'unknown session -> 404');

  global.fetch = async () => ({ ok: false, status: 401, json: async () => ({ success: false, error: { message: 'x', code: 'invalid_api_key' } }) });
  const ce = console.error; let logged = ''; console.error = (...a) => { logged += a.join(' '); };
  r = res(); await fn({ method: 'POST', body: { firstName: 'A', lastName: 'B', email: 'a@b.cm' } }, r); console.error = ce;
  ok(r.code === 502 && !logged.includes('sk_test_dummy') && logged.includes('invalid_api_key') && !logged.includes('a@b.cm'), 'SasPay error -> 502, logged without key or buyer data');
  r = res(); await fn({ method: 'DELETE', query: {} }, r); ok(r.code === 405, 'other methods refused');
})();
