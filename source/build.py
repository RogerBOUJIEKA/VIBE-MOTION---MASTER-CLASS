import json, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SP = HERE + '/data'        # content data: programme, FAQ, marquee, WhatsApp symbol, small scripts
V4 = HERE                  # style.css and app.js live next to this file
REPO = os.path.dirname(HERE)   # the repository root: index.html is written here
HG = HERE + '/icons'       # the Hugeicons used by the site (copied, no npm needed)
EN = {}


def t(k, fr, en):
    EN[k] = en
    return f'data-i18n="{k}">{fr}'


def kebab(s): return re.sub(r'([A-Z])', lambda m: '-' + m.group(1).lower(), s)


def icon(name, cls='hi'):
    src = open(f'{HG}/{name}Icon.js', encoding='utf-8').read()
    out = []
    for tag, attrs in re.findall(r'\["(\w+)", \{(.*?)\}\]', src):
        kv = dict(re.findall(r'(\w+): "([^"]*)"', attrs)); kv.pop('key', None)
        out.append('<' + tag + ' ' + ' '.join(f'{kebab(k)}="{v}"' for k, v in kv.items()) + '/>')
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" aria-hidden="true">{"".join(out)}</svg>'


CTA = 'https://rogerboujieka237.mychariow.shop/prd_9wrq07d2/checkout'
WA_GROUP = 'https://chat.whatsapp.com/HhJZm77fXCd9j9TWNGx7Bk'
WA_DM = 'https://wa.me/237678594247?text=Bonjour%20Roger%2C%20j%27ai%20une%20question%20sur%20la%20formation%20Vibe%20Motion.'
wa_sym = open(f'{SP}/wa.svg').read().strip()
WAI = '<svg class="hi" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>'
marquee = open(f'{SP}/marquee.html', encoding='utf-8').read().strip().replace('<div class="marquee" aria-hidden="true">', '<div class="loop" aria-hidden="true">', 1)
rays = ''.join(f'<line x1="{50+14*math.cos(a):.1f}" y1="{50+14*math.sin(a):.1f}" x2="{50+(46 if i%2==0 else 40)*math.cos(a):.1f}" y2="{50+(46 if i%2==0 else 40)*math.sin(a):.1f}"/>' for i, a in enumerate([k*math.pi/6+0.13 for k in range(12)]))
def spark(cls='spk'): return f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true"><g stroke="currentColor" stroke-width="9" stroke-linecap="round">{rays}</g></svg>'
IZI = '<img src="izivoice-icon.png" alt="" width="20" height="20">'
AR = '<span class="ar">' + icon('ArrowRight01') + '</span>'
CHEV = '<i class="chev" aria-hidden="true">' + icon('ArrowDown01') + '</i>'
def cta(k, fr, en, cls='btn b-red'):
    return f'<a class="{cls} js-cta" href="{CTA}"><span {t(k, fr, en)}</span>{AR}</a>'
PAY = [('img', 'pay/momo.webp', 'MTN MoMo'), ('img', 'pay/wave.webp', 'Wave'), ('moov', 'moov-money.svg', 'Moov Money'), ('img', 'pay/tmoney.webp', 'TMoney'),
       ('om', 'orange-money.svg', 'Orange Money'), ('img', 'pay/celtiis.webp', 'Celtiis Cash'), ('img', 'pay/airtel.webp', 'Airtel Money'), ('img', 'pay/freemoney.webp', 'Free Money'),
       ('mc', 'mastercard.svg', 'Mastercard'), ('visa', 'visa.svg', 'Visa')]
METHODS = '<div class="methods">' + ''.join(f'<span class="pm pm-{k}" title="{a}"><img src="{f}" alt="{a}" width="{48 if k == "img" else 60}" height="{48 if k == "img" else 36}" loading="lazy"></span>' for k, f, a in PAY) + '</div>'

# data reused from the existing content (programme, FAQ, profiles)
src = open(f'{SP}/prog.py', encoding='utf-8').read(); ns = {}; exec(src[src.index('M=['):src.index('\nEN={}')], ns); MODS = ns['M']
b2 = open(f'{SP}/v2_build.py', encoding='utf-8').read()
ns = {}; exec(b2[b2.index('FAQ=['):b2.index('def faq_html')], ns); FAQ = ns['FAQ']
FAQ = [tuple(x.replace('Orange Money, MTN MoMo, Moov Money, Visa ou Mastercard', 'MTN MoMo, Wave, Moov Money, TMoney, Orange Money, Celtiis Cash, Airtel Money, Free Money, Visa ou Mastercard').replace('Orange Money, MTN MoMo, Moov Money, Visa or Mastercard', 'MTN MoMo, Wave, Moov Money, TMoney, Orange Money, Celtiis Cash, Airtel Money, Free Money, Visa or Mastercard') for x in q) for q in FAQ]
ns = {}; exec(b2[b2.index('WHO=['):b2.index('who=[]')], ns); WHO = ns['WHO']
WORKS = [('IHRFvM2n8Ws', 'Spectacle Cabrel Tindo', 'Spot spectacle · motion design', 'Cabrel Tindo show', 'Show ad · motion design'),
         ('4abyQA1a9h8', 'Croisade Bafoussam pour Jésus', 'Événement chrétien · spot complet', 'Bafoussam for Jesus crusade', 'Christian event · full ad'),
         ('IMaHC8wFzuM', 'Pub motion design', 'Publicité · motion design', 'Motion design ad', 'Advertising · motion design'),
         ('U2wMu5KrVnQ', 'Motion design Camair-Co', 'Compagnie aérienne', 'Camair-Co motion design', 'Airline'),
         ('zbV6wVUsFxU', 'Bus gratuits', 'Bafoussam pour Jésus · annonce', 'Free buses', 'Bafoussam for Jesus · announcement'),
         ('oVP2kVm4lMs', 'Grande Nuit de Clôture', 'Bafoussam pour Jésus · invitation', 'Grand Closing Night', 'Bafoussam for Jesus · invitation'),
         ('Web3N01yUVA', 'Motion design App Mr N', 'Application mobile', 'Mr N app motion design', 'Mobile app')]
ROT_FR = ['affiches animées', 'motion designs', 'spots publicitaires', 'vidéos YouTube', 'sites animés', 'invitations']
ROT_EN = ['animated posters', 'motion designs', 'ads', 'YouTube videos', 'animated sites', 'invitations']
TUN_FR = ['Spots publicitaires', 'Motion designs', 'Affiches animées', "Vidéos d'événements", 'Lancements de produit', 'Applications mobiles', 'Vidéos YouTube', 'Statuts WhatsApp']
TUN_EN = ['Advertising spots', 'Motion designs', 'Animated posters', 'Event videos', 'Product launches', 'Mobile apps', 'YouTube videos', 'WhatsApp statuses']
POSTERS = ['work-camairco.jpg', 'motion-kwiva.jpg', 'work-bovann.jpg', 'motion-mboa.jpg', 'motion-volta.jpg', 'motion-snapia.jpg', 'spot-16x9.jpg', 'spot-9x16.jpg']
NAV = [('methode', 'Méthode', 'Method'), ('realisations', 'Réalisations', 'Portfolio'), ('programme', 'Programme', 'Programme'), ('tarif', 'Tarif', 'Pricing'), ('formateur', 'Formateur', 'Trainer'), ('faq', 'FAQ', 'FAQ')]
CHIPS = [('methode', 'Méthode', 'Method'), ('realisations', 'Réalisations', 'Portfolio'), ('calcul', 'Le calcul', 'The maths'), ('programme', 'Programme', 'Programme'), ('tarif', 'Tarif', 'Pricing'), ('formateur', 'Formateur', 'Trainer'), ('communaute', 'Communauté', 'Community'), ('faq', 'FAQ', 'FAQ'), ('contact', 'Contact', 'Contact')]

