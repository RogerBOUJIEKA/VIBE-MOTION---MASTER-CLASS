// Readability audit: every visible text against the colour behind it (WCAG contrast), light and dark themes,
// including pressed / selected states. Usage: node contrast.js [min=3]
const { chromium } = require('playwright');
const MIN = +(process.argv[2] || 3);
(async () => {
  const b = await chromium.launch();
  for (const theme of ['light', 'dark']) {
    for (const [vw, vh, mob] of [[1440, 900, false], [390, 844, true]]) {
      const ctx = await b.newContext({ viewport: { width: vw, height: vh }, isMobile: mob, hasTouch: mob, reducedMotion: 'reduce' });
      const p = await ctx.newPage();
      await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
      await p.addInitScript(t => { localStorage.setItem('mc_lang', 'fr'); localStorage.setItem('mc_theme', t); sessionStorage.setItem('mc_cbar', '0'); sessionStorage.setItem('mc_toast', '0'); }, theme);
      await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1200);
      const states = [
        ['default', async () => {}],
        ['classic pressed', async () => { await p.evaluate(() => document.querySelector('#cmp .sw button[data-m="c"]').click()); }],
        ['ai pressed', async () => { await p.evaluate(() => document.querySelector('#cmp .sw button[data-m="a"]').click()); }],
        ['chapter 3 + modules open', async () => { await p.evaluate(() => { document.querySelector('.ctab[data-ch="2"]').click(); document.querySelectorAll('.cpan.on details').forEach(d => d.open = true); }); }],
        ['chapter 1 open', async () => { await p.evaluate(() => { document.querySelector('.ctab[data-ch="0"]').click(); document.querySelectorAll('.cpan.on details').forEach(d => d.open = true); }); }],
        ['chapter 4 open', async () => { await p.evaluate(() => { document.querySelector('.ctab[data-ch="3"]').click(); document.querySelectorAll('.cpan.on details').forEach(d => d.open = true); }); }],
        ['profile 4', async () => { await p.evaluate(() => document.querySelector('.who .pills button[data-w="4"]').click()); }],
        ['faq all open', async () => { await p.evaluate(() => document.querySelectorAll('.faq details').forEach(d => d.open = true)); }],
        ['menu open', async () => { await p.evaluate(() => document.body.classList.add('menu-open')); }],
      ];
      const seen = new Map();
      for (const [name, act] of states) {
        await act(); await p.waitForTimeout(250);
        const bad = await p.evaluate(MIN => {
          const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
          const lum = c => { const f = x => { x /= 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
          const over = (top, bot) => ({ r: top.r * top.a + bot.r * (1 - top.a), g: top.g * top.a + bot.g * (1 - top.a), b: top.b * top.a + bot.b * (1 - top.a), a: 1 });
          const out = [];
          const els = [...document.querySelectorAll('body *')].filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 0));
          for (const el of els) {
            const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
            const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
            let op = 1, hidden = false; for (let n = el; n && n !== document; n = n.parentElement) { const s = getComputedStyle(n); op *= +s.opacity; if (s.display === 'none' || s.visibility === 'hidden') hidden = true; }
            if (hidden || op < .5) continue;
            if (el.closest('.sr, [aria-hidden="true"]:not(.badge):not(.loop), .rot span:not(.on), .js-tw span:not(.on), noscript, .lb:not(.on), .menu')) { if (!document.body.classList.contains('menu-open') || !el.closest('.menu')) continue; }
            if (/transparent|rgba\(0, 0, 0, 0\)/.test(cs.color) && cs.webkitTextFillColor && /rgba\(0, 0, 0, 0\)/.test(cs.webkitTextFillColor)) continue;
            let fg = parse(cs.webkitTextFillColor && !/currentcolor/i.test(cs.webkitTextFillColor) ? cs.webkitTextFillColor : cs.color); if (!fg || fg.a === 0) continue;
            // walk up for the background
            const layers = []; let grad = '';
            for (let n = el; n; n = n.parentElement) {
              const s = getComputedStyle(n);
              if (s.backgroundImage && s.backgroundImage !== 'none' && !grad) grad = (n.className && typeof n.className === 'string' ? n.className : n.tagName) + '';
              const c = parse(s.backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= .99) break; }
            }
            let bg = { r: 255, g: 255, b: 255, a: 1 };
            for (let i = layers.length - 1; i >= 0; i--) bg = over(layers[i], bg);
            if (fg.a < 1) fg = over(fg, bg);
            const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
            if (ratio < MIN && !grad) {
              const path = (el.closest('[id]') || {}).id || '';
              const cls = (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') ;
              out.push([ratio.toFixed(2), '#' + path + ' ' + el.tagName.toLowerCase() + cls, el.textContent.trim().slice(0, 40), cs.color, 'bg rgb(' + [bg.r, bg.g, bg.b].map(Math.round).join(',') + ')']);
            }
          }
          return out;
        }, MIN);
        bad.forEach(x => { const k = x[1] + '|' + x[2]; if (!seen.has(k)) seen.set(k, [name, ...x]); });
      }
      console.log(`== ${theme} ${mob ? 'phone' : 'desktop'}: ${seen.size} texts under ${MIN}:1`);
      [...seen.values()].slice(0, 60).forEach(x => console.log('  ' + x.join('  |  ')));
      await ctx.close();
    }
  }
  await b.close();
})();
