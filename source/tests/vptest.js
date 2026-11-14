// Tests the hero presentation player against a simulated YouTube iframe API (YouTube is not reachable here).
const { chromium } = require('playwright');
const OUT = process.argv[2];
const FAKE = `
window.YT = { Player: function (el, opts) {
  const self = this; let st = -1, t = 0, d = 95, muted = !!opts.playerVars.mute, vol = 100, rate = 1, last = performance.now();
  window.__fake = { get muted() { return muted; }, get vol() { return vol; }, get rate() { return rate; }, get t() { return t; } };
  const ifr = document.createElement('iframe');
  ifr.srcdoc = '<body style="margin:0;height:100vh;background:linear-gradient(135deg,#1b2a4a,#5b1020);display:grid;place-items:center;color:#fff;font:600 42px sans-serif">VIDEO</body>';
  el.replaceWith(ifr);
  const emit = s => { st = s; opts.events.onStateChange && opts.events.onStateChange({ data: s, target: self }); };
  setInterval(() => { const now = performance.now(); if (st === 1) { t += (now - last) / 1000 * rate * 3; if (t >= d) { t = d; emit(0); } } last = now; }, 100);
  Object.assign(self, { playVideo() { if (st !== 1) emit(1); }, pauseVideo() { if (st === 1) emit(2); }, seekTo(x) { t = Math.max(0, Math.min(d, x)); },
    getCurrentTime() { return t; }, getDuration() { return d; }, getPlayerState() { return st; }, mute() { muted = true; }, unMute() { muted = false; },
    isMuted() { return muted; }, setVolume(v) { vol = v; }, getVolume() { return vol; }, setPlaybackRate(r) { rate = r; }, getVideoLoadedFraction() { return Math.min(1, (t + 25) / d); }, destroy() { ifr.remove(); } });
  setTimeout(() => opts.events.onReady && opts.events.onReady({ target: self }), 250);
} };
setTimeout(() => window.onYouTubeIframeAPIReady && window.onYouTubeIframeAPIReady(), 50);`;
const hov = async (p, sel) => { await p.hover(sel, { force: true }); await p.waitForTimeout(200); };
const ok = (c, m, out) => out.push((c ? 'OK  ' : 'FAIL') + ' ' + m);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage(); const errs = [], out = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.route('https://www.youtube.com/iframe_api', r => r.fulfill({ status: 200, contentType: 'text/javascript', body: FAKE }));
  await p.route(/^https?:\/\/(?!localhost)(?!www\.youtube\.com\/iframe_api)/, r => r.abort());
  await p.addInitScript(() => { localStorage.setItem('mc_lang', 'fr'); sessionStorage.setItem('mc_cbar', '0'); sessionStorage.setItem('mc_toast', '0'); sessionStorage.setItem('mc_pp', '0'); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(800);
  await p.evaluate(() => scrollTo(0, 560)); await p.waitForTimeout(3500);
  const vp = '#vp';
  ok(await p.$eval(vp, e => e.classList.contains('preview') && e.classList.contains('started')), 'muted preview starts by itself', out);
  ok(await p.evaluate(() => window.__fake && window.__fake.muted), 'preview is muted', out);
  await p.screenshot({ path: `${OUT}/vp-1-preview.png` });
  await p.click('#vp .vp-big'); await p.waitForTimeout(1600);
  const rr = await p.evaluate(() => { const r = document.querySelector('#vp').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)]; });
  ok(rr[0] >= 60 && rr[1] <= 900, 'player scrolls fully into view (' + rr.join('-') + ')', out);
  ok(await p.$eval(vp, e => e.classList.contains('sound') && !e.classList.contains('preview')), 'big button switches to sound mode', out);
  ok(await p.evaluate(() => !window.__fake.muted && window.__fake.t < 15), 'sound on, restarted from the beginning', out);
  await p.mouse.move(700, 500); await p.waitForTimeout(500);
  ok(await p.$eval('#vp .vp-ctrl', e => getComputedStyle(e).opacity > .9), 'controls appear on hover', out);
  await p.screenshot({ path: `${OUT}/vp-2-playing.png` });
  // seek to half
  const pg = await p.$('#vp .vp-pg'); const r = await pg.boundingBox();
  await p.mouse.move(r.x + r.width * .5, r.y + r.height / 2); await p.waitForTimeout(300);
  ok(await p.$eval('#vp .vp-tip', e => getComputedStyle(e).opacity > .9 && /^\d+:\d\d$/.test(e.textContent)), 'time tooltip on the progress bar', out);
  await p.mouse.down(); await p.mouse.move(r.x + r.width * .52, r.y + r.height / 2); await p.mouse.up(); await p.waitForTimeout(300);
  const tt = await p.evaluate(() => window.__fake.t);
  ok(tt > 45 && tt < 60, 'seek by click/drag (' + tt.toFixed(1) + ' s of 95)', out);
  // volume
  const mu = await p.$('#vp .vp-mu'); const mr = await mu.boundingBox();
  await p.mouse.move(mr.x + mr.width / 2, mr.y + mr.height / 2); await p.waitForTimeout(600);
  const vs = await p.$('#vp .vp-vs'); const vr = await vs.boundingBox();
  ok(vr.width > 60, 'volume bar opens on hover (' + Math.round(vr.width) + ' px)', out);
  await p.mouse.click(vr.x + vr.width * .3, vr.y + vr.height / 2); await p.waitForTimeout(300);
  const v = await p.evaluate(() => window.__fake.vol);
  ok(v > 20 && v < 40, 'volume set by the bar (' + v + ')', out);
  await p.screenshot({ path: `${OUT}/vp-3-volume.png` });
  await hov(p, '#vp .vp-mu'); await p.click('#vp .vp-mu'); await p.waitForTimeout(200); ok(await p.evaluate(() => window.__fake.muted), 'mute button', out);
  await hov(p, '#vp .vp-mu'); await p.click('#vp .vp-mu'); await p.waitForTimeout(200); ok(await p.evaluate(() => !window.__fake.muted), 'unmute button', out);
  // speed, ±10 s, pause
  await hov(p, '#vp .vp-sp'); await p.click('#vp .vp-sp'); await p.waitForTimeout(200);
  ok(await p.evaluate(() => window.__fake.rate === 1.25 && document.querySelector('#vp .vp-sp').textContent === '1,25×'), 'speed 1,25×', out);
  await hov(p, '#vp .vp-sp'); await p.click('#vp .vp-sp'); await hov(p, '#vp .vp-sp'); await p.click('#vp .vp-sp'); await hov(p, '#vp .vp-sp'); await p.click('#vp .vp-sp'); await p.waitForTimeout(100);
  ok(await p.evaluate(() => window.__fake.rate === 1), 'speed cycles back to 1×', out);
  await hov(p, '#vp .vp-pp'); await p.click('#vp .vp-pp'); await p.waitForTimeout(300);
  ok(await p.$eval(vp, e => e.classList.contains('paused')), 'pause button', out);
  const t0 = await p.evaluate(() => window.__fake.t);
  await hov(p, '#vp .vp-rw'); await p.click('#vp .vp-rw'); await p.waitForTimeout(150); const t1 = await p.evaluate(() => window.__fake.t);
  ok(Math.abs(t0 - 10 - t1) < 1.5, '−10 s', out);
  await hov(p, '#vp .vp-fw'); await p.click('#vp .vp-fw'); await p.waitForTimeout(150); const t2 = await p.evaluate(() => window.__fake.t);
  ok(Math.abs(t2 - t1 - 10) < 1.5, '+10 s', out);
  await p.screenshot({ path: `${OUT}/vp-4-paused.png` });
  ok(await p.evaluate(() => { const s = document.querySelector('#vp .vp-scr').getBoundingClientRect(), c = document.querySelector('#vp .vp-ctrl').getBoundingClientRect(); return Math.abs(s.bottom - c.bottom) < 2; }), 'controls stay at the bottom of the screen', out);
  // keyboard
  await p.focus('#vp'); await p.keyboard.press('k'); await p.waitForTimeout(250);
  ok(await p.$eval(vp, e => e.classList.contains('playing')), 'keyboard: k plays', out);
  // end screen
  await p.evaluate(() => { const r = document.querySelector('#vp .vp-pg').getBoundingClientRect(); });
  await hov(p, '#vp .vp-pg'); const r2 = await (await p.$('#vp .vp-pg')).boundingBox(); await p.mouse.click(r2.x + r2.width * .995, r2.y + r2.height / 2); await p.waitForTimeout(2500);
  ok(await p.$eval(vp, e => e.classList.contains('ended')), 'end screen at the end', out);
  ok(await p.$eval('#vp .vp-end .js-cta', a => a.href.includes('prd_9wrq07d2/checkout')), 'end screen button -> checkout', out);
  await p.screenshot({ path: `${OUT}/vp-5-end.png` });
  await p.click('#vp .vp-again'); await p.waitForTimeout(400);
  ok(await p.$eval(vp, e => !e.classList.contains('ended') && e.classList.contains('playing')), 'Revoir restarts the video', out);
  ok(await p.$eval('#vp .vp-fs', e => !e.hidden), 'full-screen button available', out);
  // the course audio pauses the video, and the reverse
  await p.evaluate(() => { const a = document.querySelector('.js-aud-el'); a.dispatchEvent(new Event('play')); }); await p.waitForTimeout(300);
  ok(await p.$eval(vp, e => !e.classList.contains('playing')), 'audio pitch pauses the video', out);
  await p.click('#lang-en'); await p.waitForTimeout(300);
  ok(await p.evaluate(() => document.querySelector('#vp .vp-bar3').textContent.includes('Course presentation')), 'English labels', out);
  ok(errs.length === 0, 'no script errors ' + errs.join('|'), out);
  console.log(out.join('\n'));
  await b.close();
})();