H = []; A = H.append
A('''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f6f4f1">
<title>Vibe Motion · Créez des vidéos pro avec l'IA · Roger BOUJIEKA</title>
<meta name="description" content="Vibe Motion : la formation de Roger BOUJIEKA pour créer des spots, des motion designs et des affiches animées avec Claude Opus 5.5 et iziVoice, sur smartphone ou ordinateur. 15 vidéos, 14 modules, accès à vie.">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="canonical" href="https://www.rogerboujieka.com/">
<meta property="og:type" content="website"><meta property="og:url" content="https://www.rogerboujieka.com/">
<meta property="og:title" content="Vibe Motion · Créez des vidéos pro avec l'IA">
<meta property="og:description" content="Claude Opus 5.5 monte. iziVoice prête sa voix. Vous dirigez. La formation de Roger BOUJIEKA, sur smartphone ou ordinateur.">
<meta property="og:image" content="https://www.rogerboujieka.com/og-vibe-motion.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="Formation Vibe Motion : créez des vidéos pro avec l'IA, avec Roger BOUJIEKA"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="fr_FR"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://www.rogerboujieka.com/og-vibe-motion.jpg">
<meta name="color-scheme" content="light dark">
<link rel="preload" href="fonts/urbanist.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="roger-v3.webp" as="image">
<script>try{if(localStorage.getItem('mc_theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}catch(e){}</script>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1454801303232892');
fbq('track', 'PageView');
</script>
<!-- End Meta Pixel Code -->
<style>
''' + open(f'{V4}/style.css', encoding='utf-8').read() + '''
</style>
</head>
<body>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id=1454801303232892&ev=PageView&noscript=1"></noscript>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">''' + wa_sym + '''</svg>
''')

# ---------- announcement, header, menu ----------
nav = ''.join(f'<a href="#{k}" class="js-go" data-sec="{k}" {t("n_" + k, fr, en)}</a>' for k, fr, en in NAV)
chips = ''.join(f'<a href="#{k}" class="js-go" data-sec="{k}" {t("c_" + k, fr, en)}</a>' for k, fr, en in CHIPS)
menu = ''.join(f'<a class="it js-go" href="#{k}"><small>{i+1:02d}</small><span {t("c_" + k, fr, en)}</span></a>' for i, (k, fr, en) in enumerate(CHIPS))
A(f'''<a class="ann js-go" href="#tarif"><i></i><span {t("ann", "<em class='pz'>Grande promo −78 %</em> 5 500 FCFA <s class='x2'>25 000</s> <span class='x2'>· se termine dans</span>", "<em class='pz'>Big sale −78%</em> 5,500 FCFA <s class='x2'>25,000</s> <span class='x2'>· ends in</span>")}</span><b class="js-cd-hms">24:00:00</b></a>
<header class="hdr" id="hdr">
  <div class="wrap bar">
    <a class="brand js-go" href="#top" aria-label="Roger BOUJIEKA"><img class="l1" src="logo_rb_dk.png" alt="Roger BOUJIEKA" width="150" height="38"><img class="l2" src="logo_rb.png" alt="" width="150" height="38"></a>
    <nav class="nav" aria-label="Menu">{nav}</nav>
    <div class="grow"></div>
    <div class="seg" role="group" aria-label="Langue / Language"><button id="lang-fr" aria-pressed="true">FR</button><button id="lang-en" aria-pressed="false">EN</button></div>
    <button class="ib thm" id="thm" type="button" aria-label="Mode jour / nuit">{icon("Moon02", "hi m")}{icon("Sun03", "hi s")}</button>
    {cta("cta_top", "Je m'inscris", "Enrol", "btn b-red b-sm")}
    <button class="ib burger" type="button" aria-label="Menu" aria-expanded="false">{icon("Menu01")}</button>
  </div>
  <nav class="chips" aria-label="Accès rapide">{chips}</nav>
  <div class="cbar" id="cbar" hidden><div class="row">{WAI}<span class="tx" {t("cb_t", "<span class='l'>Communauté WhatsApp gratuite <b>LE DIGITAL POUR TOUS</b> : IA, marketing digital, création de contenu et bien plus.</span><span class='s'><b>LE DIGITAL POUR TOUS</b> · communauté gratuite</span>", "<span class='l'>Free WhatsApp community <b>LE DIGITAL POUR TOUS</b>: AI, digital marketing, content creation and more.</span><span class='s'><b>LE DIGITAL POUR TOUS</b> · free community</span>")}</span><a class="go js-lead" href="{WA_GROUP}" target="_blank" rel="noopener" {t("cb_go", "Rejoindre", "Join")}</a><button class="x" type="button" aria-label="Fermer">{icon("Cancel01")}</button></div></div>
</header>
<div class="menu" aria-hidden="true"><div class="mh"><img src="logo_rb_dk.png" alt="Roger BOUJIEKA" style="height:30px;width:auto"><button class="ib" type="button" id="menu-x" aria-label="Fermer">{icon("Cancel01")}</button></div>{menu}{cta("cta_menu", "Rejoindre la formation", "Join the course")}</div>
<main>
''')

# ---------- 1 · hero ----------
rot = '<span class="rot" aria-hidden="true">' + ''.join(f'<span{" class=\"on\"" if i == 0 else ""}>{w}</span>' for i, w in enumerate(ROT_FR)) + '</span>'
bars = ''.join('<i></i>' for _ in range(24))
A(f'''<section class="hero" id="top">
  <div class="hwaves" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="giant" aria-hidden="true">MOTION</div>
  <div class="wrap hgrid">
    <div class="hcopy">
      <span class="lbl" {t("h_lbl", "Formation Vibe Motion", "Vibe Motion course")}</span>
      <h1 class="h1"><span class="l" {t("h1a", "Créez des", "Create")}</span>{rot}<span class="sr js-rot-sr">{ROT_FR[0]}</span><span class="l" {t("h1b", "avec l'IA.", "with AI.")}</span></h1>
      <p class="ld" {t("h_ld", "<b>Claude Opus 5.5</b> monte. <b>iziVoice</b> prête sa voix. Vous dirigez, depuis votre smartphone ou votre ordinateur.", "<b>Claude Opus 5.5</b> edits. <b>iziVoice</b> lends its voice. You direct, from your smartphone or computer.")}</p>
      <div class="acts" id="hero-cta">{cta("cta_hero", "Rejoindre la formation", "Join the course")}<a class="btn b-ghost has-ar js-go" href="#realisations"><span {t("cta_works", "Voir les réalisations", "See the work")}</span><span class="ar">{icon("Play")}</span></a></div>
      <p class="hproof"><span>{icon("CheckmarkCircle02")}<span {t("hp1", "15 vidéos · 14 modules", "15 videos · 14 modules")}</span></span><span>{icon("CheckmarkCircle02")}<span {t("hp2", "Accès à vie", "Lifetime access")}</span></span><span>{icon("CheckmarkCircle02")}<span {t("hp3", "Smartphone ou ordinateur", "Smartphone or computer")}</span></span><span>{icon("CheckmarkCircle02")}<span {t("hp4", "Mobile Money ou carte", "Mobile Money or card")}</span></span></p>
    </div>
    <div class="subject">
      <div class="swaves" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <img src="roger-v3.webp" alt="Roger BOUJIEKA" width="1000" height="1000" fetchpriority="high">
      <span class="badge b1" aria-hidden="true"><i>{spark()}</i>Claude Opus 5.5</span>
      <span class="badge b2" aria-hidden="true"><i>{IZI}</i>iziVoice</span>
      <div class="orbm" aria-hidden="true"><svg class="orbm-t" viewBox="0 0 120 120"><defs><path id="orbmp" d="M60,60 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs><text dominant-baseline="central"><textPath href="#orbmp" textLength="301" lengthAdjust="spacing" {t("orbm", "ACCÈS À VIE – ACCÈS À VIE – ACCÈS À VIE –&#160;", "LIFETIME ACCESS – LIFETIME ACCESS –&#160;")}</textPath></text></svg><span class="orbm-r"></span><span class="orbm-c">{spark("")}</span></div>
    </div>
    <div class="hside">
      <div class="offer-mini"><div class="t"><span {t("om_t", "Grande promo 24 h", "24-hour big sale")}</span><span class="off">−78 %</span></div><div class="p"><b>5 500</b><small>FCFA</small><s>25 000</s></div><div class="cdmini js-cd"><span><b>24</b><small {t("u_h", "H", "H")}</small></span><span><b>00</b><small>MIN</small></span><span><b>00</b><small>SEC</small></span></div></div>
      <div class="aud"><button type="button" class="aud-b js-aud" aria-label="Écouter la présentation"><span class="aud-r r1"></span><span class="aud-r r2"></span><span class="aud-c"><svg class="pl" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg><svg class="pa" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/></svg></span></button><div class="aud-x"><b {t("au_t", "Écoutez avant de décider", "Listen before you decide")}</b><span class="aud-row"><span class="aud-w" aria-hidden="true">{bars}</span><span class="aud-t js-aud-t">1:30</span></span></div><audio class="js-aud-el" preload="none" src="presentation-formation.mp3"></audio></div>
    </div>
    <div class="hvid">
    <div class="hstage">
      <div class="vp" id="vp" data-yt="Ew-ZgqctuxQ" tabindex="0" role="region" aria-label="Présentation de la formation">
        <div class="vp-in">
          <div class="vp-bar3"><i></i><i></i><i></i><span>Vibe Motion · <span {t("vp_t", "Présentation de la formation", "Course presentation")}</span></span><b>HD</b></div>
          <div class="vp-scr">
            <img class="vp-po" src="https://i.ytimg.com/vi/Ew-ZgqctuxQ/maxresdefault.jpg" onerror="if(!this.dataset.f){{this.dataset.f=1;this.src='https://i.ytimg.com/vi/Ew-ZgqctuxQ/hqdefault.jpg'}}" alt="" width="1280" height="720" loading="lazy" decoding="async">
            <div class="vp-host"><div class="vp-slot"></div></div>
            <div class="vp-shield"></div>
            <span class="vp-live"><i></i><span {t("vp_lv", "Aperçu · son coupé", "Preview · muted")}</span></span>
            <span class="vp-flash" aria-hidden="true"></span>
            <i class="vp-ld" aria-hidden="true"></i>
            <button type="button" class="vp-big"><span class="c"><span class="r"></span><span class="r r2"></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg></span><span class="t"><span class="k1" {t("vp_b1", "Regarder la présentation", "Watch the presentation")}</span><span class="k2" {t("vp_b2", "Regarder avec le son", "Watch with sound")}</span></span></button>
            <button type="button" class="vp-snd">{icon("VolumeHigh")}<span {t("vp_snd", "Activer le son", "Turn sound on")}</span></button>
            <div class="vp-end"><h3 {t("vp_eh", "Prêt à créer vos vidéos ?", "Ready to create your videos?")}</h3><p {t("vp_ep", "Grande promo : 5 500 FCFA au lieu de 25 000, accès à vie.", "Big sale: 5,500 FCFA instead of 25,000, lifetime access.")}</p><div class="row">{cta("vp_cta", "Rejoindre la formation", "Join the course")}<button type="button" class="btn vp-again">{icon("Refresh")}<span {t("vp_ag", "Revoir", "Watch again")}</span></button></div></div>
            <div class="vp-ctrl">
              <div class="vp-pg"><div class="tr"><div class="vp-buf"></div><div class="vp-fill"><i></i></div></div><span class="vp-tip">0:00</span></div>
              <div class="vp-row">
                <button type="button" class="vp-pp" aria-label="Lecture / pause">{icon("Play")}</button>
                <button type="button" class="vp-rw" aria-label="Reculer de 10 secondes">{icon("GoBackward10Sec")}</button>
                <button type="button" class="vp-fw" aria-label="Avancer de 10 secondes">{icon("GoForward10Sec")}</button>
                <div class="vp-vol"><button type="button" class="vp-mu" aria-label="Son">{icon("VolumeHigh")}</button><div class="vp-vs" role="slider" aria-label="Volume"><div class="vp-vf"><i></i></div></div></div>
                <span class="vp-tm"><b>0:00</b> / <span>0:00</span></span>
                <button type="button" class="vp-sp" aria-label="Vitesse">1×</button>
                <button type="button" class="vp-fs" aria-label="Plein écran">{icon("FullScreen")}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <span class="badge b1" aria-hidden="true"><i>{spark()}</i>Claude Opus 5.5</span>
      <span class="badge b2" aria-hidden="true"><i>{IZI}</i>iziVoice</span>
    </div>
  </div>
  </div>
  <div class="cue" aria-hidden="true"><i></i><span {t("cue", "Défilez", "Scroll")}</span></div>
</section>
{marquee}
''')

