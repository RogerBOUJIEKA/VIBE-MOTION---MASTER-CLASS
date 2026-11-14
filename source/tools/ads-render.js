// Renders every ad page at 2x on the local server origin (site font and images), saved as PNG for downscaling
const { chromium } = require('playwright');
const fs = require('fs');
const DIR = __dirname + '/';
(async () => {
  const jobs = JSON.parse(fs.readFileSync(DIR + 'jobs.json', 'utf8')).filter(j => !process.argv[2] || j[0].includes(process.argv[2]));
  const b = await chromium.launch();
  for (const [fn, W, H] of jobs) {
    const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
    await p.goto('http://localhost:8765/vercel.json');
    await p.setContent(fs.readFileSync(DIR + fn + '.html', 'utf8'), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    await p.screenshot({ path: DIR + fn + '@2x.png' });
    await p.close();
  }
  await b.close();
})();
