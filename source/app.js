const EN = /*EN*/{};
const ROT = { fr: /*ROTFR*/[], en: /*ROTEN*/[] };
const TUN = { fr: /*TUNFR*/[], en: /*TUNEN*/[] };
const IC = /*IC*/{};
const CHECKOUT_URL = /*CTA*/"";
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
const lang = () => document.documentElement.lang === 'en' ? 'en' : 'fr';
const hdr = $('#hdr');
let lenis = null;

/* ---------- booking buttons ---------- */
$$('.js-cta').forEach(a => { a.href = CHECKOUT_URL; });

/* ---------- header height, used by the stacking cards, the tunnel and the jumps ---------- */
const hb = () => hdr.offsetHeight;
function setHb() { document.documentElement.style.setProperty('--hb', hb() + 'px'); }
setHb(); addEventListener('resize', setHb);

/* ---------- language (French is read from the page, English is injected) ---------- */
const FR = {}; const nodes = $$('[data-i18n]');
nodes.forEach(n => { const k = n.dataset.i18n; if (!(k in FR)) FR[k] = n.innerHTML; });
function setLang(l) {
  nodes.forEach(n => { const v = (l === 'en' ? EN : FR)[n.dataset.i18n]; if (v != null) n.innerHTML = v; });
  document.documentElement.lang = l;
  $('#lang-fr').setAttribute('aria-pressed', l === 'fr'); $('#lang-en').setAttribute('aria-pressed', l === 'en');
  try { localStorage.setItem('mc_lang', l); } catch (e) {}
  $$('.rot span').forEach((s, i) => { s.textContent = ROT[l][i]; });
  const on = $('.rot span.on'), sr = $('.js-rot-sr'); if (sr && on) sr.textContent = on.textContent;
  $$('.js-tw span').forEach((s, i) => { s.textContent = TUN[l][i]; });
  $$('.js-type').forEach(el => { if (el.dataset.done) el.textContent = el.dataset[l]; });
  if (window.maniSplit) maniSplit();
  if (window.fxRender) fxRender(); if (window.roiCalc) roiCalc();
  if (window.ScrollTrigger) ScrollTrigger.refresh();
}
$('#lang-fr').addEventListener('click', () => setLang('fr'));
$('#lang-en').addEventListener('click', () => setLang('en'));

/* ---------- day / night ---------- */
(function () {
  const root = document.documentElement, meta = $('meta[name="theme-color"]');
  const apply = t => { if (t === 'dark') root.setAttribute('data-theme', 'dark'); else root.removeAttribute('data-theme'); if (meta) meta.content = t === 'dark' ? '#0b0b0e' : '#f6f4f1'; };
  apply(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');
  $('#thm').addEventListener('click', () => { const t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; apply(t); try { localStorage.setItem('mc_theme', t); } catch (e) {} });
})();

/* ---------- jumps to sections, landing just under the header ---------- */
function goTo(id) {
  const el = document.getElementById(id); if (!el) return;
  closeMenu();
  const target = () => id === 'top' ? 0 : Math.max(0, el.getBoundingClientRect().top + scrollY - (hb() + 10));
  const fix = () => { const d = el.getBoundingClientRect().top - (hb() + 10); if (Math.abs(d) > 4 && scrollY + d >= 0) { if (lenis) lenis.scrollTo(target(), { immediate: true }); else scrollTo({ top: target(), behavior: 'instant' }); } };
  if (lenis) { lenis.scrollTo(target(), { duration: 1.1, onComplete: () => setTimeout(fix, 30) }); return; }
  const y = target();
  if (Math.abs(y - scrollY) > innerHeight * 1.5) scrollTo({ top: y + (y > scrollY ? -innerHeight * .6 : innerHeight * .6), behavior: 'instant' });
  scrollTo({ top: target(), behavior: reduce ? 'instant' : 'smooth' });
  [550, 1100].forEach(t => setTimeout(fix, t));
}
window.goTo = goTo;
document.addEventListener('click', e => {
  const a = e.target.closest('a[href^="#"]'); if (!a) return;
  const id = a.getAttribute('href').slice(1); if (!id) return;
  e.preventDefault(); goTo(id); history.replaceState(null, '', id === 'top' ? location.pathname : '#' + id);
});

/* ---------- menu ---------- */
const menu = $('.menu'), burger = $('.burger');
function closeMenu() { if (!document.body.classList.contains('menu-open')) return; document.body.classList.remove('menu-open'); burger.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-hidden', 'true'); if (lenis) lenis.start(); }
burger.addEventListener('click', () => { document.body.classList.add('menu-open'); burger.setAttribute('aria-expanded', 'true'); menu.setAttribute('aria-hidden', 'false'); if (lenis) lenis.stop(); });
$('#menu-x').addEventListener('click', closeMenu);

/* ---------- active section in the nav and quick tabs, bottom booking bar ---------- */
(function () {
  const links = $$('.nav a, .chips a'), ids = [...new Set(links.map(a => a.dataset.sec))];
  const secs = ids.map(id => document.getElementById(id)).filter(Boolean).sort((x, y) => (x.compareDocumentPosition(y) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1);
  const bar = $('#mbar'), card = $('#pcard'), heroCta = $('#hero-cta'), chips = $('.chips');
  let raf = 0, last = '';
  function upd() {
    raf = 0; const y = hb() + innerHeight * .25; let cur = '';
    secs.forEach(s => { if (s.getBoundingClientRect().top < y) cur = s.id; });
    if (cur !== last) {
      last = cur; links.forEach(a => a.classList.toggle('on', a.dataset.sec === cur));
      const q = $('a.on', chips); if (q && chips.scrollWidth > chips.clientWidth) chips.scrollTo({ left: q.offsetLeft - chips.clientWidth / 2 + q.offsetWidth / 2, behavior: 'smooth' });
    }
    const r = card.getBoundingClientRect(), c = heroCta.getBoundingClientRect();
    const ctaVis = c.top < innerHeight - 70 && c.bottom > hb(), cardVis = r.top < innerHeight && r.bottom > 0;
    bar.classList.toggle('show', !ctaVis && !cardVis && !document.body.classList.contains('lb-open'));
  }
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true }); upd();
  window.navUpd = upd;
})();

/* ---------- hero halo follows the mouse (computer) ---------- */
(function () {
  const h = $('.hero'); if (!h || !fine || reduce) return;
  let raf = 0, x = 0, y = 0;
  h.addEventListener('pointermove', e => { const r = h.getBoundingClientRect(); x = e.clientX - r.left; y = e.clientY - r.top;
    if (!raf) raf = requestAnimationFrame(() => { raf = 0; h.style.setProperty('--mx', x + 'px'); h.style.setProperty('--my', y + 'px'); }); }, { passive: true });
})();

/* ---------- free community bar ----------
   PAUSE / PLAY: the bar at the top inviting to the free WhatsApp community.
   Paused during the big sale so visitors are not pulled away from the offer.
   To turn it back on, set SHOW_COMMUNITY_BAR to true (nothing else to change).
   The free community link stays in the community section and the footer. */
const SHOW_COMMUNITY_BAR = false;
(function () {
  const bar = $('#cbar'); if (!bar || !SHOW_COMMUNITY_BAR) return;
  let closed = false; try { closed = sessionStorage.getItem('mc_cbar') === '0'; } catch (e) {}
  if (closed) return;
  setTimeout(() => { bar.hidden = false; requestAnimationFrame(() => requestAnimationFrame(() => bar.classList.add('on'))); }, 4000);
  $('.x', bar).addEventListener('click', () => { bar.classList.remove('on'); setTimeout(() => { bar.hidden = true; }, 400); try { sessionStorage.setItem('mc_cbar', '0'); } catch (e) {} });
})();

/* ---------- rotating headline word ---------- */
(function () {
  const spans = $$('.rot span'); if (spans.length < 2 || reduce) return;
  let i = 0;
  setInterval(() => {
    if (document.hidden || scrollY > innerHeight) return;
    const a = spans[i]; i = (i + 1) % spans.length; const b = spans[i];
    a.classList.remove('on'); a.classList.add('out'); b.classList.remove('out'); b.classList.add('on');
    setTimeout(() => a.classList.remove('out'), 750);
    const sr = $('.js-rot-sr'); if (sr) sr.textContent = b.textContent;
  }, 2400);
})();

/* ---------- manifesto: words light up one by one while scrolling ---------- */
(function () {
  const p = $('.js-mani'); if (!p) return;
  let words = [], raf = 0;
  window.maniSplit = function () {
    const walk = (node, key) => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/([ \t\n\r]+)/).forEach(w => { if (!w) return; if (/^[ \t\n\r]+$/.test(w)) frag.appendChild(document.createTextNode(w)); else { const s = document.createElement('span'); s.className = 'w' + (key ? ' k' : ''); s.textContent = w; frag.appendChild(s); } });
        n.replaceWith(frag);
      } else if (n.nodeType === 1) walk(n, key || n.tagName === 'EM');
    });
    walk(p, false); words = $$('.w', p); paint();
  };
  function paint() {
    raf = 0; const r = p.getBoundingClientRect(), vh = innerHeight;
    const k = reduce ? 1 : Math.max(0, Math.min(1, (vh * .82 - r.top) / (r.height + vh * .3)));
    const n = Math.round(k * words.length);
    words.forEach((w, i) => w.classList.toggle('on', i < n));
  }
  maniSplit();
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(paint); }, { passive: true });
})();