# ---------- 2 · manifesto ----------
A(f'''<section class="mani sec" id="manifeste">
  <div class="wrap">
    <span class="lbl" {t("mf_lbl", "Le manifeste", "The manifesto")}</span>
    <p class="big js-mani" {t("mf_p", "Hier, une vidéo professionnelle exigeait des logiciels hors de prix, un ordinateur puissant et des mois d'apprentissage. Aujourd'hui, vous décrivez votre idée. <em>Claude Opus 5.5</em> monte. <em>iziVoice</em> prête sa voix. Et vous, <em>vous dirigez.</em>", "Yesterday, a professional video meant expensive software, a powerful computer and months of learning. Today, you describe your idea. <em>Claude Opus 5.5</em> edits. <em>iziVoice</em> lends its voice. And you <em>direct.</em>")}</p>
    <div class="sig"><img src="roger-v3.webp" alt="" width="52" height="52" loading="lazy"><span {t("mf_sig", "Roger BOUJIEKA · fondateur de Boujieka Academy", "Roger BOUJIEKA · founder of Boujieka Academy")}</span></div>
  </div>
</section>
''')

# ---------- 3 · method (stacking acts) ----------
ING_FR = ['Objectif', 'Durée', 'Format', 'Couleurs', 'Logo', 'Rythme', 'Voix', 'Musique']
ING_EN = ['Goal', 'Length', 'Format', 'Colours', 'Logo', 'Pace', 'Voice', 'Music']
ing = ''.join(f'<span {t(f"ing{i}", f, e)}</span>' for i, (f, e) in enumerate(zip(ING_FR, ING_EN)))
wave = ''.join(f'<i style="--h:{h}%;animation-delay:-{d:.2f}s"></i>' for h, d in [(30 + (k * 37) % 65, (k * .13) % 1.1) for k in range(40)])
A(f'''<section class="meth sec" id="methode">
  <div class="wrap">
    <div class="sh split"><div><span class="lbl" {t("me_lbl", "La méthode", "The method")}</span><h2 class="t2 bt" style="margin-top:18px" {t("me_h", "Trois actes. <em>Une vidéo pro.</em>", "Three acts. <em>One pro video.</em>")}</h2></div><p class="ld" {t("me_p", "La méthode exacte que j'utilise pour mes clients, découpée en trois gestes simples que vous refaites sur chaque projet.", "The exact method I use for my clients, broken into three simple moves you repeat on every project.")}</p></div>
    <div class="acts3">
      <article class="act" style="--i:0">
        <div><span class="no">01</span><h3 {t("a1h", "Vous décrivez.", "You describe.")}</h3><p {t("a1p", "Vous écrivez, ou dictez au micro, ce que vous voulez. Ma méthode des 8 ingrédients transforme une simple idée en consignes précises. Un lien de site, une affiche ou vos rushs suffisent pour commencer.", "You write, or dictate, what you want. My 8-ingredient method turns a simple idea into precise instructions. A website link, a poster or your footage is enough to start.")}</p>
          <div class="tg"><span>{icon("AiMagic")}<span {t("a1t1", "8 ingrédients", "8 ingredients")}</span></span><span>{icon("Mic01")}<span {t("a1t2", "Dictée au micro", "Voice dictation")}</span></span><span>{icon("Layers01")}<span {t("a1t3", "Modèle de prompt", "Prompt template")}</span></span></div></div>
        <div class="vis js-vis" data-kind="prompt"><div class="bar3"><i></i><i></i><i></i><span>Claude · Code</span></div>
          <div class="prompt"><span class="js-type" data-fr="Crée un spot de 30 secondes pour le site kwiva.cm : couleurs de la marque, logo animé, titres dynamiques, voix off chaleureuse en français, format 9:16." data-en="Create a 30-second ad for the kwiva.cm website: brand colours, animated logo, dynamic titles, a warm French voice-over, 9:16 format."></span><i class="cur"></i></div>
          <div class="ing">{ing}</div><div class="send"><span>{icon("ArrowUpRight01")}<span {t("a1s", "Envoyer à Claude", "Send to Claude")}</span></span></div></div>
      </article>
      <article class="act" style="--i:1">
        <div><span class="no">02</span><h3 {t("a2h", "Claude Opus 5.5 monte.", "Claude Opus 5.5 edits.")}</h3><p {t("a2p", "L'IA construit la vidéo : rythme, titres animés, transitions, logos en mouvement et effets. Vous gardez la main et demandez chaque retouche en une phrase.", "The AI builds the video: pace, animated titles, transitions, moving logos and effects. You stay in control and ask for any change in one sentence.")}</p>
          <div class="tg"><span>{spark()}<span>Claude Opus 5.5</span></span><span>{icon("PaintBrush01")}<span>Motion design</span></span><span>{icon("Refresh")}<span {t("a2t3", "Retouches rapides", "Quick edits")}</span></span></div></div>
        <div class="vis js-vis" data-kind="tl"><div class="bar3"><i></i><i></i><i></i><span>Spot_Kwiva_9x16.mp4</span></div>
          <div class="tlw"><div class="tl"><div class="row r1"><i style="left:2%;width:20%;transition-delay:.1s"></i><i style="left:25%;width:14%;transition-delay:.25s"></i><i style="left:42%;width:26%;transition-delay:.4s"></i><i style="left:72%;width:24%;transition-delay:.55s"></i></div><div class="row r2"><i style="left:0;width:36%;transition-delay:.2s"></i><i style="left:39%;width:30%;transition-delay:.35s"></i><i style="left:72%;width:28%;transition-delay:.5s"></i></div><div class="row r3"><i style="left:3%;width:92%;transition-delay:.3s"></i></div><div class="row r4"><i style="left:10%;width:8%;transition-delay:.45s"></i><i style="left:46%;width:9%;transition-delay:.6s"></i><i style="left:80%;width:10%;transition-delay:.75s"></i></div><span class="ph"></span></div>
          <div class="prog2"><span {t("a2b", "Montage", "Editing")}</span><span class="bb"><i></i></span><span>100 %</span></div></div></div>
      </article>
      <article class="act" style="--i:2">
        <div><span class="no">03</span><h3 {t("a3h", "iziVoice parle. Vous livrez.", "iziVoice speaks. You deliver.")}</h3><p {t("a3p", "Une voix off naturelle, la musique et les sons, puis l'export dans tous les formats : YouTube, Shorts, statuts WhatsApp. La vidéo part chez votre client.", "A natural voice-over, music and sounds, then export in every format: YouTube, Shorts, WhatsApp statuses. The video goes to your client.")}</p>
          <div class="tg"><span>{IZI}<span {t("a3t1", "Voix off iziVoice", "iziVoice voice-over")}</span></span><span>{icon("Youtube")}<span>16:9 · 9:16</span></span><span>{icon("CheckmarkBadge01")}<span {t("a3t3", "Livraison pro", "Pro delivery")}</span></span></div></div>
        <div class="vis js-vis" data-kind="voice"><div class="bar3"><i></i><i></i><i></i><span>iziVoice · français</span></div>
          <div class="wave">{wave}</div>
          <div class="fmt"><span class="f1"><i></i>16:9</span><span class="f2"><i></i>9:16</span><span class="f3"><i></i>WhatsApp</span></div>
          <div class="done">{icon("CheckmarkCircle02")}<span {t("a3d", "Vidéo livrée au client", "Video delivered to the client")}</span></div></div>
      </article>
    </div>
  </div>
</section>
''')

