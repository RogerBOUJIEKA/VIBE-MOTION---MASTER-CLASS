/* ---------- hero audio pitch ---------- */
(function () {
  const box = document.querySelector('.aud'); if (!box) return;
  const a = box.querySelector('.js-aud-el'), btn = box.querySelector('.js-aud'), t = box.querySelector('.js-aud-t'), bars = [...box.querySelectorAll('.aud-w i')];
  const fmt = x => Math.floor(x / 60) + ':' + String(Math.floor(x % 60)).padStart(2, '0');
  const paint = () => { const k = a.duration ? a.currentTime / a.duration : 0, n = Math.round(k * bars.length); bars.forEach((b, i) => b.classList.toggle('on', i < n)); };
  btn.addEventListener('click', () => { if (a.paused) a.play().catch(() => {}); else a.pause(); });
  a.addEventListener('play', () => { box.classList.add('on'); document.querySelectorAll('video').forEach(v => { if (!v.paused) v.pause(); }); });
  a.addEventListener('pause', () => box.classList.remove('on'));
  a.addEventListener('ended', () => { box.classList.remove('on'); a.currentTime = 0; paint(); t.textContent = fmt(a.duration); });
  a.addEventListener('timeupdate', () => { if (a.currentTime > 0) t.textContent = fmt(a.currentTime); paint(); });
  a.addEventListener('loadedmetadata', () => { if (a.paused) t.textContent = fmt(a.duration); });
})();