/* ---------- method: the three mock-ups play when they come into view ---------- */
(function () {
  const vis = $$('.js-vis'); if (!vis.length) return;
  function play(v) {
    if (v.classList.contains('go')) return; v.classList.add('go');
    const kind = v.dataset.kind;
    if (kind === 'prompt') {
      const el = $('.js-type', v), chips = $$('.ing span', v), txt = el.dataset[lang()];
      const showChips = () => chips.forEach((c, i) => setTimeout(() => c.classList.add('on'), 140 * i));
      if (reduce) { el.textContent = txt; el.dataset.done = 1; showChips(); return; }
      let i = 0; (function step() { i += 2; el.textContent = txt.slice(0, i); if (i < txt.length) setTimeout(step, 28); else { el.dataset.done = 1; el.textContent = el.dataset[lang()]; showChips(); } })();
    }
    if (kind === 'tl') $('.tl', v).classList.add('go');
  }
  if (!('IntersectionObserver' in window)) { vis.forEach(play); return; }
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { play(e.target); io.unobserve(e.target); } }), { threshold: .45 });
  vis.forEach(v => io.observe(v));
})();

/* ---------- YouTube iframe API, loaded once for every player on the page ---------- */
let ytP = null;
const ytApi = () => ytP || (ytP = new Promise((res, rej) => {
  if (window.YT && window.YT.Player) return res();
  window.onYouTubeIframeAPIReady = res;
  const sc = document.createElement('script'); sc.src = 'https://www.youtube.com/iframe_api'; sc.onerror = () => { ytP = null; rej(); }; document.head.appendChild(sc);
}));