# ---------- 4 · tunnel + works ----------
tw = ''.join(f'<span{" class=\"on\"" if i == 0 else ""}>{w}</span>' for i, w in enumerate(TUN_FR))
A(f'''<section class="tun" id="traversee" data-posters='{json.dumps(POSTERS)}'>
  <div class="stk">
  <div class="fbk" aria-hidden="true">{"".join(f'<img src="{p}" alt="" loading="lazy">' for p in POSTERS)}</div>
  <div class="cv" id="tunnel"></div>
  <div class="ov"><span class="lbl" {t("tu_lbl", "La traversée · tout ce que la méthode permet", "The journey · everything the method makes")}</span>
    <div class="cap"><span class="n js-tn">01 / 08</span><div class="w js-tw">{tw}</div><div class="pbar"><i class="js-tp"></i></div></div></div>
  </div>
</section>
''')
cards = [f'''<button type="button" class="wc wide" data-mp4="spot-16x9.mp4" data-poster="spot-16x9.jpg" data-t="wt0"><span class="th"><img src="spot-16x9.jpg" alt="" loading="lazy" decoding="async"><span class="pl"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg></span></span><span class="cp"><b {t("wt0", "Le spot de la formation", "The course trailer")}</b><span {t("ws0", "Réalisé avec la méthode enseignée · 1:28", "Made with the method taught · 1:28")}</span></span></button>''']
for i, (vid, ft, fs, et, es) in enumerate(WORKS):
    cards.append(f'<button type="button" class="wc" data-yt="{vid}" data-t="wt{i+1}"><span class="th"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" decoding="async"><span class="nw"><i></i><span {t("nw", "Nouveau", "New")}</span></span><span class="pl"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg></span></span><span class="cp"><b {t(f"wt{i+1}", ft, et)}</b><span {t(f"ws{i+1}", fs, es)}</span></span></button>')
cards.append(f'<a class="wc wcta js-cta" href="{CTA}"><span class="th"><b {t("wct_b", "À vous.", "Your turn.")}</b><span class="ar">{icon("ArrowRight01")}</span></span><span class="cp"><b {t("wct_t", "Votre prochaine vidéo", "Your next video")}</b><span {t("wct_s", "Créée avec la méthode Vibe Motion", "Made with the Vibe Motion method")}</span></span></a>')
A(f'''<section class="works sec" id="realisations">
  <div class="wrap">
    <div class="sh split"><div><span class="lbl" {t("wk_lbl", "Réalisations", "Portfolio")}</span><h2 class="t2 bt" style="margin-top:18px" {t("wk_h", "Mes dernières <em>réalisations.</em>", "My latest <em>work.</em>")}</h2></div><p class="ld" {t("wk_p", "Des spots créés pour de vraies marques, des artistes et des événements, avec la méthode que je vous transmets. Touchez une vidéo pour la regarder.", "Ads made for real brands, artists and events, with the method I teach. Tap a video to watch it.")}</p></div>
    <div class="grid">{"".join(cards)}</div>
  </div>
</section>
<div class="lb" id="lb" aria-hidden="true" role="dialog" aria-modal="true">
  <div class="box"><div class="scr"><i class="ld"></i><button type="button" class="snd" {t("lb_snd", "Activer le son", "Tap for sound")}</button></div>
    <div class="meta"><div><b class="js-lbt"></b><span class="js-lbs"></span></div><button type="button" class="ib cls" aria-label="Fermer">{icon("Cancel01")}</button></div></div>
</div>
''')

# ---------- 5 · economy ----------
MX = [('CreditCard', 'Logiciels', 'Software', '≈&nbsp;41&nbsp;000&nbsp;FCFA&nbsp;/&nbsp;mois', '≈&nbsp;41,000&nbsp;FCFA&nbsp;/&nbsp;mo', '≈&nbsp;12&nbsp;000&nbsp;FCFA&nbsp;/&nbsp;mois', '≈&nbsp;12,000&nbsp;FCFA&nbsp;/&nbsp;mo'),
      ('SmartPhone01', 'Matériel', 'Hardware', 'Ordinateur puissant', 'Powerful computer', 'Téléphone ou PC', 'Phone or PC'),
      ('Clock01', 'Un spot de 90 s', 'A 90-second ad', '≈&nbsp;4&nbsp;heures', '≈&nbsp;4&nbsp;hours', '≈&nbsp;24&nbsp;minutes', '≈&nbsp;24&nbsp;minutes'),
      ('Mortarboard01', 'Apprentissage', 'Learning', 'Des mois', 'Months', '1&nbsp;h&nbsp;14 de formation', '1&nbsp;h&nbsp;14 of training'),
      ('Mic01', 'Voix off', 'Voice-over', 'À enregistrer soi-même', 'Record it yourself', 'Incluse avec iziVoice', 'Included with iziVoice')]
