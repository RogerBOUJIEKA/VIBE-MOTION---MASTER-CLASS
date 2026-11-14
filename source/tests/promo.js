// Promo check: prices, promo card timing/closing, screenshots
const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'OK  ' : 'FAIL') + ' ' + m);
const OUT = process.argv[2];
(async () => {
  const b = await chromium.launch();
  for (const [dev, w, h, mob] of [['phone', 390, 844, true], ['desktop', 1440, 900, false]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mob, hasTouch: mob, deviceScaleFactor: 2 });
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    await p.addInitScript(() => { localStorage.setItem('mc_lang', 'fr'); sessionStorage.setItem('mc_cbar', '0'); sessionStorage.setItem('mc_toast', '0'); });
    await p.clock.install();
    await p.goto('http://localhost:8765/index.html'); await p.clock.runFor(1500);
    const txt = await p.evaluate(() => document.body.innerText);
    ok(!/35\s?000|−57|−63|15\s000\sFCFA/.test(txt), dev + ': no old 35 000 / −57 % left');
    ok(/5\s?500/.test(txt) && /−78/.test(txt) && /25\s?000/.test(txt), dev + ': 5 500 FCFA and −63 % shown');
    await p.screenshot({ path: `${OUT}/promo-top-${dev}.png` });
    ok(await p.$eval('#pp', e => e.hidden), dev + ': promo card hidden at start');
    await p.clock.runFor(13000); await p.waitForTimeout(500);
    ok(await p.$eval('#pp', e => !e.hidden && e.classList.contains('on')), dev + ': promo card appears after 12 s');
    ok(await p.$eval('#pp .js-cd-hms', e => /^\d\d:\d\d:\d\d$/.test(e.textContent) && e.textContent !== '24:00:00'), dev + ': countdown running in the card');
    await p.screenshot({ path: `${OUT}/promo-card-${dev}.png` });
    await p.click('#pp .pp-x'); await p.clock.runFor(500);
    ok(await p.$eval('#pp', e => e.hidden), dev + ': cross closes it');
    await p.clock.runFor(30000);
    ok(await p.$eval('#pp', e => e.hidden), dev + ': stays closed 30 s later');
    await p.clock.runFor(11000); await p.waitForTimeout(300);
    ok(await p.$eval('#pp', e => !e.hidden), dev + ': comes back 40 s after closing');
    await p.click('#pp .pp-later'); await p.clock.runFor(500);
    ok(await p.$eval('#pp', e => e.hidden), dev + ': "Continuer la lecture" closes it');
    await p.evaluate(() => document.querySelector('#tarif').scrollIntoView()); await p.clock.runFor(1500);
    await p.screenshot({ path: `${OUT}/promo-tarif-${dev}.png` });
    ok(errs.length === 0, dev + ': no script errors ' + errs.join('|'));
    await ctx.close();
  }
  await b.close();
})();