/* ---------- portfolio: videos open in a clean player ---------- */
(function () {
  const lb = $('#lb'), scr = $('.scr', lb), cards = $$('.wc[data-yt], .wc[data-mp4]');
  scr.addEventListener('scroll', () => { scr.scrollTop = 0; scr.scrollLeft = 0; });
  let seen = []; try { seen = JSON.parse(localStorage.getItem('mc_seen') || '[]'); } catch (e) {}
  cards.forEach(c => { if (c.dataset.yt && seen.includes(c.dataset.yt)) c.classList.add('seen'); });
  let pl = null, timer = 0, media = null, opener = null;
  const loadApi = ytApi;
  const fmt = t => { t = Math.max(0, Math.floor(t || 0)); return Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0'); };
  const set = (k, on) => lb.classList.toggle(k, on);
  function open(c) {
    opener = c; close(true);
    $('.js-lbt', lb).innerHTML = $('.cp b', c).innerHTML; $('.js-lbs', lb).innerHTML = $('.cp span', c).innerHTML;
    const au = $('.js-aud-el'); if (au && !au.paused) au.pause();
    if (window.vpPause) vpPause();
    lb.classList.add('on'); lb.setAttribute('aria-hidden', 'false'); document.body.classList.add('lb-open'); if (window.navUpd) navUpd();
    if (lenis) lenis.stop(); else document.documentElement.style.overflow = 'hidden';
    if (c.dataset.yt) {
      c.classList.add('seen'); if (!seen.includes(c.dataset.yt)) { seen.push(c.dataset.yt); try { localStorage.setItem('mc_seen', JSON.stringify(seen)); } catch (e) {} }
      yt(c.dataset.yt);
    } else {
      set('mp4', true);
      media = document.createElement('video'); media.src = c.dataset.mp4; media.poster = c.dataset.poster || ''; media.controls = true; media.playsInline = true; media.autoplay = true; media.setAttribute('playsinline', '');
      scr.prepend(media); media.play().catch(() => {});
    }
    setTimeout(() => $('.cls', lb).focus({ preventScroll: true }), 50);
  }
  function yt(id) {
    const host = document.createElement('div'); host.className = 'host'; const slot = document.createElement('div'); host.appendChild(slot);
    const shield = document.createElement('div'); shield.className = 'shield';
    const ctrl = document.createElement('div'); ctrl.className = 'ctrl';
    ctrl.innerHTML = `<button type="button" class="pp" aria-label="Lecture / pause">${IC.pause}</button><div class="pg"><i></i></div><span class="tm">0:00 / 0:00</span><button type="button" class="mu" aria-label="Son">${IC.vol}</button>` + (scr.requestFullscreen ? `<button type="button" class="fs" aria-label="Plein écran">${IC.fs}</button>` : '');
    scr.prepend(host); scr.append(shield, ctrl); set('loading', true);
    const toggle = () => { if (pl && pl.getPlayerState) pl.getPlayerState() === 1 ? pl.pauseVideo() : pl.playVideo(); };
    shield.addEventListener('click', toggle);
    $('.pp', ctrl).addEventListener('click', toggle);
    $('.mu', ctrl).addEventListener('click', () => { if (!pl) return; if (pl.isMuted()) { pl.unMute(); pl.setVolume(100); set('muted', false); } else pl.mute(); sync(); });
    const fs = $('.fs', ctrl); if (fs) fs.addEventListener('click', () => document.fullscreenElement ? document.exitFullscreen() : scr.requestFullscreen().catch(() => {}));
    $('.pg', ctrl).addEventListener('click', e => { if (!pl) return; const r = e.currentTarget.getBoundingClientRect(); pl.seekTo((e.clientX - r.left) / r.width * pl.getDuration(), true); });
    const mine = {}; media = mine;
    loadApi().then(() => {
      if (media !== mine) return;
      pl = new YT.Player(slot, { videoId: id, host: 'https://www.youtube-nocookie.com',
        playerVars: { autoplay: 1, controls: 0, rel: 0, playsinline: 1, iv_load_policy: 3, disablekb: 1, fs: 0, modestbranding: 1, cc_load_policy: 0 },
        events: {
          onReady: e => { e.target.playVideo(); setTimeout(() => { if (pl && pl.getPlayerState && pl.getPlayerState() !== 1) { pl.mute(); pl.playVideo(); set('muted', true); } }, 1500); },
          onStateChange: e => { const st = e.data; set('loading', st === 3 || st === -1); if (st === 0) { pl.seekTo(0, true); pl.pauseVideo(); } sync(); } } });
      timer = setInterval(sync, 500);
    }).catch(() => { set('loading', false); });
  }
  function sync() {
    if (!pl || !pl.getDuration) return;
    const d = pl.getDuration() || 0, t = pl.getCurrentTime() || 0, c = $('.ctrl', scr); if (!c) return;
    $('.pg i', c).style.width = d ? (t / d * 100) + '%' : 0;
    $('.tm', c).textContent = fmt(t) + ' / ' + fmt(d);
    $('.pp', c).innerHTML = pl.getPlayerState() === 1 ? IC.pause : IC.play;
    $('.mu', c).innerHTML = pl.isMuted() ? IC.mute : IC.vol;
  }
  function close(silent) {
    clearInterval(timer); timer = 0;
    if (pl && pl.destroy) { try { pl.destroy(); } catch (e) {} } pl = null; media = null;
    $$('video, .host, .shield, .ctrl', scr).forEach(n => { if (n.tagName === 'VIDEO') n.pause(); n.remove(); });
    ['mp4', 'loading', 'muted'].forEach(k => set(k, false));
    if (silent === true) return;
    lb.classList.remove('on'); lb.setAttribute('aria-hidden', 'true'); document.body.classList.remove('lb-open'); if (window.navUpd) navUpd();
    if (lenis) lenis.start(); else document.documentElement.style.overflow = '';
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    if (opener) opener.focus({ preventScroll: true });
  }
  $('.snd', lb).addEventListener('click', () => { if (pl) { pl.unMute(); pl.setVolume(100); set('muted', false); sync(); } });
  cards.forEach(c => c.addEventListener('click', () => open(c)));
  $('.cls', lb).addEventListener('click', () => close());
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && lb.classList.contains('on')) close(); });
  window.lbPause = () => { if (pl && pl.pauseVideo) pl.pauseVideo(); const v = $('video', scr); if (v) v.pause(); };
})();

/* ---------- computer hero: the course presentation (YouTube) in our own player ----------
   idle: poster + big play button. preview: muted loop starts by itself once the page has loaded.
   play: started by the visitor, with sound and full controls (seek, ±10 s, volume, speed, full screen). */
