// Renders og.html at 1200 x 630 on the local server origin (so the site's font and images load)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const html = fs.readFileSync(__dirname + '/og.html', 'utf8');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.goto('http://localhost:8765/vercel.json');
  await p.setContent(html, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: process.argv[2], type: process.argv[2].endsWith('.jpg') ? 'jpeg' : 'png', quality: process.argv[2].endsWith('.jpg') ? 90 : undefined });
  await b.close();
})();
