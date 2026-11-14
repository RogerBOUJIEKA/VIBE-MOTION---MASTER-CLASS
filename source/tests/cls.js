// Which elements move during a scroll through the page (layout shifts), phone size
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const mob = process.argv[2] !== 'd';
  const ctx = await b.newContext(mob ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
  await p.addInitScript(() => {
    window.__ls = [];
    new PerformanceObserver(l => l.getEntries().forEach(e => {
      if (e.hadRecentInput || e.value < 0.005) return;
      const src = (e.sources || []).map(s => { const n = s.node; if (!n || !n.tagName) return '?'; return n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + (n.className && typeof n.className === 'string' ? '.' + n.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ' ' + Math.round(s.previousRect.y) + '->' + Math.round(s.currentRect.y); });
      __ls.push([Math.round(scrollY), +e.value.toFixed(3), src.join(' | ')]);
    })).observe({ type: 'layout-shift', buffered: true });
  });
  await p.goto('http://localhost:8765/index.html', { waitUntil: 'load' }); await p.waitForTimeout(2500);
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 120) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(30); }
  await p.waitForTimeout(500);
  const ls = await p.evaluate(() => __ls);
  console.log('total', ls.reduce((a, x) => a + x[1], 0).toFixed(3), 'entries', ls.length);
  ls.slice(0, 25).forEach(x => console.log(x.join('  ')));
  await b.close();
})();
