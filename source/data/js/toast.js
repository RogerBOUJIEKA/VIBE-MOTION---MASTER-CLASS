/* ---------- notifications ----------
   BOOKINGS: real bookings only, added by hand with the buyer's consent, e.g.
   { name: "Aïcha", city: "Douala", cc: "CM", when: "il y a 2 h" }
   They are shown first; the rest of the rotation are true facts about the course. */
const BOOKINGS = [];
(function () {
  const box = document.getElementById('toast'), ic = box.querySelector('.t-ic'), b = box.querySelector('b'), sm = box.querySelector('small');
  let stopped = false; try { stopped = sessionStorage.getItem('mc_toast') === '0'; } catch (e) {}
  if (stopped) return;
  const flag = cc => cc.toUpperCase().replace(/./g, c => String.fromCodePoint(127397 + c.charCodeAt(0)));
  function items() {
    const en = document.documentElement.lang === 'en';
    const real = BOOKINGS.map(x => [flag(x.cc), x.name + ' (' + x.city + ')', (en ? 'joined the course' : 'a rejoint la formation') + (x.when ? ' · ' + x.when : '')]);
    const facts = [
      ['⚡', en ? 'Instant access' : 'Accès immédiat', en ? 'Watch the course right after payment' : 'Regardez la formation juste après le paiement'],
      ['💻', en ? 'Smartphone or computer' : 'Smartphone ou ordinateur', en ? 'Use the device you already have' : "Avec l'appareil que vous avez déjà"],
      ['🎁', en ? 'Video + PDF included' : 'Vidéo + PDF inclus', en ? 'Watch every step again at your own pace' : 'Revoyez chaque étape à votre rythme'],
      ['🔒', en ? 'Private group access' : 'Accès direct au groupe privé', en ? 'Right after payment' : 'Juste après le paiement'],
      ['💳', en ? 'Mobile Money or card' : 'Paiement Mobile Money ou carte', 'Orange Money · MoMo · Moov · Visa'],
      ['🔥', en ? '5,500 FCFA instead of 25,000' : '5 500 FCFA au lieu de 25 000', en ? 'Big sale · 24 hours only' : 'Grande promo · 24 h seulement'],
    ];
    for (let i = facts.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [facts[i], facts[j]] = [facts[j], facts[i]]; }
    return real.concat(facts);
  }
  let queue = items(), k = 0, shown = 0, t;
  function show() {
    if (stopped || shown >= 8 || document.hidden) { t = setTimeout(show, 15000); return; }
    if (k >= queue.length) { queue = items(); k = 0; }
    const [i, title, sub] = queue[k++]; ic.textContent = i; b.textContent = title; sm.textContent = sub;
    box.hidden = false; requestAnimationFrame(() => requestAnimationFrame(() => box.classList.add('on'))); shown++;
    t = setTimeout(() => { box.classList.remove('on'); t = setTimeout(show, 14000 + Math.random() * 9000); }, 5500);
  }
  t = setTimeout(show, 9000);
  box.addEventListener('click', e => {
    if (e.target.closest('.t-x')) { stopped = true; clearTimeout(t); box.classList.remove('on'); try { sessionStorage.setItem('mc_toast', '0'); } catch (x) {} return; }
    document.getElementById('offre').scrollIntoView({ behavior: 'smooth' });
  });
})();