(function () {
  const vp = $('#vp'); if (!vp) return;
  const q = s => $(s, vp), scr = q('.vp-scr'), id = vp.dataset.yt;
  const mq = { matches: true };
  scr.addEventListener('scroll', () => { scr.scrollTop = 0; scr.scrollLeft = 0; });
  const fmt = t => { t = Math.max(0, Math.floor(t || 0)); return Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0'); };
  const set = (k, on) => vp.classList.toggle(k, on);
  const RATES = [1, 1.25, 1.5, 2];
  let pl = null, ready = null, mode = 'idle', vol = 80, rate = 1, timer = 0, hideT = 0, seekDrag = null, vDrag = false, lastKey = '', seen = false;
  try { const v = localStorage.getItem('mc_vol'); if (v !== null) vol = Math.max(0, Math.min(100, +v)); } catch (e) {}

  function build(muted) {
    if (ready) return ready;
    set('loading', true);
    ready = ytApi().then(() => new Promise(res => {
      pl = new YT.Player(q('.vp-slot'), {
        videoId: id, host: 'https://www.youtube-nocookie.com',
        playerVars: { autoplay: 1, mute: muted ? 1 : 0, controls: 0, rel: 0, playsinline: 1, iv_load_policy: 3, disablekb: 1, fs: 0, modestbranding: 1, cc_load_policy: 0 },
        events: {
          onReady: e => { if (muted) e.target.mute(); else { e.target.unMute(); e.target.setVolume(vol); } e.target.playVideo(); res(); },
          onStateChange: onState,
          onError: () => set('loading', false)
        }
      });
      if (!timer) timer = setInterval(sync, 250);
    })).catch(() => { set('loading', false); ready = null; if (mode === 'preview') { mode = 'idle'; set('preview', false); } });
    return ready;
  }
  function onState(e) {
    const st = e.data;
    set('loading', st === 3);
    set('playing', st === 1);
    set('paused', mode === 'play' && st === 2);
    if (st === 1) set('started', true);
    if (st === 0) { if (mode === 'preview') { pl.seekTo(0, true); pl.playVideo(); } else { set('ended', true); set('ui', false); } }
    else if (st === 1) set('ended', false);
    lastKey = ''; sync();
  }
  function others() { const a = $('.js-aud-el'); if (a && !a.paused) a.pause(); if (window.lbPause) lbPause(); }
  function preview() {
    if (mode !== 'idle' || !mq.matches || reduce) return;
    const cn = navigator.connection; if (cn && (cn.saveData || /(^|-)2g$/.test(cn.effectiveType || ''))) return;
    mode = 'preview'; set('preview', true); build(true);
  }
  function withSound() {
    const wasPreview = mode === 'preview';
    mode = 'play'; set('preview', false); set('sound', true); set('ended', false); others();
    const go = () => {
      if (!pl || !pl.unMute) return;
      pl.unMute(); pl.setVolume(vol || 60); if (wasPreview) pl.seekTo(0, true); pl.playVideo(); if (rate !== 1) pl.setPlaybackRate(rate);
      setTimeout(() => { if (mode === 'play' && pl.getPlayerState && pl.getPlayerState() !== 1 && pl.getPlayerState() !== 3) { pl.mute(); pl.playVideo(); } lastKey = ''; sync(); }, 1600);
    };
    (ready || build(false)).then(go);
    flash('play'); poke(); center();
  }
  // bring the whole player into view, controls included
  function center() {
    const r = vp.getBoundingClientRect(), top = hb() + 12;
    if (r.top >= top && r.bottom <= innerHeight - 8) return;
    const y = Math.max(0, scrollY + r.top - Math.max(top, (innerHeight - r.height) / 2));
    if (lenis) lenis.scrollTo(y, { duration: 1 }); else scrollTo({ top: y, behavior: 'smooth' });
  }
  function toggle() {
    if (mode !== 'play') return withSound();
    if (!pl || !pl.getPlayerState) return;
    if (vp.classList.contains('ended')) return replay();
    const on = pl.getPlayerState() === 1;
    if (on) pl.pauseVideo(); else { others(); pl.playVideo(); }
    flash(on ? 'pause' : 'play'); poke();
  }
  function replay() { if (!pl) return; set('ended', false); pl.seekTo(0, true); pl.playVideo(); flash('play'); poke(); }
  function flash(k) { const f = q('.vp-flash'); f.innerHTML = IC[k] || ''; f.classList.remove('go'); void f.offsetWidth; f.classList.add('go'); }
  function poke() { set('ui', true); clearTimeout(hideT); hideT = setTimeout(() => { if (!seekDrag && !vDrag) set('ui', false); }, 2600); }
  function sync() {
    if (!pl || !pl.getDuration) return;
    const d = pl.getDuration() || 0, t = seekDrag != null ? seekDrag * d : (pl.getCurrentTime() || 0);
    const st = pl.getPlayerState ? pl.getPlayerState() : -1, muted = pl.isMuted ? pl.isMuted() : true;
    q('.vp-fill').style.width = (d ? Math.min(100, t / d * 100) : 0) + '%';
    q('.vp-buf').style.width = ((pl.getVideoLoadedFraction ? pl.getVideoLoadedFraction() : 0) * 100) + '%';
    q('.vp-tm b').textContent = fmt(t); q('.vp-tm span').textContent = fmt(d);
    const key = (st === 1) + '|' + muted + '|' + vol;
    if (key === lastKey) return; lastKey = key;
    q('.vp-pp').innerHTML = st === 1 ? IC.pause : IC.play;
    q('.vp-mu').innerHTML = muted || vol === 0 ? IC.mute : vol < 50 ? IC.volLow : IC.vol;
    q('.vp-vf').style.width = (muted ? 0 : vol) + '%';
    q('.vp-vs').setAttribute('aria-valuenow', muted ? 0 : vol);
    set('muted', mode === 'play' && muted);
  }
  const ratio = (el, x) => { const r = el.getBoundingClientRect(); return Math.max(0, Math.min(1, (x - r.left) / r.width)); };

  // progress: hover shows the time, click or drag to seek
  const pg = q('.vp-pg'), tip = q('.vp-tip');
  pg.addEventListener('pointermove', e => {
    const d = pl && pl.getDuration ? pl.getDuration() : 0, k = ratio(pg, e.clientX);
    tip.textContent = fmt(k * d); tip.style.left = (k * 100) + '%';
    if (seekDrag != null) { seekDrag = k; sync(); }
  });
  pg.addEventListener('pointerdown', e => { if (!pl) return; try { pg.setPointerCapture(e.pointerId); } catch (x) {} seekDrag = ratio(pg, e.clientX); set('drag', true); sync(); });
  const endSeek = () => { if (seekDrag == null || !pl) return; pl.seekTo(seekDrag * (pl.getDuration() || 0), true); seekDrag = null; set('drag', false); set('ended', false); poke(); };
  pg.addEventListener('pointerup', endSeek); pg.addEventListener('pointercancel', endSeek);

  // volume: the bar opens on hover; click or drag to set it, the button mutes
  const vs = q('.vp-vs');
  const setVol = v => {
    vol = Math.round(Math.max(0, Math.min(100, v))); try { localStorage.setItem('mc_vol', vol); } catch (e) {}
    if (!pl || !pl.setVolume) return;
    if (vol === 0) pl.mute(); else { pl.unMute(); pl.setVolume(vol); }
    lastKey = ''; sync();
  };
  vs.addEventListener('pointerdown', e => { try { vs.setPointerCapture(e.pointerId); } catch (x) {} vDrag = true; set('vdrag', true); setVol(ratio(vs, e.clientX) * 100); });
  vs.addEventListener('pointermove', e => { if (vDrag) setVol(ratio(vs, e.clientX) * 100); });
  const endV = () => { vDrag = false; set('vdrag', false); };
  vs.addEventListener('pointerup', endV); vs.addEventListener('pointercancel', endV);
  q('.vp-mu').addEventListener('click', () => {
    if (!pl || !pl.isMuted) return;
    if (pl.isMuted() || vol === 0) { if (vol === 0) vol = 60; pl.unMute(); pl.setVolume(vol); } else pl.mute();
    lastKey = ''; sync(); poke();
  });

  q('.vp-pp').addEventListener('click', toggle);
  q('.vp-rw').addEventListener('click', () => { if (pl && pl.seekTo) { pl.seekTo(Math.max(0, pl.getCurrentTime() - 10), true); flash('rw'); poke(); } });
  q('.vp-fw').addEventListener('click', () => { if (pl && pl.seekTo) { pl.seekTo(Math.min(pl.getDuration() - 1, pl.getCurrentTime() + 10), true); flash('fw'); poke(); } });
  q('.vp-sp').addEventListener('click', e => {
    rate = RATES[(RATES.indexOf(rate) + 1) % RATES.length]; if (pl && pl.setPlaybackRate) pl.setPlaybackRate(rate);
    const b = e.currentTarget; b.textContent = (lang() === 'fr' ? String(rate).replace('.', ',') : String(rate)) + '×';
    b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop'); poke();
  });
  const rfs = scr.requestFullscreen || scr.webkitRequestFullscreen;
  if (!rfs) q('.vp-fs').hidden = true;
  q('.vp-fs').addEventListener('click', () => {
    const cur = document.fullscreenElement || document.webkitFullscreenElement;
    if (cur) (document.exitFullscreen || document.webkitExitFullscreen).call(document); else if (rfs) { const p = rfs.call(scr); if (p && p.catch) p.catch(() => {}); }
  });
  const onFs = () => { const on = (document.fullscreenElement || document.webkitFullscreenElement) === scr; set('fs', on); q('.vp-fs').innerHTML = on ? IC.fsx : IC.fs; };
  document.addEventListener('fullscreenchange', onFs); document.addEventListener('webkitfullscreenchange', onFs);

  q('.vp-big').addEventListener('click', e => { e.stopPropagation(); withSound(); });
  // on touch screens the first tap only brings the controls back
  q('.vp-shield').addEventListener('click', () => { if (mode === 'play' && !vp.classList.contains('ui') && !vp.classList.contains('paused') && matchMedia('(hover: none)').matches) { poke(); return; } toggle(); });
  q('.vp-snd').addEventListener('click', e => { e.stopPropagation(); if (pl && pl.unMute) { if (vol === 0) vol = 60; pl.unMute(); pl.setVolume(vol); lastKey = ''; sync(); } });
  q('.vp-again').addEventListener('click', replay);
  vp.addEventListener('pointermove', () => { if (mode === 'play') poke(); });
  vp.addEventListener('pointerleave', () => { if (mode === 'play' && pl && pl.getPlayerState && pl.getPlayerState() === 1 && !seekDrag && !vDrag) set('ui', false); });
  vp.addEventListener('keydown', e => {
    const k = e.key, onBtn = e.target.closest('button, a');
    if ((k === ' ' || k === 'Enter') && onBtn) return;
    if (k === ' ' || k === 'k') { e.preventDefault(); toggle(); return; }
    if (!pl || mode !== 'play' || !pl.seekTo) return;
    if (k === 'ArrowRight') { e.preventDefault(); pl.seekTo(pl.getCurrentTime() + 5, true); flash('fw'); }
    else if (k === 'ArrowLeft') { e.preventDefault(); pl.seekTo(Math.max(0, pl.getCurrentTime() - 5), true); flash('rw'); }
    else if (k === 'ArrowUp') { e.preventDefault(); setVol(vol + 10); }
    else if (k === 'ArrowDown') { e.preventDefault(); setVol(vol - 10); }
    else if (k === 'm') q('.vp-mu').click();
    else if (k === 'f') q('.vp-fs').click();
    poke();
  });

  // the muted preview starts once the page has loaded and the screen is in view; it pauses off screen
  let loaded = document.readyState === 'complete';
  if (!loaded) addEventListener('load', () => { loaded = true; if (seen) setTimeout(preview, 900); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(es => {
      const vis = es[0].isIntersecting; seen = seen || vis;
      if (vis && mode === 'idle' && loaded) setTimeout(preview, 900);
      if (mode === 'preview' && pl && pl.getPlayerState) { if (vis && !document.body.classList.contains('lb-open')) pl.playVideo(); else pl.pauseVideo(); }
    }, { rootMargin: '150px 0px' }).observe(vp);
  }
  if (mq.addEventListener) mq.addEventListener('change', () => { if (!mq.matches && pl && pl.pauseVideo) pl.pauseVideo(); });
  window.vpPause = () => { if (pl && pl.getPlayerState && pl.getPlayerState() === 1) pl.pauseVideo(); };
  const au = $('.js-aud-el'); if (au) au.addEventListener('play', () => window.vpPause());
})();

/* ---------- classic editing vs Vibe Motion ---------- */
(function () {
  const box = $('#cmp'); if (!box) return;
  const btns = $$('.sw button', box); let touched = false;
  function mode(m) {
    const ai = m === 'a'; if (box.classList.contains('ai') === ai) return;
    box.classList.toggle('ai', ai); btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.m === m));
    $$('.mx b', box).forEach((b, i) => { b.classList.remove('flip'); void b.offsetWidth; b.style.animationDelay = (i * 60) + 'ms'; b.classList.add('flip'); });
  }
  btns.forEach(b => b.addEventListener('click', () => { touched = true; mode(b.dataset.m); }));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { if (es[0].isIntersecting) { io.disconnect(); setTimeout(() => { if (!touched) mode('a'); }, 1400); } }, { threshold: .55 }); io.observe(box);
  }
})();

