const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'OK  ' : 'FAIL') + ' ' + m);
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true })).newPage();
  await p.route(/^https?:\/\/(?!localhost)/, r => r.abort());
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(6000);
  ok(await p.$eval('#cbar', e => e.hidden && !e.classList.contains('on')), 'top community bar stays hidden after 6 s');
  ok(await p.$$eval('a.js-lead', a => a.length >= 1 && a.every(x => x.href.includes('chat.whatsapp.com'))), 'free community links still in the page (' + (await p.$$eval('a.js-lead', a => a.length)) + ')');
  await b.close();
})();
