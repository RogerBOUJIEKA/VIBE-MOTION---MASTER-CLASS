const { chromium } = require('playwright');
const ok = (c, m, out) => out.push((c ? 'OK  ' : 'FAIL') + ' ' + m);
const under = id => `Math.round(document.getElementById('${id}').getBoundingClientRect().top - document.getElementById('hdr').getBoundingClientRect().bottom)`;
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  for (const [n, w, h, mob] of [['phone-360', 360, 740, true], ['phone-390', 390, 844, true], ['desktop', 1440, 900, false]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mob, hasTouch: mob, locale: 'fr-FR' });
    const p = await ctx.newPage(); const errs = [], out = [];
    await p.addInitScript(() => { try { sessionStorage.setItem('mc_pp', '0'); } catch (e) {} });
    p.on('pageerror', e => errs.push(e.message));
    await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1500);
    ok(await p.evaluate(() => document.documentElement.scrollWidth - innerWidth) <= 0, 'no sideways scroll', out);
    const hrefs = await p.$$eval('.js-cta', a => a.map(x => x.href));
    ok(hrefs.length >= 7 && hrefs.every(x => x.includes('prd_9wrq07d2/checkout')), hrefs.length + ' buttons -> checkout', out);
    const c1 = await p.$eval('.js-cd-hms', e => e.textContent); await p.waitForTimeout(2100); const c2 = await p.$eval('.js-cd-hms', e => e.textContent);
    ok(c1 !== c2 && /^2[34]:/.test(c2), 'countdown 24 h ticking (' + c2 + ')', out);
    const w1 = await p.$eval('.rot span.on', e => e.textContent); await p.waitForTimeout(2600);
    ok(w1 !== await p.$eval('.rot span.on', e => e.textContent), 'headline word rotates', out);
    await p.waitForTimeout(1000); ok(await p.$eval('#cbar', e => e.hidden && !e.classList.contains('on')), 'community bar paused (stays hidden)', out);
    // section jumps land just under the header (also after the pinned tunnel)
    const ids = ['methode', 'realisations', 'calcul', 'competences', 'programme', 'pour-qui', 'formateur', 'tarif', 'communaute', 'faq', 'contact'];
    const land = [];
    for (const id of ids) { await p.evaluate(id => goTo(id), id); await p.waitForTimeout(2300); land.push(await p.evaluate(under(id))); }
    ok(land.every(v => Math.abs(v - 10) <= 6), 'sections land under header ' + land.join(','), out);
    await p.evaluate(() => goTo('top')); await p.waitForTimeout(2000);
    ok(await p.evaluate(() => scrollY) < 5, 'back to top', out);
    if (mob) {
      await p.click('.burger'); await p.waitForTimeout(500); ok(await p.evaluate(() => document.body.classList.contains('menu-open')), 'menu opens', out);
      await p.click('.menu a[href="#faq"]'); await p.waitForTimeout(2400);
      ok(await p.evaluate(`!document.body.classList.contains('menu-open') && Math.abs(${under('faq')} - 10) < 8`), 'menu link -> FAQ', out);
      await p.click('.chips a[href="#tarif"]'); await p.waitForTimeout(2400);
      ok(await p.evaluate(`Math.abs(${under('tarif')} - 10) < 8`), 'quick tab -> tarif', out);
      ok(await p.$eval('.chips a[data-sec="tarif"]', a => a.classList.contains('on')), 'active quick tab', out);
    } else {
      await p.click('.nav a[href="#programme"]'); await p.waitForTimeout(2400);
      ok(await p.evaluate(`Math.abs(${under('programme')} - 10) < 8`), 'nav link -> programme', out);
      ok(await p.$eval('.nav a[data-sec="programme"]', a => a.classList.contains('on')), 'active nav item', out);
    }
    // audio pitch
    await p.evaluate(() => goTo('top')); await p.waitForTimeout(1600);
    await p.click('.js-aud'); await p.waitForTimeout(2200);
    ok(await p.evaluate(() => { const a = document.querySelector('.js-aud-el'); return !a.paused && a.currentTime > 0.5; }), 'audio plays', out);
    await p.click('.js-aud'); await p.waitForTimeout(200); ok(await p.$eval('.js-aud-el', a => a.paused), 'audio pauses', out);
    // manifesto lights up
    await p.evaluate(() => goTo('manifeste')); await p.waitForTimeout(1800);
    const lit = await p.evaluate(() => { const w = document.querySelectorAll('.js-mani .w'); return [w.length, [...w].filter(x => x.classList.contains('on')).length]; });
    ok(lit[0] > 30 && lit[1] > lit[0] * .3, 'manifesto words light up ' + lit[1] + '/' + lit[0], out);
    // method mock-ups
    await p.evaluate(() => goTo('methode')); await p.waitForTimeout(800);
    await p.evaluate(() => document.querySelector('.js-vis[data-kind="prompt"]').scrollIntoView({ block: 'center' })); await p.waitForTimeout(4500);
    ok(await p.evaluate(() => document.querySelector('.js-type').textContent.length > 60 && document.querySelectorAll('.ing span.on').length === 8), 'prompt types + 8 ingredients', out);
    await p.evaluate(() => document.querySelector('.js-vis[data-kind="tl"]').scrollIntoView({ block: 'center' })); await p.waitForTimeout(1200);
    ok(await p.$eval('.tl', e => e.classList.contains('go')), 'timeline plays', out);
    // tunnel: canvas + captions follow the scroll
    await p.evaluate(() => goTo('traversee')); await p.waitForTimeout(2500);
    const t0 = await p.$eval('.js-tn', e => e.textContent);
    await p.evaluate(() => scrollBy(0, innerHeight * 1.6)); await p.waitForTimeout(1500);
    const t1 = await p.$eval('.js-tn', e => e.textContent);
    ok(await p.evaluate(() => !!document.querySelector('#tunnel canvas')), '3D tunnel running', out);
    ok(t0 !== t1, 'tunnel captions advance ' + t0 + ' -> ' + t1, out);
    // works lightbox: mp4 and YouTube (YouTube is blocked in the test, the player must still open and close cleanly)
    await p.evaluate(() => goTo('realisations')); await p.waitForTimeout(2400);
    await p.click('.wc.wide'); await p.waitForTimeout(1200);
    ok(await p.evaluate(() => { const v = document.querySelector('#lb video'); return document.querySelector('#lb').classList.contains('on') && v && !v.paused; }), 'trailer plays in the player', out);
    await p.keyboard.press('Escape'); await p.waitForTimeout(600);
    ok(await p.evaluate(() => !document.querySelector('#lb').classList.contains('on') && !document.querySelector('#lb video')), 'player closes (Escape)', out);
    await p.click('.wc[data-yt="4abyQA1a9h8"]'); await p.waitForTimeout(800);
    ok(await p.evaluate(() => document.querySelector('#lb').classList.contains('on') && !!document.querySelector('#lb .ctrl') && document.querySelector('.js-lbt').textContent.includes('Bafoussam')), 'YouTube player opens with own controls', out);
    await p.click('#lb .cls'); await p.waitForTimeout(600);
    ok(await p.evaluate(() => !document.querySelector('#lb').classList.contains('on') && !document.querySelector('#lb .host')), 'player closes (button)', out);
    ok(await p.evaluate(() => document.querySelector('.wc[data-yt="4abyQA1a9h8"]').classList.contains('seen') && JSON.parse(localStorage.getItem('mc_seen')).includes('4abyQA1a9h8')), '"Nouveau" badge removed once seen', out);
    // comparator
    await p.evaluate(() => goTo('calcul')); await p.waitForTimeout(800);
    await p.evaluate(() => document.getElementById('cmp').scrollIntoView({ block: 'center' })); await p.waitForTimeout(2600);
    ok(await p.$eval('#cmp', e => e.classList.contains('ai')), 'comparator switches to Vibe Motion by itself', out);
    await p.click('#cmp .sw button[data-m="c"]'); await p.waitForTimeout(300);
    ok(await p.evaluate(() => { const b = document.querySelector('#cmp .mx b'); return !document.getElementById('cmp').classList.contains('ai') && getComputedStyle(b.querySelector('.a')).display === 'none' && getComputedStyle(b.querySelector('.c')).display !== 'none'; }), 'comparator shows one value at a time', out);
    // calculator
    await p.evaluate(() => document.getElementById('roi').scrollIntoView({ block: 'center' })); await p.waitForTimeout(800);
    await p.click('.js-seg button[data-p="150000"]');
    await p.evaluate(() => { const r = document.querySelector('.js-rr'); r.value = 10; r.dispatchEvent(new Event('input')); }); await p.waitForTimeout(1000);
    ok(await p.evaluate(() => document.querySelector('.js-rv').textContent.replace(/\D/g, '') === '1500000' && document.querySelector('.js-rx').textContent === '125×'), 'earnings calculator', out);
    // chapters, modules, profiles, FAQ
    await p.evaluate(() => goTo('programme')); await p.waitForTimeout(2300);
    await p.click('.ctab[data-ch="2"]'); await p.waitForTimeout(300);
    ok(await p.evaluate(() => document.querySelector('.cpan[data-ch="2"]').classList.contains('on') && !document.querySelector('.cpan[data-ch="0"]').classList.contains('on')), 'chapter tabs', out);
    await p.evaluate(() => { const d = document.querySelectorAll('.cpan.on details'); d[0].querySelector('summary').click(); d[1].querySelector('summary').click(); }); await p.waitForTimeout(300);
    ok(await p.$$eval('.cpan.on details[open]', e => e.length === 1), 'modules: one open', out);
    await p.evaluate(() => goTo('pour-qui')); await p.waitForTimeout(2300);
    await p.click('.who .pills button[data-w="3"]'); await p.waitForTimeout(300);
    ok(await p.evaluate(() => document.querySelector('.wpan[data-w="3"]').classList.contains('on') && document.querySelectorAll('.wpan.on').length === 1), 'profiles', out);
    await p.evaluate(() => document.querySelectorAll('.faq details')[3].querySelector('summary').click()); await p.waitForTimeout(300);
    ok(await p.$$eval('.faq details[open]', e => e.length === 1), 'FAQ: one open', out);
    // language + theme
    await p.click('#lang-en'); await p.waitForTimeout(400);
    ok(await p.evaluate(() => document.documentElement.lang === 'en' && document.querySelector('[data-i18n="cta_hero"]').textContent === 'Join the course' && document.querySelector('.js-tw span').textContent === 'Advertising spots'), 'English', out);
    const fr = await p.evaluate(() => [...document.querySelectorAll('[data-i18n]')].filter(n => /\b(vous|votre|formation|Je |les |des |pour )\b/.test(n.textContent) && !/Vibe Motion|BOUJIEKA|LE DIGITAL POUR TOUS|Bafoussam|Croisade|Clôture|Invitation|Bus gratuits/.test(n.textContent)).map(n => n.dataset.i18n));
    ok(fr.length === 0, 'no French left in English mode ' + fr.slice(0, 6).join(','), out);
    ok(await p.evaluate(() => document.querySelectorAll('.js-mani .w').length > 20), 'manifesto re-split in English', out);
    await p.click('#lang-fr'); await p.waitForTimeout(300);
    ok(await p.evaluate(() => document.querySelector('[data-i18n="cta_hero"]').textContent === 'Rejoindre la formation'), 'French', out);
    await p.click('#thm'); await p.waitForTimeout(150); ok(await p.evaluate(() => document.documentElement.getAttribute('data-theme') === 'dark'), 'dark mode', out);
    await p.click('#thm'); await p.waitForTimeout(150); ok(await p.evaluate(() => !document.documentElement.getAttribute('data-theme')), 'light mode', out);
    ok(await p.$$eval('#fx-cur option', o => o.length) > 5, 'currency list', out);
    if (mob) {
      await p.evaluate(() => goTo('competences')); await p.waitForTimeout(2000);
      ok(await p.$eval('#mbar', e => e.classList.contains('show')), 'bottom booking bar shows', out);
      await p.evaluate(() => document.getElementById('pcard').scrollIntoView({ block: 'center' })); await p.waitForTimeout(500);
      ok(await p.$eval('#mbar', e => !e.classList.contains('show')), 'bottom bar hides on the price card', out);
    }
    // scroll the whole page: every block revealed
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y <= H + 600; y += 450) { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(70); }
    await p.waitForTimeout(1500);
    ok(await p.evaluate(() => [...document.querySelectorAll('.rv')].filter(e => getComputedStyle(e).opacity < 0.9).length) === 0, 'every block revealed', out);
    ok(errs.length === 0, 'no script errors ' + errs.join('|'), out);
    console.log('== ' + n + '\n' + out.join('\n')); await ctx.close();
  }
  await b.close();
})();
