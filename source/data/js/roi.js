/* ---------- Claude plan: earnings calculator ---------- */
(function () {
  const box = document.getElementById('roi'); if (!box) return;
  const q = s => box.querySelector(s), SUB = 12000, rr = q('.js-rr'), seg = [...box.querySelectorAll('.js-seg button')];
  const fmt = v => Math.round(v).toLocaleString(document.documentElement.lang === 'en' ? 'en-US' : 'fr-FR').replace(/ /g, ' ');
  let price = 50000, shown = 0, started = false, raf = 0;
  function animateTo(target) { cancelAnimationFrame(raf); const from = shown, t0 = performance.now();
    (function f(now) { const k = Math.min(1, (now - t0) / 700), e = 1 - Math.pow(1 - k, 3); shown = from + (target - from) * e; q('.js-rv').textContent = fmt(shown); if (k < 1) raf = requestAnimationFrame(f); })(t0); }
  window.roiCalc = function () {
    const n = +rr.value, rev = n * price;
    q('.js-rn').textContent = n; q('.js-rc').textContent = n; q('.js-bg').textContent = fmt(rev) + ' FCFA'; q('.js-rx').textContent = Math.floor(rev / SUB) + '×';
    if (!started) return; q('.js-bgb').style.width = '100%'; q('.js-bc').style.width = Math.max(2, SUB / rev * 100).toFixed(1) + '%'; animateTo(rev);
  };
  rr.addEventListener('input', roiCalc);
  seg.forEach(b => b.addEventListener('click', () => { price = +b.dataset.p; seg.forEach(x => x.setAttribute('aria-pressed', x === b)); roiCalc(); }));
  roiCalc();
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting) { started = true; roiCalc(); io.disconnect(); } }, { threshold: .35 }); io.observe(box);
})();