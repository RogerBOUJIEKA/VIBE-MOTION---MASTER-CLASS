/* ---------- promo countdown: 24 h per visitor, kept across visits, restarts by itself ---------- */
(function () {
  const CYCLE = 24 * 3600 * 1000, KEY = 'mc_promo_start';
  let start = 0;
  try { start = +localStorage.getItem(KEY) || 0; } catch (e) {}
  if (!start) { const m = document.cookie.match(/(?:^|; )mc_ps=(\d+)/); if (m) start = +m[1]; }
  const now = Date.now(); if (!start || start > now) start = now;
  try { localStorage.setItem(KEY, start); } catch (e) {}
  document.cookie = 'mc_ps=' + start + ';max-age=31536000;path=/;SameSite=Lax';
  const pad = n => String(n).padStart(2, '0');
  const boxes = document.querySelectorAll('.js-cd'), lines = document.querySelectorAll('.js-cd-hms');
  function tick() {
    const t = Math.floor((CYCLE - (Date.now() - start) % CYCLE) / 1000);
    const v = [Math.floor(t / 3600), Math.floor(t % 3600 / 60), t % 60].map(pad);
    boxes.forEach(b => b.querySelectorAll('b').forEach((el, i) => { if (el.textContent !== v[i]) { el.textContent = v[i]; if (i === 2) { el.classList.remove('tk'); void el.offsetWidth; el.classList.add('tk'); } } }));
    document.querySelectorAll('.js-cd-bar').forEach(b => { b.style.width = (t / (CYCLE / 1000) * 100).toFixed(2) + '%'; });
    lines.forEach(l => { l.textContent = v.join(':'); });
  }
  tick(); setInterval(() => { if (!document.hidden) tick(); }, 1000);
})();