const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2.6, isMobile: true, hasTouch: true });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
  const cdp = await ctx.newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  await p.addInitScript(() => {
    window.__lt = []; window.__cls = 0;
    new PerformanceObserver(l => l.getEntries().forEach(e => __lt.push(e.duration))).observe({ type: 'longtask', buffered: true });
    new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) __cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
  });
  const t0 = Date.now(); await p.goto('http://localhost:8765/index.html', { waitUntil: 'load' }); const loadMs = Date.now() - t0;
  await p.waitForTimeout(1500);
  const nav = await p.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; const fcp = performance.getEntriesByName('first-contentful-paint')[0]; return { dcl: Math.round(n.domContentLoadedEventEnd), fcp: fcp && Math.round(fcp.startTime) }; });
  const ltLoad = await p.evaluate(() => __lt.slice());
  await p.evaluate(() => { __lt = []; window.__f = []; let last = performance.now(); (function f(t) { __f.push(t - last); last = t; window.__raf = requestAnimationFrame(f); })(performance.now()); });
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += 120) { await p.mouse.wheel(0, 120); await p.waitForTimeout(16); }
  await p.waitForTimeout(500);
  const r = await p.evaluate(() => { cancelAnimationFrame(__raf); const f = __f.slice(2); const slow = f.filter(x => x > 34).length; return { frames: f.length, avg: +(f.reduce((a, b) => a + b, 0) / f.length).toFixed(1), slow, worst: Math.round(Math.max(...f)), lt: __lt.length, ltMax: Math.round(Math.max(0, ...__lt)), cls: +__cls.toFixed(3) }; });
  // tap response: time from click to tab panel change
  await p.evaluate(() => goTo("faq"));
  const tap = await p.evaluate(async () => { const t = document.getElementById('lang-en'); const s = performance.now(); t.click(); await new Promise(r => requestAnimationFrame(() => r())); return Math.round(performance.now() - s); });
  console.log(JSON.stringify({ loadMs, ...nav, longTasksOnLoad: ltLoad.length, longestOnLoad: Math.round(Math.max(0, ...ltLoad)), scroll: r, tapToPaintMs: tap, errs }));
  await b.close();
})();
