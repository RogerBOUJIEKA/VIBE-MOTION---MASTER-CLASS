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
const ok = (c, m, out) => out.push((c ? 'OK  ' : 'FAIL') + ' ' + m);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  const p = await ctx.newPage(); const errs = [], out = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.route('https://www.youtube.com/iframe_api', r => r.fulfill({ status: 200, contentType: 'text/javascript', body: FAKE }));
  await p.route(/^https?:\/\/(?!localhost)(?!www\.youtube\.com\/iframe_api)/, r => r.abort());
  await p.addInitScript(() => { localStorage.setItem('mc_lang', 'fr'); sessionStorage.setItem('mc_toast', '0'); sessionStorage.setItem('mc_pp', '0'); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(800);
  const vp = '#vp';
  await p.waitForTimeout(3500);
  ok(await p.$eval(vp, e => e.classList.contains('preview') && e.classList.contains('started')), 'phone: muted preview starts by itself in the hero', out);
  ok(await p.evaluate(() => window.__fake && window.__fake.muted), 'preview is muted', out);
  await p.screenshot({ path: `${OUT}/vpm-1-preview.png` });
  await p.tap('#vp .vp-big'); await p.waitForTimeout(1600);
  const rr = await p.evaluate(() => { const r = document.querySelector('#vp').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)]; });
  ok(rr[0] >= 50 && rr[1] <= 844, 'player fully in view after the tap (' + rr.join('-') + ')', out);
  ok(await p.$eval(vp, e => e.classList.contains('sound') && !e.classList.contains('preview')), 'tap switches to sound mode', out);
  ok(await p.evaluate(() => !window.__fake.muted && window.__fake.t < 15), 'sound on, restarted from the beginning', out);
  await p.tap('#vp .vp-scr', { position: { x: 150, y: 60 } }).catch(() => {}); await p.waitForTimeout(500);
  const shown = await p.$eval('#vp .vp-ctrl', e => getComputedStyle(e).opacity > .9);
  ok(shown || await p.$eval(vp, e => e.classList.contains('paused')), 'controls visible after a tap', out);
  if (!await p.$eval(vp, e => e.classList.contains('paused'))) { await p.tap('#vp .vp-scr', { position: { x: 150, y: 60 } }); await p.waitForTimeout(400); }
  await p.screenshot({ path: `${OUT}/vpm-2-controls.png` });
  const cw = await p.evaluate(() => { const row = document.querySelector('#vp .vp-row'); const kids = [...row.children].filter(k => getComputedStyle(k).display !== 'none'); const r = row.getBoundingClientRect(); return { fits: kids.every(k => { const b = k.getBoundingClientRect(); return b.left >= r.left - 1 && b.right <= r.right + 1; }), n: kids.length, sw: row.scrollWidth, cw: row.clientWidth }; });
  ok(cw.fits && cw.sw <= cw.cw + 1, 'control row fits in one line (' + cw.n + ' controls, ' + cw.sw + '/' + cw.cw + ' px)', out);
  const pg = await p.$('#vp .vp-pg'); const r = await pg.boundingBox();
  await p.touchscreen.tap(r.x + r.width * .5, r.y + r.height / 2); await p.waitForTimeout(400);
  const tt = await p.evaluate(() => window.__fake.t);
  ok(tt > 40 && tt < 62, 'tap on the progress bar seeks (' + tt.toFixed(1) + ' s of 95)', out);
  await p.tap('#vp .vp-sp'); await p.waitForTimeout(200);
  ok(await p.evaluate(() => window.__fake.rate === 1.25), 'speed button works by touch', out);
  await p.tap('#vp .vp-pp'); await p.waitForTimeout(300);
  ok(await p.$eval(vp, e => e.classList.contains('paused')), 'pause button works by touch', out);
  const t0 = await p.evaluate(() => window.__fake.t);
  await p.tap('#vp .vp-rw'); await p.waitForTimeout(150); const t1 = await p.evaluate(() => window.__fake.t);
  ok(Math.abs(t0 - 10 - t1) < 1.5, '−10 s', out);
  await p.tap('#vp .vp-fw'); await p.waitForTimeout(150); const t2 = await p.evaluate(() => window.__fake.t);
  ok(Math.abs(t2 - t1 - 10) < 1.5, '+10 s', out);
  await p.screenshot({ path: `${OUT}/vpm-3-paused.png` });
  await p.tap('#vp .vp-pp'); await p.waitForTimeout(300);
  const r2 = await (await p.$('#vp .vp-pg')).boundingBox(); await p.touchscreen.tap(r2.x + r2.width * .995, r2.y + r2.height / 2); await p.waitForTimeout(2500);
  ok(await p.$eval(vp, e => e.classList.contains('ended')), 'end screen at the end', out);
  const ef = await p.evaluate(() => { const end = document.querySelector('#vp .vp-end').getBoundingClientRect(); const kids = [...document.querySelectorAll('#vp .vp-end h3, #vp .vp-end p, #vp .vp-end .btn')]; return kids.every(k => { const b = k.getBoundingClientRect(); return b.top >= end.top && b.bottom <= end.bottom && b.left >= end.left && b.right <= end.right; }); });
  ok(ef, 'end screen content fits inside the player', out);
  await p.screenshot({ path: `${OUT}/vpm-4-end.png` });
  await p.tap('#vp .vp-again'); await p.waitForTimeout(400);
  ok(await p.$eval(vp, e => !e.classList.contains('ended') && e.classList.contains('playing')), 'Revoir restarts the video', out);
  ok(errs.length === 0, 'no script errors ' + errs.join('|'), out);
  console.log(out.join('\n'));
  await b.close();
})();