mx = ''.join(f'<div><span>{icon(ic)}<span {t(f"mx{i}", fl, el)}</span></span><b><span class="c" {t(f"mxc{i}", fc, ec)}</span><span class="a" {t(f"mxa{i}", fa, ea)}</span></b></div>' for i, (ic, fl, el, fc, ec, fa, ea) in enumerate(MX))
A(f'''<section class="eco sec" id="calcul" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap">
    <div class="sh split"><div><span class="lbl" {t("ec_lbl", "Le calcul", "The maths")}</span><h2 class="t2 bt" style="margin-top:18px" {t("ec_h", "Le studio complet <em>pour 12&nbsp;000&nbsp;FCFA par mois.</em>", "The whole studio <em>for 12,000&nbsp;FCFA a month.</em>")}</h2></div><p class="ld" {t("ec_p", "Après la formation, un seul abonnement suffit pour créer : <b>Claude Pro</b>. Comparez avec les logiciels classiques, puis calculez ce que vos vidéos peuvent vous rapporter.", "After the course, one plan is all you need to create: <b>Claude Pro</b>. Compare it with classic software, then work out what your videos could earn you.")}</p></div>
    <div class="grid2">
      <div class="cmp" id="cmp">
        <div class="sw"><span class="pill"></span><button type="button" data-m="c" aria-pressed="true" {t("sw_c", "Montage classique", "Classic editing")}</button><button type="button" data-m="a" aria-pressed="false" {t("sw_a", "Avec Vibe Motion", "With Vibe Motion")}</button></div>
        <div class="apps"><span class="c1"><i class="ps">Ps</i><i class="pr">Pr</i><i class="ae">Ae</i></span><i class="cl c2">{spark("")}</i><i class="iz c2">{IZI}</i><b><span class="c" {t("ap_c", "Photoshop, Premiere, After Effects", "Photoshop, Premiere, After Effects")}</span><span class="a">Claude Opus 5.5 + iziVoice</span></b></div>
        <div class="mx">{mx}</div>
        <div class="tbar"><div class="r"><span {t("tb_l", "Temps pour un spot", "Time for one ad")}</span><b><span class="c">100 %</span><span class="a">10 %</span></b></div><div class="bb"><i></i></div></div>
        <p class="note" {t("cm_n", "Durées indicatives. Adobe Creative Cloud Pro : 69,99 $/mois ; Claude Pro : 20 $/mois. Prix variables selon le pays.", "Indicative times. Adobe Creative Cloud Pro: $69.99/month; Claude Pro: $20/month. Prices vary by country.")}</p>
      </div>
      <div class="calc" id="roi">
        <h3 {t("ro_ch", "Ce que vos vidéos peuvent rapporter", "What your videos could earn")}</h3><p class="sub" {t("ro_sub", "Choisissez un rythme et un prix : le calcul se fait en direct.", "Pick a pace and a price: the maths runs live.")}</p>
        <div class="ctl"><div class="r"><span {t("ro_n", "Vidéos livrées par mois", "Videos delivered per month")}</span><b class="js-rn">4</b></div><input type="range" min="1" max="20" value="4" class="js-rr" aria-label="Vidéos par mois"></div>
        <div class="ctl"><div class="r"><span {t("ro_pp", "Prix d'une vidéo (FCFA)", "Price per video (FCFA)")}</span></div>
          <div class="js-seg"><button type="button" data-p="15000" aria-pressed="false">15&nbsp;000<small {t("ro_s1", "affiche animée", "animated poster")}</small></button><button type="button" data-p="25000" aria-pressed="false">25&nbsp;000<small {t("ro_s2", "statut", "status")}</small></button><button type="button" data-p="50000" aria-pressed="true">50&nbsp;000<small {t("ro_s3", "spot motion", "motion ad")}</small></button><button type="button" data-p="150000" aria-pressed="false">150&nbsp;000<small {t("ro_s4", "spot pro", "pro ad")}</small></button></div></div>
        <div class="bars"><div class="cost"><div class="bl"><span {t("ro_b1", "Abonnement Claude", "Claude plan")}</span><b>12&nbsp;000&nbsp;FCFA</b></div><div class="tr"><i class="js-bc"></i></div></div>
          <div class="gain"><div class="bl"><span {t("ro_b2", "Ce que vous facturez", "What you bill")}</span><b class="js-bg">200&nbsp;000&nbsp;FCFA</b></div><div class="tr"><i class="js-bgb"></i></div></div></div>
        <div class="res"><div><span class="big js-rv">0</span><small><span {t("ro_r", "FCFA par mois · ", "FCFA a month · ")}</span><span class="js-rc">4</span> <span {t("ro_rc", "clients livrés", "clients served")}</span></small></div><div class="x"><span class="js-rx">16×</span><small {t("ro_x", "l'abonnement", "the plan")}</small></div></div>
        <p class="rn" {t("ro_note", "Exemple indicatif avec des prix couramment pratiqués. Vos revenus dépendent de vos clients et de votre travail. Les limites d'utilisation de Claude sont fixées par Anthropic.", "Indicative example using common prices. Your income depends on your clients and your work. Claude's usage limits are set by Anthropic.")}</p>
      </div>
    </div>
    <div class="plan"><span class="si">{spark()}</span><p {t("pl_p", "<b>À prévoir après la formation :</b> l'abonnement Claude Pro, mensuel et sans engagement. Je vous montre comment le prendre au module 4, même par Mobile Money.", "<b>Plan for after the course:</b> the Claude Pro plan, monthly, cancel anytime. Module 4 shows you how to get it, even with Mobile Money.")}</p><span class="am">≈&nbsp;12&nbsp;000 <small {t("pl_m", "FCFA / mois · 20 $", "FCFA / month · $20")}</small></span></div>
  </div>
</section>
''')

# ---------- 6 · skills ----------
SK = [('Link01', 'Modules 8 · 9', 'Un spot à partir d’un lien', 'A spot from a single link', "Donnez l'adresse d'un site : Claude l'analyse et construit une vidéo aux couleurs de la marque.", "Give a website address: Claude analyses it and builds a video in the brand's colours."),
      ('Image01', 'Module 10', 'Des affiches qui prennent vie', 'Posters that come alive', "Concerts, conférences, croisades, promotions : l'affiche devient une vidéo pour les statuts.", 'Concerts, conferences, crusades, promotions: the poster becomes a video for statuses.'),
      ('Mic01', 'Module 7', 'Des voix off naturelles', 'Natural voice-overs', 'Voix, accents, musique et effets sonores avec iziVoice, directement depuis Claude.', 'Voices, accents, music and sound effects with iziVoice, right from Claude.'),
      ('Film01', 'Module 11', 'Des vidéos longues', 'Long videos', 'Mariages, anniversaires, YouTube : Claude place vos rushs au bon endroit.', 'Weddings, birthdays, YouTube: Claude places your footage in the right spot.'),
      ('Layers01', 'Module 12', 'Tous les formats', 'Every format', '16:9 pour YouTube, 9:16 pour les Shorts et les statuts, livrés en une fois.', '16:9 for YouTube, 9:16 for Shorts and statuses, delivered in one go.'),
      ('Money03', 'Module 14', 'Vendre vos vidéos', 'Sell your videos', 'Quoi proposer, à quel prix, et comment trouver vos premiers clients.', 'What to offer, at what price, and how to find your first clients.')]
# bento order on three columns: wide + small / small + wide / wide + small; wide cards carry a real poster
SK_ORDER = [(0, 'motion-kwiva.jpg'), (2, None), (3, None), (1, 'motion-volta.jpg'), (5, 'motion-mboa.jpg'), (4, None)]
sk = ''
for i, img in SK_ORDER:
    ic, md, fh, eh, fp, ep = SK[i]
    body = f'<span class="ic">{icon(ic)}</span><span class="md">{md}</span><h3 {t(f"sk{i}h", fh, eh)}</h3><p {t(f"sk{i}p", fp, ep)}</p>'
    sk += (f'<article class="bx w rv"><div class="tx">{body}</div><div class="im"><img src="{img}" alt="" width="960" height="540" loading="lazy" decoding="async"></div></article>' if img
           else f'<article class="bx rv">{body}</article>')
A(f'''<section class="sec" id="competences" style="padding-top:0">
  <div class="wrap">
    <div class="sh c"><span class="lbl c" {t("sk_lbl", "Compétences", "Skills")}</span><h2 class="t2 bt" {t("sk_h", "Ce que vous saurez <em>faire.</em>", "What you will be able <em>to do.</em>")}</h2></div>
    <div class="bento">{sk}</div>
  </div>
</section>
''')

# ---------- 7 · programme (chapters) ----------
CH = [(0, 6, 'Préparer', 'Prepare', 'Installer Claude, l’extension Chrome, votre compte Pro et le dossier qui guide l’IA.', 'Install Claude, the Chrome extension, your Pro account and the folder that guides the AI.'),
      (6, 8, 'Diriger l’IA', 'Direct the AI', 'Le prompt qui donne le bon résultat, et la voix off avec iziVoice.', 'The prompt that gets the right result, and voice-over with iziVoice.'),
      (8, 12, 'Créer', 'Create', 'Le cas pratique en direct, le motion à partir d’un lien, les affiches animées et les vidéos longues.', 'The live case study, motion from a link, animated posters and long videos.'),
      (12, 15, 'Livrer et vendre', 'Deliver and sell', 'Retouches et livraison, inspiration, puis vos premiers clients.', 'Edits and delivery, inspiration, then your first clients.')]