/* ---------- programme chapters and profiles ---------- */
(function () {
  const tabs = $$('.ctab'), pans = $$('.cpan');
  tabs.forEach(t => t.addEventListener('click', () => {
    tabs.forEach(x => x.setAttribute('aria-selected', x === t));
    pans.forEach(p => { p.classList.toggle('on', p.dataset.ch === t.dataset.ch); if (p.dataset.ch !== t.dataset.ch) $$('details[open]', p).forEach(d => { d.open = false; }); });
    if (window.ScrollTrigger) setTimeout(() => ScrollTrigger.refresh(), 60);
  }));
  const pills = $$('.who .pills button'), wp = $$('.wpan');
  pills.forEach(b => b.addEventListener('click', () => {
    pills.forEach(x => x.setAttribute('aria-pressed', x === b));
    wp.forEach(p => p.classList.toggle('on', p.dataset.w === b.dataset.w));
    if (window.ScrollTrigger) setTimeout(() => ScrollTrigger.refresh(), 60);
  }));
})();

/* ---------- accordions: one open at a time ---------- */
$$('.faq, .cpan').forEach(box => box.addEventListener('toggle', e => {
  const d = e.target; if (d.tagName !== 'DETAILS' || d.parentElement !== box) return;
  if (d.open) $$(':scope > details[open]', box).forEach(o => { if (o !== d) o.open = false; });
  if (window.ScrollTrigger) setTimeout(() => ScrollTrigger.refresh(), 60);
}, true));

