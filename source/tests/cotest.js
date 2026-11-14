// Checkout flow in the browser with /api/checkout simulated (enabled and disabled)
const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'OK  ' : 'FAIL') + ' ' + m);
(async () => {
  const b = await chromium.launch();
  for (const [dev, w, h, mob] of [['phone', 390, 844, true], ['desktop', 1440, 900, false]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mob, hasTouch: mob, deviceScaleFactor: mob ? 2 : 1 });
    const p = await ctx.newPage(); const errs = []; let posted = null;
    p.on('pageerror', e => errs.push(e.message));
    await p.route('**/api/checkout', r => {
      if (r.request().method() === 'GET') return r.fulfill({ status: 200, contentType: 'application/json', body: '{"enabled":true}' });
      posted = JSON.parse(r.request().postData());
      if (posted.email === 'fail@test.cm') return r.fulfill({ status: 502, contentType: 'application/json', body: '{"error":"checkout_failed"}' });
      return r.fulfill({ status: 200, contentType: 'application/json', body: '{"url":"https://pay.example.test/ok","id":"c9a17e2c-4b1a-4f0e-9c3d-2a1b3c4d5e6f"}' });
    });
    await p.route('https://pay.example.test/**', r => r.fulfill({ status: 200, contentType: 'text/html', body: '<h1>PAY</h1>' }));
    await p.route(/^https?:\/\/(?!localhost)(?!pay\.example\.test)/, r => r.abort());
    await p.addInitScript(() => { localStorage.setItem('mc_lang', 'fr'); sessionStorage.setItem('mc_cbar', '0'); sessionStorage.setItem('mc_toast', '0'); });
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1500);
    await p.click('#hero-cta .js-cta'); await p.waitForTimeout(600);
    ok(await p.$eval('#co', e => !e.hidden && e.classList.contains('on')) && p.url().includes('localhost'), dev + ': CTA opens the form instead of leaving');
    await p.screenshot({ path: `${process.argv[2]}/co-${dev}.png` });
    await p.click('.co-go'); await p.waitForTimeout(200);
    ok(await p.$eval('.co-err', e => !e.hidden && e.textContent.includes('prénom')), dev + ': empty form -> message');
    await p.fill('input[name=firstName]', 'Aïcha'); await p.fill('input[name=lastName]', 'Ngo'); await p.fill('input[name=email]', 'fail@test.cm');
    await p.click('.co-go'); await p.waitForTimeout(600);
    ok(await p.$eval('.co-err', e => !e.hidden && e.textContent.includes('WhatsApp')) && !(await p.$eval('.co-go', e => e.disabled)), dev + ': server error -> message, button usable again');
    await p.fill('input[name=email]', 'aicha@test.cm'); await p.fill('input[name=phone]', '+237 678 00 00 00');
    await p.click('.co-go'); await p.waitForURL('https://pay.example.test/ok', { timeout: 5000 }).catch(() => {});
    ok(p.url() === 'https://pay.example.test/ok', dev + ': redirected to the payment page');
    ok(posted && posted.firstName === 'Aïcha' && posted.email === 'aicha@test.cm' && posted.phone.includes('678'), dev + ': sent ' + JSON.stringify(posted));
    // return from SasPay: paid -> access link
    const p3 = await ctx.newPage(); let polls = 0;
    await p3.route('**/api/checkout**', r => { const u = r.request().url();
      if (!u.includes('session=')) return r.fulfill({ status: 200, contentType: 'application/json', body: '{"enabled":true}' });
      polls++; return r.fulfill({ status: 200, contentType: 'application/json', body: polls < 2 ? '{"paid":false,"status":"PENDING"}' : '{"paid":true,"status":"PAID","access":"https://course.example/acces","group":"https://chat.whatsapp.com/TEST"}' }); });
    await p3.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    await p3.goto('http://localhost:8765/index.html?paiement=merci'); await p3.waitForTimeout(800);
    ok(await p3.evaluate(() => localStorage.getItem('mc_sess')) === 'c9a17e2c-4b1a-4f0e-9c3d-2a1b3c4d5e6f', dev + ': session id kept for the return');
    ok(await p3.$eval('#ty', e => !e.hidden && e.classList.contains('wait')) && p3.url().endsWith('index.html'), dev + ': return -> checking sheet, address cleaned');
    await p3.waitForSelector('#ty .ty-go:not([hidden])', { timeout: 9000 }).catch(() => {});
    ok(await p3.$eval('#ty .ty-go', e => !e.hidden && e.href === 'https://course.example/acces' && document.querySelector('#ty .ty-re').offsetHeight === 0) && polls === 2, dev + ': confirmed after polling -> access button');
    ok(await p3.$eval('#ty .ty-grp', e => e.offsetHeight > 0 && e.href === 'https://chat.whatsapp.com/TEST'), dev + ': students group button shown');
    await p3.screenshot({ path: `${process.argv[2]}/ty-${dev}.png` });
    await p3.close();
    // return without a session on this device
    const p4 = await ctx.newPage(); await p4.addInitScript(() => localStorage.removeItem('mc_sess'));
    await p4.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    await p4.goto('http://localhost:8765/index.html?paiement=merci'); await p4.waitForTimeout(800);
    ok(await p4.$eval('#ty', e => !e.hidden && e.querySelector('.ty-go').offsetHeight === 0 && e.querySelector('.ty-re').offsetHeight === 0 && e.querySelector('.ty-wa').offsetHeight > 0), dev + ': unknown device -> WhatsApp help');
    await p4.close();
    // disabled: buttons keep the Chariow link
    const p2 = await ctx.newPage();
    await p2.route('**/api/checkout', r => r.fulfill({ status: 200, contentType: 'application/json', body: '{"enabled":false}' }));
    await p2.route(/^https?:\/\/(?!localhost)/, r => r.request().url().includes('mychariow') ? r.fulfill({ status: 200, contentType: 'text/html', body: 'CHARIOW' }) : r.abort());
    await p2.goto('http://localhost:8765/index.html'); await p2.waitForTimeout(1500);
    await p2.click('#hero-cta .js-cta'); await p2.waitForTimeout(1500);
    ok(p2.url().includes('mychariow'), dev + ': not configured -> Chariow as before');
    ok(errs.length === 0, dev + ': no script errors ' + errs.join('|'));
    await ctx.close();
  }
  await b.close();
})();