flagFR = {'key': 'Essentiel', 'live': 'Cas pratique', 'money': 'Revenus'}; flagEN = {'key': 'Key', 'live': 'Case study', 'money': 'Income'}
tabs = ''; pans = ''
for ci, (a, b, fr, en, dfr, den) in enumerate(CH):
    rng = f'{MODS[a][0]} — {MODS[b-1][0]}'
    tabs += f'<button type="button" class="ctab" role="tab" aria-selected="{"true" if ci == 0 else "false"}" data-ch="{ci}"><small {t(f"chk{ci}", f"Chapitre {ci+1} · modules {rng}", f"Chapter {ci+1} · modules {rng}")}</small><b {t(f"chb{ci}", fr, en)}</b><span {t(f"chd{ci}", dfr, den)}</span></button>'
    mods = ''
    for i in range(a, b):
        n, d, ft, fs, fd, et, es, ed, fl = MODS[i]
        badge = f'<span class="f {fl}" {t("pf_" + fl, flagFR[fl], flagEN[fl])}</span>' if fl else ''
        mods += f'<details class="mod"><summary><span class="n">{n}</span><span class="b"><b><span {t(f"m{i}t", ft, et)}</span>{badge}</b><span {t(f"m{i}s", fs, es)}</span></span><span class="d">{d}</span>{CHEV}</summary><p {t(f"m{i}d", fd, ed)}</p></details>'
    pans += f'<div class="cpan{" on" if ci == 0 else ""}" data-ch="{ci}" role="tabpanel">{mods}</div>'
KP = [('Video01', '15', 'vidéos', 'videos'), ('Layers01', '14', 'modules', 'modules'), ('Clock01', '1 h 14', 'de formation', 'of training'), ('InfinityCircle', '∞', 'accès à vie', 'lifetime access')]
kp = ''.join(f'<div class="rv"><span class="ic">{icon(ic)}</span><span><b>{v}</b><span {t(f"kp{i}", fr, en)}</span></span></div>' for i, (ic, v, fr, en) in enumerate(KP))
NEED = [('SmartPhone01', 'Un smartphone ou un ordinateur', 'A smartphone or a computer'), ('Wifi01', 'Une bonne connexion', 'A good connection'), ('Google', 'Un compte Google', 'A Google account'), ('Chrome', 'Google Chrome', 'Google Chrome')]
need = ''.join(f'<span>{icon(ic)}<span {t(f"nd{i}", fr, en)}</span></span>' for i, (ic, fr, en) in enumerate(NEED))
A(f'''<section class="prg sec" id="programme">
  <div class="wrap">
    <div class="sh split"><div><span class="lbl" {t("pg_lbl", "Programme", "Programme")}</span><h2 class="t2 bt" style="margin-top:18px" {t("pg_h", "15 vidéos. <em>4 chapitres.</em>", "15 videos. <em>4 chapters.</em>")}</h2></div><p class="ld" {t("pg_p", "De l'installation jusqu'à vos premiers clients, dans le bon ordre. Choisissez un chapitre, puis touchez un module pour voir son contenu.", "From setup to your first clients, in the right order. Pick a chapter, then tap a module to see what's inside.")}</p></div>
    <div class="kpis">{kp}</div>
    <div class="chap"><div class="ctabs" role="tablist">{tabs}</div><div class="cpans">{pans}<div class="need"><h4 {t("nd_h", "Ce dont vous avez besoin", "What you need")}</h4>{need}<p {t("nd_p", "Pour les vidéos longues avec beaucoup de rushs, l'ordinateur est plus confortable.", "For long videos with lots of footage, a computer is more comfortable.")}</p></div></div></div>
  </div>
</section>
''')

# ---------- 8 · who ----------
WHO_IC = ['Briefcase01', 'Church', 'Megaphone01', 'Youtube', 'PaintBrush01', 'Mortarboard01']
pills = ''; wp = ''
for i, (e, ft, fd, fl, et, ed, el) in enumerate(WHO):
    pills += f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-w="{i}">{icon(WHO_IC[i])}<span {t(f"wh{i}t", ft, et)}</span></button>'
    EN[f'wh{i}l'] = ''.join(f'<li>{icon("CheckmarkCircle02")}<span>{x}</span></li>' for x in el)
    wp += f'<div class="wpan{" on" if i == 0 else ""}" data-w="{i}"><div><h3 {t(f"whh{i}", ft, et)}</h3><p {t(f"wh{i}d", fd, ed)}</p></div><ul data-i18n="wh{i}l">' + ''.join(f'<li>{icon("CheckmarkCircle02")}<span>{x}</span></li>' for x in fl) + '</ul></div>'
A(f'''<section class="who sec" id="pour-qui" style="padding-bottom:clamp(60px,8vw,110px)">
  <div class="wrap">
    <div class="sh c"><span class="lbl c" {t("wh_lbl", "Pour qui ?", "Who is it for?")}</span><h2 class="t2 bt" {t("wh_h", "Faite pour <em>vous</em> si vous êtes…", "Made for <em>you</em> if you are…")}</h2></div>
    <div class="pills">{pills}</div>{wp}
  </div>
</section>
''')

# ---------- 9 · trainer ----------
ROLES = [('AiMagic', 'Intelligence artificielle', 'Artificial intelligence'), ('Film01', 'Montage vidéo', 'Video editing'), ('PaintBrush01', 'Motion design', 'Motion design'), ('Megaphone01', 'Marketing digital', 'Digital marketing')]
A(f'''<section class="trn sec" id="formateur">
  <div class="wrap">
    <div class="frame rv"><div class="por"><span class="rg"></span><span class="rg"></span><span class="rg"></span><img class="ph" src="roger-v3.webp" alt="Roger BOUJIEKA" width="1000" height="1000" loading="lazy" decoding="async"><span class="badge b1" aria-hidden="true"><i>{spark()}</i>Claude Opus 5.5</span><span class="badge b2" aria-hidden="true"><i>{IZI}</i>iziVoice</span></div></div>
    <div>
      <span class="lbl" {t("tr_lbl", "Le formateur", "The trainer")}</span>
      <h2 class="name bt">Roger <em>BOUJIEKA</em></h2>
      <p class="ld rv" {t("tr_p", "Entrepreneur web, expert en intelligence artificielle, en montage vidéo, en motion design et en marketing digital. Je crée chaque jour des vidéos et des campagnes pour des marques, des entreprises et des églises, et je vous transmets exactement ce qui marche.", "Web entrepreneur, expert in artificial intelligence, video editing, motion design and digital marketing. Every day I create videos and campaigns for brands, companies and churches, and I pass on exactly what works.")}</p>
      <div class="roles rv">{"".join(f'<span>{icon(ic)}<span {t(f"r{k}", fr, en)}</span></span>' for k, (ic, fr, en) in enumerate(ROLES))}</div>
      <div class="cos rv"><div><small {t("ceo", "PDG", "CEO")}</small>Boujieka Group</div><div><small {t("ceo", "PDG", "CEO")}</small>Boujieka Agency</div><div><small {t("ceo", "PDG", "CEO")}</small>Boujieka Academy</div></div>
      <p class="quote rv" {t("tr_q", "« Responsable, et enfant de Dieu. »", "“Responsible, and a child of God.”")}</p>
    </div>
  </div>
</section>
''')

# ---------- 10 · pricing ----------
INC = [("<b>La formation complète</b> : 15 vidéos, 14 modules, 1 h 14", "<b>The full course</b>: 15 videos, 14 modules, 1 h 14"),
       ("À suivre sur <b>smartphone ou ordinateur</b>", "Follow it on a <b>smartphone or a computer</b>"),
       ("Le <b>cas pratique en direct</b> d'une vidéo motion de A à Z", "The <b>live case study</b> of a motion video from A to Z"),
       ("Mon <b>modèle de prompt</b> et ma méthode des 8 ingrédients", "My <b>prompt template</b> and 8-ingredient method"),
       ("Le <b>module monétisation</b> : offres, prix, premiers clients", "The <b>monetisation module</b>: offers, prices, first clients"),
       ("Le <b>PDF</b> des présentations et les ressources", "The slides <b>PDF</b> and resources"),
       ("Un <b>accès immédiat</b> juste après le paiement", "<b>Instant access</b> right after payment")]
CI = icon("CheckmarkCircle02")
EN['inc_l'] = ''.join(f'<li>{CI}<span>{en}</span></li>' for fr, en in INC)
G = [('InfinityCircle', 'Accès à vie', 'Lifetime access', 'Payez une fois, gardez tout.', 'Pay once, keep everything.'),
     ('Refresh', 'Mises à jour offertes', 'Free updates', 'Chaque nouvelle méthode incluse.', 'Every new method included.'),
     ('UserGroup', 'Accompagnement', 'Support', 'Groupe WhatsApp privé.', 'Private WhatsApp group.')]
