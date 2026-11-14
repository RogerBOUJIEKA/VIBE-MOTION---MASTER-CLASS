/* ---------- local currency + local time, chosen automatically from the visitor's time zone ----------
   The payment itself stays in FCFA on Chariow; amounts in other currencies are estimates.
   Rates: live daily rates (currency-api), cached 12 h; the values below (12 Oct 2026) are the fallback. */
(function () {
  const PRICE = 5500, NAMES = {XAF:["FCFA","FCFA"],USD:["dollar américain","US dollar"],EUR:["euro","euro"],CAD:["dollar canadien","Canadian dollar"],GBP:["livre sterling","British pound"],CHF:["franc suisse","Swiss franc"],CDF:["franc congolais","Congolese franc"],GNF:["franc guinéen","Guinean franc"],NGN:["naira nigérian","Nigerian naira"],GHS:["cedi ghanéen","Ghanaian cedi"],MAD:["dirham marocain","Moroccan dirham"],DZD:["dinar algérien","Algerian dinar"],TND:["dinar tunisien","Tunisian dinar"],RWF:["franc rwandais","Rwandan franc"],BIF:["franc burundais","Burundian franc"],KES:["shilling kényan","Kenyan shilling"],ZAR:["rand sud-africain","South African rand"],KMF:["franc comorien","Comorian franc"],MGA:["ariary malgache","Malagasy ariary"],MRU:["ouguiya mauritanien","Mauritanian ouguiya"],DJF:["franc djiboutien","Djiboutian franc"],HTG:["gourde haïtienne","Haitian gourde"],AED:["dirham émirati","UAE dirham"]};
  const RATES = {usd:0.0017074959,eur:0.0015244902,cad:0.002435105,gbp:0.0012900629,chf:0.0014188134,cdf:3.95197988,gnf:15.02218249,ngn:2.27367723,ghs:0.020097125,mad:0.016695015,dzd:0.22972376,tnd:0.0050877317,rwf:2.5210712,bif:5.10742836,kes:0.22153785,zar:0.028186129,kmf:0.75,mga:7.61946569,mru:0.068189891,djf:0.30399081,htg:0.2234538,aed:0.0062707788};
  const TZ = {"Africa/Douala":"XAF","Africa/Libreville":"XAF","Africa/Brazzaville":"XAF","Africa/Ndjamena":"XAF","Africa/Bangui":"XAF","Africa/Malabo":"XAF","Africa/Abidjan":"XAF","Africa/Dakar":"XAF","Africa/Bamako":"XAF","Africa/Ouagadougou":"XAF","Africa/Niamey":"XAF","Africa/Lome":"XAF","Africa/Porto-Novo":"XAF","Africa/Bissau":"XAF","Africa/Kinshasa":"CDF","Africa/Lubumbashi":"CDF","Africa/Conakry":"GNF","Africa/Lagos":"NGN","Africa/Accra":"GHS","Africa/Casablanca":"MAD","Africa/El_Aaiun":"MAD","Africa/Algiers":"DZD","Africa/Tunis":"TND","Africa/Kigali":"RWF","Africa/Bujumbura":"BIF","Africa/Nairobi":"KES","Africa/Johannesburg":"ZAR","Africa/Nouakchott":"MRU","Africa/Djibouti":"DJF","Indian/Comoro":"KMF","Indian/Antananarivo":"MGA","America/Port-au-Prince":"HTG","Asia/Dubai":"AED","Europe/London":"GBP","Europe/Zurich":"CHF","America/Toronto":"CAD","America/Montreal":"CAD","America/Vancouver":"CAD","America/Edmonton":"CAD","America/Winnipeg":"CAD","America/Halifax":"CAD","America/Regina":"CAD","America/St_Johns":"CAD","America/Moncton":"CAD","America/Martinique":"EUR","America/Guadeloupe":"EUR","America/Cayenne":"EUR","Indian/Reunion":"EUR","Indian/Mayotte":"EUR"};
  const tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || '');
  const auto = TZ[tz] || (/^America\//.test(tz) ? 'USD' : /^Europe\//.test(tz) ? 'EUR' : 'XAF');
  let cur = auto; try { cur = localStorage.getItem('mc_cur') || auto; } catch (e) {}
  const sel = document.getElementById('fx-cur'), fx = document.querySelector('.js-fx'), fx2 = document.querySelector('.js-fx2'), note = document.querySelector('.fxnote');
  const en = () => document.documentElement.lang === 'en';
  function fmt(v, c) {
    const d = v >= 1000 ? 0 : 2;
    try { return new Intl.NumberFormat(en() ? 'en-US' : 'fr-FR', { style: 'currency', currency: c, minimumFractionDigits: d, maximumFractionDigits: d }).format(v); }
    catch (e) { return Math.round(v) + ' ' + c; }
  }
  function render() {
    sel.innerHTML = Object.keys(NAMES).map(c => '<option value="' + c + '">' + (c === 'XAF' ? 'FCFA' : c + ' · ' + NAMES[c][en() ? 1 : 0]) + '</option>').join('');
    if (!NAMES[cur]) cur = 'XAF';
    sel.value = cur;
    const r = cur === 'XAF' ? 0 : RATES[cur.toLowerCase()];
    if (!r) { fx.hidden = true; fx2.textContent = ''; note.hidden = true; return; }
    const txt = '≈ ' + fmt(PRICE * r, cur);
    fx.innerHTML = txt + ' <small>' + (en() ? '· estimate in your currency' : '· estimation dans votre devise') + '</small>';
    fx.hidden = false; fx2.textContent = txt; note.hidden = false;
  }
  window.fxRender = render;
  sel.addEventListener('change', () => { cur = sel.value; try { localStorage.setItem('mc_cur', cur); } catch (e) {} render(); });
  render();
  let cached = null; try { cached = JSON.parse(localStorage.getItem('mc_fx') || 'null'); } catch (e) {}
  if (cached && Date.now() - cached.t < 43200000) { Object.assign(RATES, cached.r); render(); return; }
  const urls = ['https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/xaf.min.json', 'https://latest.currency-api.pages.dev/v1/currencies/xaf.min.json'];
  (function next(i) {
    if (i >= urls.length || !window.fetch) return;
    fetch(urls[i]).then(res => res.ok ? res.json() : Promise.reject()).then(d => {
      const r = {}; Object.keys(RATES).forEach(k => { if (d.xaf && d.xaf[k] > 0) r[k] = d.xaf[k]; });
      Object.assign(RATES, r); try { localStorage.setItem('mc_fx', JSON.stringify({ t: Date.now(), r })); } catch (e) {}
      render();
    }).catch(() => next(i + 1));
  })(0);
})();