/* ---------- pause CSS animations in blocks that are off screen ---------- */
(function () {
  if (!('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('zz', !e.isIntersecting)), { rootMargin: '150px 0px' });
  $$('main > section, .loop, .ft').forEach(el => io.observe(el));
})();

/*COUNTDOWN*/

/*ROI*/

/*AUDIO*/

/*TOAST*/

/*FX*/

/* ---------- SasPay checkout: the booking buttons open a short form, the server creates the payment page ----------
   Used only when /api/checkout says SasPay is configured (secret key on Vercel); otherwise the
   buttons keep their Chariow link. */
(function () {
  const co = $('#co'); if (!co) return;
  const form = $('form', co), err = $('.co-err', co), go = $('.co-go', co);
  let enabled = false, last = null;
  fetch('/api/checkout', { headers: { Accept: 'application/json' } }).then(r => r.ok ? r.json() : null).then(d => { enabled = !!(d && d.enabled); }).catch(() => {});
  const T = k => ({ fr: { name: 'Indiquez votre prénom et votre nom.', mail: 'Vérifiez votre adresse e-mail.', fail: "Le paiement n'a pas pu démarrer. Réessayez ou écrivez-nous sur WhatsApp." }, en: { name: 'Enter your first and last name.', mail: 'Check your email address.', fail: 'Payment could not start. Try again or message us on WhatsApp.' } })[lang()][k];
  function open(a) {
    last = a; co.hidden = false; requestAnimationFrame(() => co.classList.add('on'));
    if (lenis) lenis.stop(); else document.documentElement.style.overflow = 'hidden';
    try { const s = JSON.parse(localStorage.getItem('mc_buyer') || '{}'); ['firstName', 'lastName', 'email', 'phone'].forEach(k => { if (s[k] && !form[k].value) form[k].value = s[k]; }); } catch (e) {}
    setTimeout(() => (form.firstName.value ? form.email : form.firstName).focus({ preventScroll: true }), 60);
  }
  function close() {
    co.classList.remove('on'); setTimeout(() => { co.hidden = true; }, 300);
    if (lenis) lenis.start(); else document.documentElement.style.overflow = '';
    if (last) last.focus({ preventScroll: true });
  }
  function fail(msg, field) { err.textContent = msg; err.hidden = false; if (field) { field.setAttribute('aria-invalid', 'true'); field.focus(); } }
  // capture phase: runs before the Chariow redirect of the Pixel handler
  document.addEventListener('click', e => {
    const a = e.target.closest('.js-cta'); if (!a || !enabled || e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1) return;
    e.preventDefault(); e.stopImmediatePropagation();
    try { if (window.fbq) fbq('track', 'InitiateCheckout', { content_name: 'Formation Montage IA' }); } catch (x) {}
    open(a);
  }, true);
  $('.co-x', co).addEventListener('click', close);
  co.addEventListener('click', e => { if (e.target === co) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !co.hidden) close(); });
  form.addEventListener('input', e => { e.target.removeAttribute('aria-invalid'); err.hidden = true; });
  form.addEventListener('submit', async e => {
    e.preventDefault(); err.hidden = true;
    const d = { firstName: form.firstName.value.trim(), lastName: form.lastName.value.trim(), email: form.email.value.trim(), phone: form.phone.value.trim() };
    if (!d.firstName) return fail(T('name'), form.firstName);
    if (!d.lastName) return fail(T('name'), form.lastName);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) return fail(T('mail'), form.email);
    try { localStorage.setItem('mc_buyer', JSON.stringify(d)); } catch (x) {}
    go.disabled = true; go.classList.add('wait');
    try {
      const r = await fetch('/api/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) });
      const j = await r.json().catch(() => null);
      if (r.ok && j && /^https:\/\//.test(j.url)) {
        try { localStorage.setItem('mc_sess', j.id); } catch (x) {}
        try { if (window.fbq) fbq('track', 'AddPaymentInfo'); } catch (x) {}
        location.href = j.url; return;
      }
      if (j && j.error === 'invalid_email') fail(T('mail'), form.email); else fail(T('fail'));
    } catch (x) { fail(T('fail')); }
    go.disabled = false; go.classList.remove('wait');
  });
  window.__co = { enable: v => { enabled = v; } };
})();

/* ---------- Back from SasPay (?paiement=merci): the server asks SasPay for the real status,
   and only a confirmed payment reveals the course link ---------- */
(function () {
  const ty = $('#ty'); if (!ty || !/[?&]paiement=merci\b/.test(location.search)) return;
  let id = ''; try { id = localStorage.getItem('mc_sess') || ''; } catch (e) {}
  const h = $('#ty-h', ty), p = $('.ty-p', ty), go = $('.ty-go', ty), re = $('.ty-re', ty);
  const M = {
    fr: { wait: ['Confirmation du paiement…', 'Quelques secondes, nous vérifions votre paiement auprès de SasPay.'],
          ok: ['Bienvenue dans Vibe Motion !', 'Votre paiement est confirmé. Gardez bien ce lien : c\'est votre accès à la formation.'],
          okn: ['Paiement confirmé !', 'Merci ! Écrivez-moi sur WhatsApp pour recevoir votre accès tout de suite.'],
          slow: ['Paiement en cours de confirmation', 'Si vous avez validé sur votre téléphone, patientez un instant puis vérifiez à nouveau.'],
          none: ['Merci !', 'Nous ne retrouvons pas votre paiement sur cet appareil. Écrivez-moi sur WhatsApp avec votre reçu, je vous donne l\'accès.'] },
    en: { wait: ['Confirming your payment…', 'A few seconds, we are checking your payment with SasPay.'],
          ok: ['Welcome to Vibe Motion!', 'Your payment is confirmed. Keep this link safe: it is your access to the course.'],
          okn: ['Payment confirmed!', 'Thank you! Message me on WhatsApp to get your access right away.'],
          slow: ['Payment being confirmed', 'If you approved it on your phone, wait a moment then check again.'],
          none: ['Thank you!', 'We cannot find your payment on this device. Message me on WhatsApp with your receipt and I will give you access.'] }
  };
  const show = k => { const m = M[lang()][k]; h.textContent = m[0]; p.textContent = m[1]; ty.classList.toggle('wait', k === 'wait'); };
  function open() { ty.hidden = false; requestAnimationFrame(() => ty.classList.add('on')); if (lenis) lenis.stop(); else document.documentElement.style.overflow = 'hidden'; }
  function close() { ty.classList.remove('on'); setTimeout(() => { ty.hidden = true; }, 300); if (lenis) lenis.start(); else document.documentElement.style.overflow = ''; }
  $('.co-x', ty).addEventListener('click', close);
  ty.addEventListener('click', e => { if (e.target === ty) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !ty.hidden) close(); });
  // clean the address bar so a shared link does not reopen this sheet
  try { history.replaceState(null, '', location.pathname + location.hash); } catch (e) {}
  let tries = 0;
  async function check() {
    re.hidden = true; show('wait');
    try {
      const r = await fetch('/api/checkout?session=' + encodeURIComponent(id), { headers: { Accept: 'application/json' } });
      const j = await r.json().catch(() => null);
      if (r.ok && j && j.paid) {
        if (j.access && /^https:\/\//.test(j.access)) { go.href = j.access; go.hidden = false; show('ok'); } else show('okn');
        const grp = $('.ty-grp', ty); if (j.group && /^https:\/\/chat\.whatsapp\.com\//.test(j.group)) { grp.href = j.group; grp.hidden = false; }
        try { if (localStorage.getItem('mc_paid') !== id && window.fbq) fbq('track', 'Purchase', { value: 5500, currency: 'XOF', content_name: 'Formation Montage IA' }); localStorage.setItem('mc_paid', id); } catch (x) {}
        return;
      }
      if (r.status === 404 || r.status === 400) return show('none');
    } catch (x) {}
    if (++tries < 6) return setTimeout(check, 5000);
    show('slow'); re.hidden = false;
  }
  re.addEventListener('click', () => { tries = 3; check(); });
  open();
  if (!id) show('none'); else check();
})();

/* ---------- Promo card: first after 12 s, then 40 s after each close; never over a form, a video or the menu ---------- */
(function () {
  const pp = $('#pp'); if (!pp) return;
  try { if (sessionStorage.getItem('mc_pp') === '0') return; } catch (e) {} // test switch
  let t = 0;
  const busy = () => document.hidden || $$('#co:not([hidden]), #ty:not([hidden]), .lb.on, .menu.on, body.menu-open').length > 0
    || (document.activeElement && /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName));
  function show() {
    if (busy()) { t = setTimeout(show, 8000); return; }
    pp.hidden = false; requestAnimationFrame(() => requestAnimationFrame(() => pp.classList.add('on')));
  }
  function hide() { pp.classList.remove('on'); setTimeout(() => { pp.hidden = true; }, 350); clearTimeout(t); t = setTimeout(show, 40000); }
  $('.pp-x', pp).addEventListener('click', hide);
  $('.pp-later', pp).addEventListener('click', hide);
  pp.addEventListener('click', e => { if (e.target === pp) hide(); if (e.target.closest('.js-cta')) { pp.classList.remove('on'); pp.hidden = true; clearTimeout(t); t = setTimeout(show, 40000); } });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !pp.hidden) hide(); });
  t = setTimeout(show, 12000);
  window.__pp = { show, hide };
})();