gs = ''.join(f'<div>{icon(ic)}<b {t(f"g{k}h", fh, eh)}</b><span {t(f"g{k}p", fp, ep)}</span></div>' for k, (ic, fh, eh, fp, ep) in enumerate(G))
A(f'''<section class="prc sec" id="tarif">
  <div class="wrap">
    <div class="sh c"><span class="lbl c" {t("pr_lbl", "Tarif", "Pricing")}</span><h2 class="t2 bt" {t("pr_h", "Une formation. Un paiement. <em>À vie.</em>", "One course. One payment. <em>For life.</em>")}</h2></div>
    <div class="card rv" id="pcard">
      <div class="lft"><h3 {t("inc_h", "Ce que vous recevez", "What you get")}</h3><ul class="inc" data-i18n="inc_l">{"".join(f'<li>{CI}<span>{fr}</span></li>' for fr, en in INC)}</ul><div class="guar">{gs}</div></div>
      <div class="rgt">
        <div class="t"><span {t("pr_tag", "Grande promo · 24 h", "Big sale · 24 h")}</span><span class="off">−78 %</span></div>
        <div class="pr"><b>5 500</b><small>FCFA</small><span class="was" {t("pr_was", "au lieu de <s>25 000 FCFA</s>", "instead of <s>25,000 FCFA</s>")}</span></div>
        <p class="save" {t("pr_save", "Vous économisez 19 500 FCFA aujourd'hui", "You save 19,500 FCFA today")}</p>
        <p class="once" {t("pc_once", "Paiement unique · accès à vie · sans abonnement", "One-time payment · lifetime access · no subscription")}</p>
        <div class="cdb" role="timer"><div class="l"><i></i><span {t("cd_l", "La grande promo se termine dans", "The big sale ends in")}</span></div><div class="js-cd"><div class="u"><b>24</b><small {t("cd_h", "HEURES", "HOURS")}</small></div><span class="sep">:</span><div class="u"><b>00</b><small>MINUTES</small></div><span class="sep">:</span><div class="u"><b>00</b><small {t("cd_s", "SECONDES", "SECONDS")}</small></div></div><div class="pb"><i class="js-cd-bar"></i></div></div>
        {cta("pc_cta", "Rejoindre la formation", "Join the course")}
        <p class="safe" {t("pc_safe", "Paiement sécurisé · accès immédiat", "Secure payment · instant access")}</p>
        {METHODS}
        <div class="fxbox"><span class="js-fx2"></span><label class="fxsel"><span {t("fx_lbl", "Voir dans votre devise :", "See it in your currency:")}</span><select id="fx-cur"></select></label><small class="fxnote" hidden {t("fx_note", "Montant indicatif. Le paiement se fait en FCFA.", "Indicative amount. Payment is made in FCFA.")}</small><span class="js-fx" hidden></span></div>
      </div>
    </div>
    <p class="nt" {t("pr_nt", "Pour créer après la formation, prévoyez l'abonnement Claude Pro (≈ 12&nbsp;000&nbsp;FCFA/mois). <a class='js-go' href='#calcul'>Voir le calcul</a>", "To create after the course, plan for the Claude Pro plan (≈ 12,000&nbsp;FCFA/month). <a class='js-go' href='#calcul'>See the maths</a>")}</p>
  </div>
</section>
''')

# ---------- 11 · community ----------
A(f'''<section id="communaute" style="padding-bottom:clamp(60px,8vw,110px)">
  <div class="wrap"><div class="comm rv">
    <span class="big"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg></span>
    <div><h2 {t("cm_h", "Rejoignez la communauté gratuite", "Join the free community")}</h2><p {t("cm_p", "<b>LE DIGITAL POUR TOUS</b> : un groupe WhatsApp gratuit pour apprendre l'IA, le marketing digital et la création de contenu avec d'autres passionnés.", "<b>LE DIGITAL POUR TOUS</b>: a free WhatsApp group to learn AI, digital marketing and content creation with other enthusiasts.")}</p></div>
    <a class="btn b-green js-lead" href="{WA_GROUP}" target="_blank" rel="noopener">{WAI}<span {t("cm_b", "Rejoindre gratuitement", "Join for free")}</span></a>
  </div></div>
</section>
''')

# ---------- 12 · FAQ ----------
faq = ''.join(f'<details{" open" if i == 0 else ""}><summary><span {t(f"fq{i}q", fq, eq)}</span>{CHEV}</summary><p {t(f"fq{i}a", fa, ea)}</p></details>' for i, (fq, fa, eq, ea) in enumerate(FAQ))
A(f'''<section class="sec" id="faq" style="padding-top:0">
  <div class="wrap faqg">
    <div class="side"><span class="lbl" {t("fq_lbl", "FAQ", "FAQ")}</span><h2 class="t2 bt" style="margin-top:18px" {t("fq_h", "Vos questions, <em>mes réponses.</em>", "Your questions, <em>my answers.</em>")}</h2><p class="ld" style="margin-top:18px" {t("fq_p", "Une autre question ? Écrivez-moi directement, je vous réponds.", "Another question? Message me directly, I'll answer.")}</p><a class="btn b-green js-wa" href="{WA_DM}" target="_blank" rel="noopener">{WAI}<span {t("fq_b", "Poser ma question", "Ask my question")}</span></a></div>
    <div class="faq">{faq}</div>
  </div>
</section>
</main>
''')

