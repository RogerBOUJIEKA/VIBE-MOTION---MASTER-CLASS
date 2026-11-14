// New phone hero: screenshots at several phone widths + desktop, overflow check, every rotating word fits
const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'OK  ' : 'FAIL') + ' ' + m);
const OUT = process.argv[2];
(async () => {
  const b = await chromium.launch();
  for (const [name, w, h, mob] of [['m360', 360, 740, true], ['m390', 390, 844, true], ['m430', 430, 932, true], ['d1440', 1440, 900, false]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mob, hasTouch: mob, deviceScaleFactor: 2 });
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    await p.addInitScript(() => { localStorage.setItem('mc_lang', 'fr'); sessionStorage.setItem('mc_toast', '0'); sessionStorage.setItem('mc_pp', '0'); });
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
    const m = await p.evaluate(() => {
      const r = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return { top: Math.round(b.top + scrollY), h: Math.round(b.height), w: Math.round(b.width), left: Math.round(b.left) }; };
      const words = [...document.querySelectorAll('.rot span')].map(s => { const b = s.getBoundingClientRect(); return { t: s.textContent, w: Math.round(s.scrollWidth) }; });
      return { scrollW: document.documentElement.scrollWidth, vw: innerWidth, h1: r('.h1'), vp: r('#vp'), acts: r('#hero-cta'), offer: r('.offer-mini'), photo: !!document.querySelector('.subject') && getComputedStyle(document.querySelector('.subject')).display, words, gridW: r('.hgrid') };
    });
    ok(m.scrollW <= m.vw, `${name}: no horizontal scroll (${m.scrollW} <= ${m.vw})`);
    ok(m.photo === 'none', `${name}: photo hidden in the hero`);
    ok(m.words.every(x => x.w <= m.gridW.w - 4), `${name}: every rotating word fits (${Math.max(...m.words.map(x => x.w))} <= ${m.gridW.w})`);
    console.log(`     ${name}: h1 top ${m.h1.top}, player top ${m.vp.top} (${m.vp.w}x${m.vp.h}), cta top ${m.acts.top}, offer top ${m.offer.top}`);
    ok(errs.length === 0, `${name}: no script errors ${errs.join('|')}`);
    await p.screenshot({ path: `${OUT}/hero-${name}.png` });
    await p.screenshot({ path: `${OUT}/hero-${name}-full.png`, fullPage: false, clip: { x: 0, y: 0, width: w, height: Math.min(m.offer.top + m.offer.h + 300, 2200) }, });
    await ctx.close();
  }
  await b.close();
})();