/* ---------- Meta Pixel events ----------
   InitiateCheckout: booking buttons (wait 250 ms so the event leaves before Chariow opens).
   Lead: free community. Contact: WhatsApp. */
(function () {
  const track = (ev, data) => { try { if (window.fbq) fbq('track', ev, data || {}); } catch (e) {} };
  $$('.js-cta').forEach(a => a.addEventListener('click', e => {
    track('InitiateCheckout', { content_name: 'Formation Montage IA' });
    if (!window.fbq || e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1) return;
    e.preventDefault(); const url = a.href; setTimeout(() => { location.href = url; }, 250);
  }));
  $$('.cbar .go, .js-lead').forEach(a => a.addEventListener('click', () => track('Lead', { content_name: 'Communauté LE DIGITAL POUR TOUS' })));
  $$('.waf, .js-wa').forEach(a => a.addEventListener('click', () => track('Contact')));
})();

/* ---------- init language ---------- */
let L = /^en\b/i.test(navigator.language || '') ? 'en' : 'fr';
try { L = localStorage.getItem('mc_lang') || L; } catch (e) {}
if (L === 'en') setLang('en');

/* ---------- the journey: captions follow the scroll, the 3D tunnel joins when ready ---------- */
const tun = { sec: $('#traversee'), api: null, k: -1 };
function tunProgress(p) {
  if (tun.api) tun.api.setProgress(p);
  const words = $$('.js-tw span'), n = words.length, k = Math.min(n - 1, Math.floor(p * n * .999));
  $('.js-tp').style.width = (p * 100).toFixed(1) + '%';
  if (k === tun.k) return;
  const prev = tun.k; tun.k = k;
  words.forEach((w, i) => { w.classList.toggle('on', i === k); w.classList.toggle('out', i === prev && i !== k); });
  $('.js-tn').textContent = String(k + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0');
}
function tunnel3d() {
  if (!tun.sec || reduce) return;
  if (navigator.connection && navigator.connection.saveData) return;
  try { const c = document.createElement('canvas'); if (!(c.getContext('webgl2') || c.getContext('webgl'))) return; } catch (e) { return; }
  import('./assets/tunnel.js').then(m => {
    tun.api = m.start($('#tunnel'), { posters: JSON.parse(tun.sec.dataset.posters || '[]') });
    if (tun.api) { tun.api.setProgress(tun.p || 0); tun.sec.classList.add('ready'); }
  }).catch(() => {});
}

/* ---------- motion layer: GSAP + ScrollTrigger + Lenis ---------- */
function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
function splitWords(el) {
  const walk = node => [...node.childNodes].forEach(n => {
    if (n.nodeType === 3) {
      const frag = document.createDocumentFragment();
      n.textContent.split(/([ \t\n\r]+)/).forEach(p => { if (!p) return; if (/^[ \t\n\r]+$/.test(p)) frag.appendChild(document.createTextNode(p)); else { const s = document.createElement('span'); s.className = 'bw'; s.textContent = p; frag.appendChild(s); } });
      n.replaceWith(frag);
    } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
  });
  walk(el); return $$('.bw', el);
}
function noMotion() {}
// progress through the tall section while its stage stays in place
(function () {
  if (!tun.sec) return;
  const stk = $('.stk', tun.sec); let raf = 0;
  const upd = () => { raf = 0; const r = tun.sec.getBoundingClientRect(); tun.p = Math.max(0, Math.min(1, (hb() - r.top) / Math.max(1, r.height - stk.offsetHeight))); tunProgress(tun.p); };
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true }); addEventListener('resize', upd); upd();
})();
function motion() {
  if (reduce || !window.gsap || !window.ScrollTrigger) { noMotion(); return; }
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.config({ ignoreMobileResize: true });
  if (fine && window.Lenis) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
    document.documentElement.classList.add('lenis');
  }
  const vh = innerHeight, bl = fine ? 'blur(6px)' : 'blur(0px)';
  // hero: the giant word sinks slower than the page, the portrait lifts away
  gsap.to('.giant', { '--py': '22vh', ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.to('.subject', { '--sy': '-6vh', ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  // headings: words float in
  $$('.bt').forEach(h => { if (h.getBoundingClientRect().top < vh * .9) return; const w = splitWords(h);
    gsap.fromTo(w, { opacity: 0, y: 22, filter: bl }, { opacity: 1, y: 0, filter: 'blur(0px)', clearProps: 'filter', duration: .9, ease: 'power3.out', stagger: .045, scrollTrigger: { trigger: h, start: 'top 88%' } }); });
  // blocks
  const below = $$('.rv').filter(el => el.getBoundingClientRect().top > vh * .92);
  gsap.set(below, fine ? { opacity: 0, y: 36, filter: bl } : { opacity: 0, y: 36 });
  ScrollTrigger.batch(below, { start: 'top 90%', onEnter: b => gsap.to(b, { opacity: 1, y: 0, ...(fine ? { filter: 'blur(0px)' } : {}), clearProps: 'filter,transform', duration: .9, ease: 'power3.out', stagger: .08, overwrite: true }) });
  // method: each card sinks back as the next one slides over it
  const mm = gsap.matchMedia();
  // computer hero: the trailer screen straightens up as the visitor scrolls
  mm.add('(min-width: 768px)', () => {
    gsap.fromTo('.vp', { '--tilt': '14deg', '--sc': .94 }, { '--tilt': '0deg', '--sc': 1, ease: 'none', scrollTrigger: { trigger: '.hvid', start: 'top 92%', end: 'top 20%', scrub: true } });
  });
  mm.add('(min-width: 1000px) and (min-height: 701px)', () => {
    const acts = $$('.act');
    acts.slice(0, -1).forEach((a, i) => gsap.to(a, { scale: .94, '--dim': .55, ease: 'none', scrollTrigger: { trigger: acts[i + 1], start: 'top bottom', end: () => 'top top+=' + (hb() + 16 + (i + 1) * 18), scrub: true } }));
  });
  addEventListener('load', () => ScrollTrigger.refresh());
}
const idle = window.requestIdleCallback || (f => setTimeout(f, 200));
const ready = Promise.all([loadScript('assets/gsap.min.js'), loadScript('assets/ScrollTrigger.min.js'), fine ? loadScript('assets/lenis.min.js').catch(() => {}) : Promise.resolve()])
  .then(motion).catch(noMotion);
ready.then(() => { if (location.hash.length > 1) setTimeout(() => goTo(decodeURIComponent(location.hash.slice(1))), 120); });
if (document.readyState === 'complete') idle(tunnel3d); else addEventListener('load', () => idle(tunnel3d));