# ---------- 13 · footer ----------
L1 = [('methode', 'La méthode', 'The method'), ('realisations', 'Réalisations', 'Portfolio'), ('programme', 'Programme', 'Programme'), ('tarif', 'Tarif', 'Pricing'), ('formateur', 'Le formateur', 'The trainer')]
L2 = [('calcul', 'Le calcul', 'The maths'), ('competences', 'Compétences', 'Skills'), ('pour-qui', 'Pour qui ?', 'Who is it for?'), ('faq', 'FAQ', 'FAQ')]
l1 = ''.join(f'<li><a class="js-go" href="#{k}" {t("f1_" + k.replace("-", "_"), fr, en)}</a></li>' for k, fr, en in L1)
l2 = ''.join(f'<li><a class="js-go" href="#{k}" {t("f2_" + k.replace("-", "_"), fr, en)}</a></li>' for k, fr, en in L2) + f'<li><a class="js-lead" href="{WA_GROUP}" target="_blank" rel="noopener" {t("f_grp", "Communauté gratuite", "Free community")}</a></li>'
A(f'''<footer class="ft" id="contact">
  <div class="fc"><div class="tx"><h2 {t("fc_h", "Votre prochaine vidéo commence ici.", "Your next video starts here.")}</h2><p {t("fc_p", "Rejoignez Vibe Motion : accès immédiat, accès à&nbsp;vie, mises à&nbsp;jour offertes et accompagnement WhatsApp.", "Join Vibe Motion: instant access, lifetime access, free updates and WhatsApp support.")}</p>{cta("fc_cta", "Rejoindre la formation", "Join the course", "btn")}<p class="mini"><span {t("fc_mini", "L'offre se termine dans", "Offer ends in")}</span> <b class="js-cd-hms">24:00:00</b></p></div>
    <img class="ph" src="roger-v3.webp" alt="" width="1000" height="1000" loading="lazy" decoding="async">
    <div class="orb" aria-hidden="true">
      <svg class="orb-t" viewBox="0 0 300 300"><defs><path id="orbp" d="M150,150 m-128,0 a128,128 0 1,1 256,0 a128,128 0 1,1 -256,0"/></defs><text><textPath href="#orbp" textLength="800" lengthAdjust="spacing" {t("orb", "VIBE MOTION · CLAUDE OPUS 5.5 · IZIVOICE · ACCÈS À VIE · MISES À JOUR OFFERTES ·", "VIBE MOTION · CLAUDE OPUS 5.5 · IZIVOICE · LIFETIME ACCESS · FREE UPDATES ·")}</textPath></text></svg>
      <div class="orb-r"><i class="o1">{IZI}</i><i class="o2">{icon("Play")}</i><i class="o3">{icon("Film01")}</i></div>
      <div class="orb-c"><span class="orb-h"></span><span class="orb-h h2"></span><span class="orb-l">{spark("")}</span></div>
    </div></div>
  <div class="fb">
    <div><a class="lg js-go" href="#top"><img class="l1" src="logo_rb_dk.png" alt="Roger BOUJIEKA" loading="lazy"><img class="l2" src="logo_rb.png" alt="" loading="lazy"></a><p class="d" {t("ft_p", "Vibe Motion : la formation de Roger BOUJIEKA pour créer des spots, des motion designs et des affiches animées avec l'intelligence artificielle.", "Vibe Motion: Roger BOUJIEKA's course for creating ads, motion designs and animated posters with artificial intelligence.")}</p></div>
    <div><h4 {t("fh1", "La formation", "The course")}</h4><ul>{l1}</ul></div>
    <div><h4 {t("fh2", "Ressources", "Resources")}</h4><ul>{l2}</ul></div>
    <div><h4 {t("fh3", "Contact", "Contact")}</h4><ul class="ct">
      <li><a class="js-wa" href="{WA_DM}" target="_blank" rel="noopener"><span class="i" style="background:#25d366">{WAI}</span><span>WhatsApp<small {t("fc1", "Réponse rapide", "Quick reply")}</small></span></a></li>
      <li><a href="mailto:rogerboujieka237@gmail.com"><span class="i" style="background:#3d8bfd">{icon("Mail01")}</span><span>E-mail<small {t("fc2", "Écrivez-moi", "Write to me")}</small></span></a></li>
      <li><a href="tel:+237678594247"><span class="i" style="background:var(--red)">{icon("Call02")}</span><span><span {t("fc3", "Appeler", "Call")}</span><small {t("fc3s", "Téléphone", "Phone")}</small></span></a></li>
    </ul></div>
    <div class="fbar"><div><span class="pl" {t("fpay", "Paiement sécurisé", "Secure payment")}</span>{METHODS}</div><div><span class="pl" {t("fpa", "Partenaires", "Partners")}</span><div class="pts"><img class="l1" src="logo_transmission_dk.png" alt="TRANSMISSION" loading="lazy" style="height:34px"><img class="l2" src="logo_transmission.png" alt="" loading="lazy" style="height:34px"><img class="l1" src="logo_boujieka_agency_dk.png" alt="Boujieka Agency" loading="lazy"><img class="l2" src="logo_boujieka_agency.png" alt="" loading="lazy"><img class="l1" src="logo_izivoice_darktext.png" alt="iziVoice" loading="lazy"><img class="l2" src="logo_izivoice.png" alt="" loading="lazy"></div></div></div>
    <p class="legal"><span>© 2026 Roger BOUJIEKA · Boujieka Academy</span><span {t("legal", "Claude et Opus sont des marques d'Anthropic ; formation indépendante, non affiliée à Anthropic.", "Claude and Opus are trademarks of Anthropic; independent course, not affiliated with Anthropic.")}</span></p>
    <span class="band" aria-hidden="true"></span>
  </div>
</footer>
<div class="mbar" id="mbar"><div class="p"><span class="pr">5 500 FCFA<small class="js-cd-hms">24:00:00</small></span><small {t("mb_s", "<b class='pz2'>−78 %</b> au lieu de 25 000 FCFA", "<b class='pz2'>−78%</b> instead of 25,000 FCFA")}</small></div>{cta("mb_cta", "Je m'inscris", "Enrol now")}</div>
<a class="waf js-wa" href="{WA_DM}" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg></a>
<div class="co" id="co" role="dialog" aria-modal="true" aria-labelledby="co-h" hidden>
  <form class="co-box" novalidate>
    <button type="button" class="ib co-x" aria-label="Fermer">{icon("Cancel01")}</button>
    <div class="co-top"><span class="off">−78 %</span><span class="co-pr"><b>5 500</b> FCFA <s>25 000</s></span></div>
    <h3 id="co-h" {t("co_h", "Plus qu'une étape.", "One last step.")}</h3>
    <p class="co-p" {t("co_p", "Vos informations servent à vous envoyer votre accès à la formation.", "We use your details to send you access to the course.")}</p>
    <div class="co-2"><label><span {t("co_fn", "Prénom", "First name")}</span><input name="firstName" autocomplete="given-name" required maxlength="60"></label><label><span {t("co_ln", "Nom", "Last name")}</span><input name="lastName" autocomplete="family-name" required maxlength="60"></label></div>
    <label><span {t("co_em", "E-mail", "Email")}</span><input name="email" type="email" inputmode="email" autocomplete="email" required maxlength="120"></label>
    <label><span {t("co_ph", "WhatsApp (facultatif)", "WhatsApp (optional)")}</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" maxlength="24" placeholder="+237 6XX XX XX XX"></label>
    <p class="co-err" role="alert" hidden></p>
    <button type="submit" class="btn b-red co-go"><span {t("co_go", "Continuer vers le paiement", "Continue to payment")}</span>{AR}</button>
    <p class="co-safe">{icon("SecurityLock")}<span {t("co_safe", "Paiement sécurisé · Mobile Money ou carte", "Secure payment · Mobile Money or card")}</span></p>
    {METHODS}
  </form>
</div>
<div class="co ty" id="ty" role="dialog" aria-modal="true" aria-labelledby="ty-h" hidden>
  <div class="co-box">
    <button type="button" class="ib co-x" aria-label="Fermer">{icon("Cancel01")}</button>
    <div class="ty-ic">{icon("CheckmarkCircle02")}</div>
    <h3 id="ty-h"></h3>
    <p class="co-p ty-p"></p>
    <a class="btn b-red ty-go" href="#" target="_blank" rel="noopener" hidden><span {t("ty_go", "Accéder à ma formation", "Open my course")}</span>{AR}</a>
    <a class="btn b-green ty-grp" href="#" target="_blank" rel="noopener" hidden>{WAI}<span {t("ty_grp", "Rejoindre le groupe des élèves", "Join the students' group")}</span></a>
    <button type="button" class="btn b-red ty-re" hidden><span {t("ty_re", "Vérifier à nouveau", "Check again")}</span>{AR}</button>
    <a class="btn b-green ty-wa js-wa" href="{WA_DM}" target="_blank" rel="noopener">{WAI}<span {t("ty_wa", "Besoin d'aide ? WhatsApp", "Need help? WhatsApp")}</span></a>
  </div>
</div>
<div class="pp" id="pp" role="dialog" aria-modal="false" aria-labelledby="pp-h" hidden>
  <div class="pp-box">
    <button type="button" class="pp-x" aria-label="Fermer">{icon("Cancel01")}</button>
    <span class="pp-tag"><i></i><span {t("pp_tag", "Grande promo", "Big sale")}</span></span>
    <div class="pp-off">−78<small>%</small></div>
    <h3 id="pp-h" {t("pp_h", "Vibe Motion à 5 500 FCFA", "Vibe Motion for 5,500 FCFA")}</h3>
    <p class="pp-p" {t("pp_p", "au lieu de <s>25 000 FCFA</s> · accès à vie", "instead of <s>25,000 FCFA</s> · lifetime access")}</p>
    <div class="pp-cd"><span {t("pp_cd", "Se termine dans", "Ends in")}</span><b class="js-cd-hms">24:00:00</b></div>
    {cta("pp_cta", "J'en profite maintenant", "Grab it now")}
    <button type="button" class="pp-later" {t("pp_later", "Continuer la lecture", "Keep reading")}</button>
  </div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite" hidden><span class="t-ic"></span><span class="t-tx"><b></b><small></small></span><button class="t-x" type="button" aria-label="Fermer">✕</button></div>
''')

html = '\n'.join(H)
def _nb(m):
    x = m.group(0); x = re.sub(r'(?<=\d) (?=000\b)', ' ', x); x = re.sub(r'(?<=000) (?=FCFA)', ' ', x)
    return re.sub(r' ([?!:;»])', ' \\1', x).replace('« ', '« ')
cut = html.index('</style>')
html = html[:cut] + re.sub(r'>[^<]+<', _nb, html[cut:])
js = open(f'{V4}/app.js', encoding='utf-8').read()
for k in ['countdown', 'roi', 'audio', 'fx', 'toast']:
    js = js.replace(f'/*{k.upper()}*/', open(f'{SP}/js/{k}.js', encoding='utf-8').read().replace("document.getElementById('offre').scrollIntoView({ behavior: 'smooth' })", "goTo('tarif')"))
js = (js.replace('/*EN*/{}', json.dumps(EN, ensure_ascii=False)).replace('/*ROTFR*/[]', json.dumps(ROT_FR, ensure_ascii=False)).replace('/*ROTEN*/[]', json.dumps(ROT_EN, ensure_ascii=False))
        .replace('/*TUNFR*/[]', json.dumps(TUN_FR, ensure_ascii=False)).replace('/*TUNEN*/[]', json.dumps(TUN_EN, ensure_ascii=False)).replace('/*CTA*/""', json.dumps(CTA))
        .replace('/*IC*/{}', json.dumps({'play': icon('Play'), 'pause': icon('Pause'), 'vol': icon('VolumeHigh'), 'volLow': icon('VolumeLow'), 'mute': icon('VolumeOff'), 'fs': icon('FullScreen'), 'fsx': icon('ArrowShrink02'), 'rw': icon('GoBackward10Sec'), 'fw': icon('GoForward10Sec')})))
html += f'<script>\n{js}\n</script>\n</body>\n</html>\n'
open(f'{REPO}/index.html', 'w', encoding='utf-8').write(html)
print('written', len(html), 'keys', len(EN))
