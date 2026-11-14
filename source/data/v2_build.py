# Fichiers de travail : lis seulement le texte (FAQ, profils), ce script ne sert pas tel quel. Voir source/README.md.
import json, math, re, os
SP='/tmp/claude-0/-home-user/86aa9d93-3569-51fa-b7ca-8789a11c3cd6/scratchpad'
REPO='/home/user/vibe-motion---master-class'
EN={}
def t(k, fr, en):
    EN[k]=en
    return f'data-i18n="{k}">{fr}'
CTA='https://rogerboujieka237.mychariow.shop/prd_9wrq07d2/checkout'
WA_GROUP='https://chat.whatsapp.com/HhJZm77fXCd9j9TWNGx7Bk'
WA_DM='https://wa.me/237678594247?text=Bonjour%20Roger%2C%20j%27ai%20une%20question%20sur%20la%20formation%20Vibe%20Motion.'
wa_sym=open(f'{SP}/wa.svg').read().strip()
marquee=open(f'{SP}/marquee.html').read().strip()
rays=''.join(f'<line x1="{50+14*math.cos(a):.1f}" y1="{50+14*math.sin(a):.1f}" x2="{50+(46 if i%2==0 else 40)*math.cos(a):.1f}" y2="{50+(46 if i%2==0 else 40)*math.sin(a):.1f}"/>' for i,a in enumerate([k*math.pi/6+0.13 for k in range(12)]))
def spark(cls): return f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true"><g stroke="currentColor" stroke-width="9" stroke-linecap="round">{rays}</g></svg>'
def btn(k, fr, en, cls='btn btn-red', href=None, cta=True, extra=''):
    h = href or CTA
    return f'<a class="{cls}{" js-cta" if cta else ""}" href="{h}"{extra}><span {t(k,fr,en)}</span><span class="arr" aria-hidden="true"></span></a>'
def arr(): return '<span class="arr" aria-hidden="true"></span>'
INF='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M18.2 8.2c2.4 0 4.3 1.7 4.3 3.8s-1.9 3.8-4.3 3.8c-3.6 0-8.8-7.6-12.4-7.6C3.4 8.2 1.5 9.9 1.5 12s1.9 3.8 4.3 3.8c3.6 0 8.8-7.6 12.4-7.6z"/></svg>'
UPD='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 12a8.5 8.5 0 0 1-14.7 5.8M3.5 12A8.5 8.5 0 0 1 18.2 6.2"/><path d="M18.5 2.5v4h-4M5.5 21.5v-4h4"/></svg>'
WAI='<svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg>'
def cdbox(pfx):
    return (f'<div class="cd island" role="timer"><div class="l"><i></i><span {t("cd_l","Le prix promo expire dans :","The promo price expires in:")}</span></div>'
            f'<div class="t js-cd"><div class="u"><b>10</b><small {t("cd_h","HEURES","HOURS")}</small></div><span class="sep">:</span><div class="u"><b>00</b><small {t("cd_m","MINUTES","MINUTES")}</small></div><span class="sep">:</span><div class="u"><b>00</b><small {t("cd_s","SECONDES","SECONDS")}</small></div></div>'
            '<div class="pb"><i class="js-cd-bar"></i></div></div>')
METHODS='<div class="methods"><img decoding="async" src="orange-money.svg" alt="Orange Money" width="54" height="32"><img decoding="async" src="momo-mtn.webp" alt="MoMo MTN Mobile Money" width="54" height="32"><img decoding="async" src="moov-money.svg" alt="Moov Money" width="54" height="32"><img decoding="async" src="visa.svg" alt="Visa" width="48" height="32"><img decoding="async" src="mastercard.svg" alt="Mastercard" width="48" height="32"></div>'

# ---------- works ----------
WORKS=[('IHRFvM2n8Ws','Spectacle Cabrel Tindo','Spot spectacle · motion design','Cabrel Tindo show','Show ad · motion design'),
 ('4abyQA1a9h8','Croisade Bafoussam pour Jésus','Événement chrétien · spot complet','Bafoussam for Jesus crusade','Christian event · full ad'),
 ('IMaHC8wFzuM','Pub motion design','Publicité · motion design','Motion design ad','Advertising · motion design'),
 ('U2wMu5KrVnQ','Motion design Camair-Co','Compagnie aérienne · motion design','Camair-Co motion design','Airline · motion design'),
 ('zbV6wVUsFxU','Bus gratuits · Bafoussam pour Jésus','Spot annonce événement','Free buses · Bafoussam for Jesus','Event announcement ad'),
 ('oVP2kVm4lMs','Invitation Grande Nuit de Clôture','Bafoussam pour Jésus · spot invitation','Grand Closing Night invitation','Bafoussam for Jesus · invitation ad'),
 ('Web3N01yUVA','Motion design App Mr N','Application mobile · motion design','Mr N app motion design','Mobile app · motion design')]
def yt(i,w):
    vid,ft,fs,et,es=w
    return (f'<figure class="wk"><span class="nw" {t("nw","<i></i>Nouvelle réalisation","<i></i>New work")}</span>'
            f'<div class="yt" role="button" tabindex="0" data-yt="{vid}" aria-label="▶ {ft}"><img class="th" loading="lazy" decoding="async" src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt=""><i class="pl" aria-hidden="true"></i><i class="ld" aria-hidden="true"></i></div>'
            f'<figcaption><b {t(f"w{i}t",ft,et)}</b><span {t(f"w{i}s",fs,es)}</span></figcaption></figure>')
works_html=''.join(yt(i,w) for i,w in enumerate(WORKS))

# ---------- modules (from the programme document) ----------
src=open(f'{SP}/prog.py',encoding='utf-8').read()
ns={}; exec(src[src.index('M=['):src.index('\nEN={}')],ns); M=ns['M']
flagFR={'key':'Essentiel','live':'Cas pratique','money':'Revenus'}; flagEN={'key':'Key','live':'Case study','money':'Income'}
mods=[]
for i,(n,d,ft,fs,fd,et,es,ed,fl) in enumerate(M):
    kick=('Introduction' if n=='00' else f'Module {int(n)}')
    badge=f'<span class="f {fl}" {t("pf_"+fl,flagFR[fl],flagEN[fl])}</span>' if fl else ''
    mods.append(f'<details class="pm{" hl" if fl=="money" else ""}"{" open" if i==0 else ""}><summary><span class="n">{n}</span><span class="b"><span class="k">{kick} · {d}{badge}</span><b {t(f"m{i}t",ft,et)}</b><span class="s" {t(f"m{i}s",fs,es)}</span></span><i class="chev" aria-hidden="true"></i></summary><p {t(f"m{i}d",fd,ed)}</p></details>')
mods_html='\n'.join(mods)

# ---------- FAQ ----------
FAQ=[("Faut-il un ordinateur, ou mon téléphone suffit-il ?","Les deux fonctionnent. Vous pouvez suivre la formation et appliquer la méthode sur smartphone ou sur ordinateur, avec l'appareil que vous avez déjà. Pour les vidéos longues avec beaucoup de rushs, l'ordinateur est plus confortable.",
      "Do I need a computer, or is my phone enough?","Both work. You can follow the course and apply the method on a smartphone or a computer, with the device you already have. For long videos with lots of footage, a computer is more comfortable."),
     ("Je n'ai jamais fait de montage. Est-ce pour moi ?","Oui. Je pars de zéro : installation, organisation du projet, prompt, voix off, puis création et livraison. Chaque étape est montrée à l'écran.",
      "I've never edited a video. Is this for me?","Yes. I start from zero: setup, project organisation, prompt, voice-over, then creation and delivery. Every step is shown on screen."),
     ("Quand est-ce que je reçois mon accès ?","Juste après le paiement, vous recevez l'accès à vie à la formation et au groupe WhatsApp d'accompagnement.",
      "When do I get access?","Right after payment, you get lifetime access to the course and the WhatsApp support group."),
     ("Combien de temps ai-je accès à la formation ?","À vie. Vous payez une seule fois et vous gardez l'accès pour toujours, avec toutes les mises à jour gratuites : chaque nouveau module ou nouvelle méthode vous est offert.",
      "How long do I have access?","For life. You pay once and keep access forever, with every update free: each new module or method is included."),
     ("Comment se déroule la formation ?","C'est une formation vidéo déjà enregistrée : 15 vidéos, 1 h 14 au total. Vous la regardez quand vous voulez, à votre rythme, et vous revoyez chaque étape autant de fois que nécessaire.",
      "How does the course work?","It's a pre-recorded video course: 15 videos, 1 h 14 in total. Watch whenever you want, at your own pace, and replay every step as often as you need."),
     ("Faut-il payer un abonnement en plus ?","Oui, il faut un abonnement Claude Pro : 20 $ par mois, soit environ 12 000 FCFA, sans engagement. Je vous montre au module 4 comment le prendre, même avec une carte virtuelle payée par Mobile Money. iziVoice fonctionne avec des crédits selon votre usage. Une seule vidéo vendue suffit en général à couvrir l'abonnement du mois.",
      "Do I need to pay for a subscription too?","Yes, you need a Claude Pro subscription: $20 a month, about 12,000 FCFA, cancel anytime. Module 4 shows you how to get it, even with a virtual card paid by Mobile Money. iziVoice works with credits as you go. A single video sold usually covers the month's subscription."),
     ("J'habite hors du Cameroun. Comment ça se passe ?","Aucun problème : la formation est 100 % en ligne. Le prix est en FCFA et le site vous affiche une estimation dans votre devise. Le paiement par carte fonctionne partout.",
      "I live outside Cameroon. How does it work?","No problem: the course is 100% online. The price is in FCFA and the site shows you an estimate in your currency. Card payment works everywhere."),
     ("Comment se passe le paiement ?","Le paiement est sécurisé : Orange Money, MTN MoMo, Moov Money, Visa ou Mastercard. Vous payez une seule fois, sans abonnement.",
      "How does payment work?","Payment is secure: Orange Money, MTN MoMo, Moov Money, Visa or Mastercard. You pay once, with no subscription."),
     ("Vais-je vraiment pouvoir gagner de l'argent ?","Les entreprises, les églises et les créateurs ont besoin de vidéos. Le module 14 vous montre quoi vendre, à quel prix, et comment trouver vos premiers clients. Vos résultats dépendront de votre travail : aucun revenu n'est garanti.",
      "Will I really be able to earn money?","Businesses, churches and creators need videos. Module 14 shows you what to sell, at what price and how to find your first clients. Your results depend on your work: no income is guaranteed.")]
def faq_html(items, pfx, first_open=True):
    out=[]
    for i,(fq,fa,eq,ea) in enumerate(items):
        out.append(f'<details{" open" if (i==0 and first_open) else ""}><summary><span {t(f"{pfx}{i}q",fq,eq)}</span><i class="chev" aria-hidden="true"></i></summary><p {t(f"{pfx}{i}a",fa,ea)}</p></details>')
    return '\n'.join(out)

# ---------- who ----------
WHO=[('💼','Entrepreneurs et commerçants',"Vous payez un monteur à chaque vidéo, ou vous ne publiez presque rien.",["Vos pubs et statuts WhatsApp vous-même","Des vidéos produit qui font vendre"],'Entrepreneurs and shop owners',"You pay an editor for every video, or hardly post at all.",["Your own ads and WhatsApp statuses","Product videos that sell"]),
 ('⛪','Pasteurs, églises et ministères',"Vous annoncez cultes, croisades et conférences et voulez toucher plus d'âmes.",["Affiches transformées en invitations animées","Une équipe média qui produit chaque semaine"],'Pastors, churches and ministries',"You announce services, crusades and conferences and want to reach more people.",["Posters turned into animated invitations","A media team that produces every week"]),
 ('📣','Responsables communication',"Entreprise, ONG, école : on vous demande plus de vidéos, plus vite.",["Spots et teasers produits en interne","Formats 16:9 et 9:16 livrés vite"],'Communication managers',"Company, NGO, school: you're asked for more videos, faster.",["Ads and teasers made in-house","16:9 and 9:16 formats delivered fast"]),
 ('🎬','Créateurs de contenu',"YouTube, TikTok, Instagram : vous voulez un rendu pro et un rythme qui retient.",["Vidéos longues et Shorts plus vite","Titres animés, sons et voix off"],'Content creators',"YouTube, TikTok, Instagram: you want a pro look and pacing that keeps viewers.",["Long videos and Shorts, faster","Animated titles, sounds and voice-overs"]),
 ('🎨','Graphistes et vidéastes',"Vous maîtrisez l'image et voulez ajouter le motion design et l'IA à vos services.",["Affiches animées et spots motion","Des packs vendus plus cher"],'Designers and videographers',"You master visuals and want to add motion design and AI to your services.",["Animated posters and motion ads","Packages sold at a better price"]),
 ('🎓','Étudiants et reconversion',"Vous cherchez une compétence demandée, rapide à apprendre et à vendre.",["Apprendre de zéro, sans logiciel compliqué","Trouver vos premiers clients"],'Students and career changers',"You want an in-demand skill that's quick to learn and to sell.",["Learn from scratch, no complicated software","Find your first clients"])]
who=[]
for i,(e,ft,fd,fl,et,ed,el) in enumerate(WHO):
    EN[f'wh{i}l']=''.join(f'<li>{x}</li>' for x in el)
    who.append(f'<article class="wc"><span class="e" aria-hidden="true">{e}</span><h3 {t(f"wh{i}t",ft,et)}</h3><p {t(f"wh{i}d",fd,ed)}</p><ul data-i18n="wh{i}l">'+''.join(f'<li>{x}</li>' for x in fl)+'</ul></article>')
who_html='\n'.join(who)

def guarantees(cls):
    return (f'<div class="{cls}">'
      f'<div class="g rv"><span class="gi">{INF}</span><div><b {t("g1h","Accès à vie","Lifetime access")}</b><p {t("g1p","Payez une seule fois, gardez la formation pour toujours.","Pay once, keep the course forever.")}</p></div></div>'
      f'<div class="g rv d1"><span class="gi">{UPD}</span><div><b {t("g2h","Mises à jour gratuites à vie","Free lifetime updates")}</b><p {t("g2p","Chaque nouveau module et chaque nouvelle méthode vous sont offerts.","Every new module and method is yours at no extra cost.")}</p></div></div>'
      f'<div class="g rv d2"><span class="gi">{WAI}</span><div><b {t("g3h","Accompagnement garanti","Guaranteed support")}</b><p {t("g3p","Dans le groupe WhatsApp privé, je réponds à vos questions.","In the private WhatsApp group, I answer your questions.")}</p></div></div>'
      '</div>')

NAV=[('accueil','Accueil','Home'),('formation','La formation','The course'),('formateur','Le formateur','The trainer'),('vision','La vision','The vision'),('avantages','Avantages','Benefits'),('faq','FAQ','FAQ')]
nav_html=''.join(f'<a href="#{k}" data-v="{k}" {t("nav_"+k,fr,en)}</a>' for k,fr,en in NAV)
sheet_html=''.join(f'<a class="it" href="#{k}" data-v="{k}" {t("nav_"+k,fr,en)}</a>' for k,fr,en in NAV)

ROT_FR=['publicités','motion designs','affiches animées','vidéos YouTube','invitations']
ROT_EN=['ads','motion designs','animated posters','YouTube videos','invitations']
rot='<span class="rot" aria-hidden="true">'+''.join(f'<span{" class=\"on\"" if i==0 else ""}>{w}</span>' for i,w in enumerate(ROT_FR))+'</span>'

H=[]
A=H.append
A(f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#ffffff">
<title>Vibe Motion · Formation montage vidéo et motion design avec l'IA</title>
<meta name="description" content="Créez des spots, des motion designs et des affiches animées avec Claude Opus 5.5 et iziVoice. Formation de Roger BOUJIEKA : 15 vidéos, accès à vie, smartphone ou ordinateur. 15 000 FCFA au lieu de 35 000.">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:url" content="https://www.rogerboujieka.com/"><meta property="og:title" content="Vibe Motion · Créez des vidéos pro avec l'IA">
<meta property="og:description" content="Montage vidéo et motion design avec Claude Opus 5.5 et iziVoice, sur smartphone ou ordinateur. 15 000 FCFA au lieu de 35 000."><meta property="og:image" content="https://www.rogerboujieka.com/og.jpg">
<script>try{{if(localStorage.getItem('mc_theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<link rel="preload" href="fonts/inter-tight.woff2" as="font" type="font/woff2" crossorigin>
<style>
{open(f"{SP}/v2/css.css").read()}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{wa_sym}</svg>
<div class="amb" aria-hidden="true"><i></i><i></i></div>

<a class="ann js-goffer" href="#offre"><i class="dot"></i><span {t("ann","Offre −57 % · fin dans","Offer −57% · ends in")}</span><b class="js-cd-hms">10:00:00</b></a>
<header class="top" id="top">
  <div class="wrap">
    <a class="brand" href="#accueil" data-v="accueil" aria-label="Roger BOUJIEKA"><img class="lg-d" src="logo_rb.png" alt="Roger BOUJIEKA" width="160" height="40"><img class="lg-l" src="logo_rb_dk.png" alt="Roger BOUJIEKA" width="160" height="40"></a>
    <nav class="nav" aria-label="Menu">{nav_html}</nav>
    <div class="sp"></div>
    <div class="lang" role="group" aria-label="Langue / Language"><button id="lang-fr" aria-pressed="true">FR</button><button id="lang-en" aria-pressed="false">EN</button></div>
    <button class="thm" id="thm" type="button" aria-label="Mode jour / nuit"><svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg></button>
    {btn("cta_top","Je m'inscris","Enrol now")}
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><i></i></button>
  </div>
  <div class="cbar" id="cbar" hidden><div class="row"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg><span class="tx" {t("cb_t","<span class='l'>Communauté WhatsApp gratuite <b>LE DIGITAL POUR TOUS</b> : IA, marketing digital, création de contenu et bien plus.</span><span class='s'><b>LE DIGITAL POUR TOUS</b> · communauté gratuite</span>","<span class='l'>Free WhatsApp community <b>LE DIGITAL POUR TOUS</b>: AI, digital marketing, content creation and more.</span><span class='s'><b>LE DIGITAL POUR TOUS</b> · free community</span>")}</span><a class="go" href="{WA_GROUP}" target="_blank" rel="noopener" {t("cb_go","Rejoindre","Join")}</a><button class="x" type="button" aria-label="Fermer">✕</button></div></div>
</header>
<div class="sheet" aria-hidden="true">{sheet_html}{btn("cta_sheet","Je rejoins la formation","Join the course","btn btn-red btn-lg")}</div>

<main>
<!-- ================= ACCUEIL ================= -->
<div class="view on" id="v-accueil" data-view="accueil">

<section class="hero">
  <div class="sky">
    <div class="clouds" aria-hidden="true"><i class="k1"></i><i class="k2"></i><i class="k3"></i><i class="k4"></i><i class="k5"></i><i class="k6"></i></div>
    <span class="fl fl1 cl" aria-hidden="true">{spark("x")}</span><span class="fl fl2" aria-hidden="true"><img src="izivoice-icon.png" alt=""></span><span class="fl fl3" aria-hidden="true"><img src="izivoice-icon.png" alt=""></span><span class="fl fl4 cl" aria-hidden="true">{spark("x")}</span><span class="fl fl5 cl" aria-hidden="true">{spark("x")}</span>
    <div class="wrap hc">
      <span class="pill in"><i></i><span {t("h_pill","Nouvelle formation · Accès immédiat","New course · Instant access")}</span></span>
      <h1 class="h1"><span class="l" {t("h1a","Créez des","Create")}</span>{rot}<span class="sr js-rot-sr">{ROT_FR[0]}</span><span class="l" {t("h1b","avec l'IA.","with AI.")}</span></h1>
      <p class="sub" {t("h_sub","Même si vous partez de zéro. Je vous montre la méthode exacte que j'utilise pour mes clients : <b>Claude Opus 5.5 monte</b>, <b>iziVoice fait la voix</b>, vous dirigez. Sur smartphone ou ordinateur.","Even if you're starting from zero. I show you the exact method I use for my clients: <b>Claude Opus 5.5 edits</b>, <b>iziVoice does the voice</b>, you direct. On a smartphone or a computer.")}</p>
      <div class="cta-row">{btn("cta_hero","Je rejoins la formation","Join the course","btn btn-red btn-lg")}<a class="btn btn-glass btn-lg" href="#realisations"><span {t("h_see","Voir mes réalisations","See my work")}</span></a></div>
      <div class="price-mini"><b>15 000</b><small>FCFA</small><s>35 000 FCFA</s><span class="off">−57 %</span></div>
      <ul class="trust"><li {t("tr1","Accès immédiat","Instant access")}</li><li {t("tr2","Accès à vie","Lifetime access")}</li><li {t("tr3","Téléphone ou PC","Phone or PC")}</li><li {t("tr4","Mobile Money","Mobile Money")}</li></ul>
    </div>
    <div class="ringw" aria-hidden="true"><div class="ring"><div class="rs" style="--i:0"><div class="rc im"><img src="motion-kwiva.jpg" alt="" loading="lazy" decoding="async"><span>Kwiva · motion</span></div></div><div class="rs" style="--i:1"><div class="rc ui"><span class="ut"><i class="uic cl">{spark("x")}</i>Claude Opus 5.5</span><small {t("rg1","Montage en cours","Editing")}</small><span class="ub"><i style="width:78%"></i></span><b>78 %</b></div></div><div class="rs" style="--i:2"><div class="rc im"><img src="work-camairco.jpg" alt="" loading="lazy" decoding="async"><span>Camair-Co · spot</span></div></div><div class="rs" style="--i:3"><div class="rc ui"><span class="ut"><i class="uic"><img class='izi' src='izivoice-icon.png' alt='' width='22' height='22'></i>iziVoice</span><small {t("rg2","Voix off · français","Voice-over · French")}</small><span class="wave"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></div></div><div class="rs" style="--i:4"><div class="rc im"><img src="motion-mboa.jpg" alt="" loading="lazy" decoding="async"><span>Mboa Market</span></div></div><div class="rs" style="--i:5"><div class="rc ui ok"><span class="ut"><i class="uic g">✓</i><span {t("rg3","Vidéo prête","Video ready")}</span></span><small>16:9 · 9:16 · 1080p</small><b {t("rg4","Livrée au client","Sent to the client")}</b></div></div><div class="rs" style="--i:6"><div class="rc im"><img src="work-bovann.jpg" alt="" loading="lazy" decoding="async"><span>Bovann Group</span></div></div><div class="rs" style="--i:7"><div class="rc ui"><span class="ut"><i class="uic r">₣</i><span {t("rg5","Paiement reçu","Payment received")}</span></span><small>Mobile Money</small><b>+ 50 000 FCFA</b></div></div><div class="rs" style="--i:8"><div class="rc im"><img src="motion-volta.jpg" alt="" loading="lazy" decoding="async"><span>Volta · lancement</span></div></div><div class="rs" style="--i:9"><div class="rc im"><img src="motion-snapia.jpg" alt="" loading="lazy" decoding="async"><span>Snapia · app</span></div></div></div></div>
  </div>
</section>

<div>{marquee}</div>

<section class="about">
  <div class="wrap">
    <div class="head c rv"><span class="eye" {t("ab_eye","À propos","About")}</span><h2 class="h2" {t("ab_h","Une formation pour créer <em>et vendre des vidéos pro.</em>","A course to create <em>and sell pro videos.</em>")}</h2></div>
    <div class="b2g">
      <div class="b2 photo rv"><div class="sky2" aria-hidden="true"></div><img src="roger.webp" alt="Roger BOUJIEKA" width="1000" height="1000" loading="lazy" decoding="async"><span class="tag">Roger BOUJIEKA</span><div class="ov"><b><span class="js-count" data-to="7">0</span></b><span {t("ab1","réalisations récentes à découvrir","recent works to discover")}</span></div></div>
      <div class="b2 w rv d1"><span class="k" {t("ab2k","Accès","Access")}</span><b class="inf">∞</b><p {t("ab2p","Accès à vie et mises à jour gratuites : vous payez une fois, la formation évolue avec les outils d'IA, et vous en profitez sans rien payer de plus.","Lifetime access and free updates: you pay once, the course evolves with AI tools, and you benefit at no extra cost.")}</p><div class="tl2"><span><i class="cl">{spark("x")}</i>Claude Opus 5.5</span><span><i><img class='izi' src='izivoice-icon.png' alt='' width='22' height='22'></i>iziVoice</span></div></div>
      <div class="b2 red rv d2"><span class="k" {t("ab3k","Vidéos de formation","Course videos")}</span><b><span class="js-count" data-to="15">0</span></b><p {t("ab3p","Courtes, concrètes, dans le bon ordre : 1 h 14 au total.","Short, practical, in the right order: 1 h 14 in total.")}</p></div>
      <div class="b2 blk rv d3"><span class="k" {t("ab4k","Modules pas à pas","Step-by-step modules")}</span><b><span class="js-count" data-to="14">0</span></b></div>
    </div>
  </div>
</section>

<section id="realisations" style="padding-top:20px">
  <div class="wrap">
    <div class="head rv"><span class="eye" {t("wk_eye","Réalisations","Portfolio")}</span><h2 class="h2" {t("wk_h","Voici ce que vous allez <em>savoir créer.</em>","This is what you will <em>learn to create.</em>")}</h2><p class="lead" {t("wk_p","Des spots réalisés pour de vrais clients avec la méthode enseignée dans la formation. Appuyez pour regarder.","Ads made for real clients with the method taught in the course. Tap to watch.")}</p></div>
    <div class="rail js-rail">{works_html}</div>
    <div class="rail-nav"><span class="made" {t("wk_made","7 réalisations · balayez pour voir la suite","7 works · swipe to see more")}</span><div class="rail-btns"><button type="button" class="js-prev" aria-label="Précédent">←</button><button type="button" class="js-next" aria-label="Suivant">→</button></div></div>
  </div>
</section>

<section class="op island" id="opus">
  <div class="op-bg" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><b></b></div>
  <div class="wrap"><div class="op-in rv">
    <span class="op-eye" {t("op_eye","Mes vidéos sont réalisées avec","My videos are made with")}</span>
    <h2 class="op-t"><span>Claude</span>{spark("op-sp")}<span class="op-o">OPUS 5.5</span></h2>
    <p class="op-p" {t("op_p","Dans la formation, c'est <b>Claude Opus 5.5</b> qui monte vos vidéos et vos motion designs. <b><img class='op-izi' src='izivoice-icon.png' alt='' width='22' height='22'>iziVoice</b> lui apporte les voix off, la musique et les sons, directement depuis Claude.","In the course, <b>Claude Opus 5.5</b> edits your videos and motion designs. <b><img class='op-izi' src='izivoice-icon.png' alt='' width='22' height='22'>iziVoice</b> adds the voice-overs, music and sounds, right from Claude.")}</p>
    <ul class="op-f"><li {t("op_f1","Montage et motion design","Editing and motion design")}</li><li style="display:flex;align-items:center;gap:6px"><img class="izi" src="izivoice-icon.png" alt="" width="22" height="22"><span {t("op_f2","Voix off et musique avec iziVoice","Voice-over and music with iziVoice")}</span></li><li {t("op_f3","Formats YouTube et réseaux sociaux","YouTube and social formats")}</li></ul>
    {btn("op_cta","J'apprends avec Claude Opus 5.5","I learn with Claude Opus 5.5")}
    <p class="op-tm" {t("op_tm","Claude et Opus sont des marques d'Anthropic. Formation indépendante, non affiliée à Anthropic.","Claude and Opus are trademarks of Anthropic. Independent course, not affiliated with Anthropic.")}</p>
  </div></div>
</section>


<section class="roi" id="abonnement">
  <div class="wrap">
    <div class="rv">
      <div class="head" style="margin-bottom:0"><span class="eye" {t("ro_eye","Après la formation","After the course")}</span><h2 class="h2" {t("ro_h","Un abonnement à 12 000 FCFA.<br><em>Des vidéos qui valent bien plus.</em>","A 12,000 FCFA subscription.<br><em>Videos worth far more.</em>")}</h2>
      <p class="lead" {t("ro_p","Pour créer vos vidéos, il vous faut l'abonnement <b>Claude Pro</b>. C'est votre monteur, votre motion designer et votre animateur, réunis dans un seul outil. Je vous montre comment le prendre, pas à pas, même par Mobile Money.","To create your videos you need the <b>Claude Pro</b> subscription. It's your editor, motion designer and animator in one tool. I show you how to get it, step by step, even with Mobile Money.")}</p></div>
      <div class="sub-card"><span class="ic">{spark("x")}</span><div><b>Claude Pro</b><span {t("ro_sc","Abonnement mensuel, sans engagement · module 4","Monthly, cancel anytime · module 4")}</span></div><div class="amt"><b>≈ 12 000</b><small {t("ro_am","FCFA / mois · 20 $","FCFA / month · $20")}</small></div></div>
      <ul class="roi-pts" data-i18n="ro_l"><li><b>Une seule vidéo vendue</b> rembourse l'abonnement du mois.</li><li>Spots, motion designs, affiches animées, vidéos longues : <b>tout se fait avec le même abonnement.</b></li><li>Voix off avec <b>iziVoice</b> : des crédits selon votre usage, et la qualité Eco pour économiser (module 7).</li></ul>
    </div>
    <div class="roi-in island rv d1" id="roi">
      <h3 {t("ro_ch","Calculez ce que vous pouvez gagner","Work out what you could earn")}</h3>
      <div class="ctl"><div class="r"><span {t("ro_n","Vidéos livrées par mois","Videos delivered per month")}</span><b class="js-rn">4</b></div><input type="range" min="1" max="20" value="4" class="js-rr" aria-label="Vidéos par mois"></div>
      <div class="ctl"><div class="r"><span {t("ro_pp","Prix d'une vidéo","Price per video")}</span></div>
        <div class="seg js-seg"><button type="button" data-p="15000" aria-pressed="false">15 000<small {t("ro_s1","affiche animée","animated poster")}</small></button><button type="button" data-p="25000" aria-pressed="false">25 000<small {t("ro_s2","statut / réseaux","status / social")}</small></button><button type="button" data-p="50000" aria-pressed="true">50 000<small {t("ro_s3","spot motion","motion ad")}</small></button><button type="button" data-p="150000" aria-pressed="false">150 000<small {t("ro_s4","spot pro","pro ad")}</small></button></div></div>
      <div class="bars"><div class="cost"><div class="bl"><span {t("ro_b1","Votre abonnement Claude","Your Claude subscription")}</span><b>12 000 FCFA</b></div><div class="tr"><i class="js-bc"></i></div></div>
        <div class="gain"><div class="bl"><span {t("ro_b2","Ce que vous facturez","What you bill")}</span><b class="js-bg">200 000 FCFA</b></div><div class="tr"><i class="js-bgb"></i></div></div></div>
      <div class="res"><div><span class="big js-rv">200 000</span><small><span {t("ro_r","FCFA par mois · ","FCFA a month · ")}</span><span class="js-rc">4</span> <span {t("ro_rc","clients livrés","clients served")}</span></small></div><div class="x"><span class="js-rx">17×</span><small {t("ro_x","l'abonnement","the subscription")}</small></div></div>
      <p class="roi-n" {t("ro_note","Exemple de calcul indicatif, avec des prix couramment pratiqués. Vos revenus dépendent de vos clients et de votre travail. Claude Pro : 20 $/mois (prix variable selon le pays et les taxes) ; ses limites d'utilisation sont fixées par Anthropic.","Indicative example using common market prices. Your income depends on your clients and your work. Claude Pro: $20/month (price varies by country and taxes); usage limits are set by Anthropic.")}</p>
    </div>
  </div>
</section>

<section style="padding-bottom:0">
  <div class="wrap">
    <div class="head c rv"><span class="eye" {t("rc_eye","Le match","The match")}</span><h2 class="h2" {t("rc_h","Logiciels classiques<br><em>contre IA.</em>","Classic software<br><em>versus AI.</em>")}</h2><p class="lead" {t("rc_p","Le même spot de 90 secondes, deux façons de le faire. Lancez la comparaison et regardez la différence.","The same 90-second ad, two ways to make it. Start the comparison and watch the difference.")}</p></div>
    <div class="race island rv" id="race">
      <div class="lanes">
        <div class="lane classic">
          <div class="lh"><span class="apps"><i class="ps">Ps</i><i class="pr">Pr</i><i class="ae">Ae</i></span><span {t("rc_c","Montage classique","Classic editing")}</span></div>
          <div class="facts"><span><small {t("rc_f1","Logiciels","Software")}</small><b {t("rc_c1","≈ 41 000 FCFA/mois","≈ 41,000 FCFA/mo")}</b></span><span><small {t("rc_f2","Matériel","Hardware")}</small><b {t("rc_c2","PC puissant","Powerful PC")}</b></span><span><small {t("rc_f3","Apprendre","Learning")}</small><b {t("rc_c3","Des mois","Months")}</b></span></div>
          <div class="prog"><i class="js-pa"></i></div>
          <div class="st"><span class="js-sa" {t("rc_ready","Prêt à démarrer","Ready to start")}</span><b class="js-ta">0 min</b></div>
        </div>
        <div class="vs"><span>VS</span></div>
        <div class="lane ai">
          <div class="lh"><span class="apps"><i class="cl">{spark("x")}</i><i class="iz"><img class='izi' src='izivoice-icon.png' alt='' width='22' height='22'></i></span><span>Claude Opus 5.5 + iziVoice</span></div>
          <div class="facts"><span><small {t("rc_f1","Logiciels","Software")}</small><b {t("rc_a1","≈ 12 000 FCFA/mois","≈ 12,000 FCFA/mo")}</b></span><span><small {t("rc_f2","Matériel","Hardware")}</small><b {t("rc_a2","Téléphone ou PC","Phone or PC")}</b></span><span><small {t("rc_f3","Apprendre","Learning")}</small><b>1 h 14</b></span></div>
          <div class="prog"><i class="js-pb"></i></div>
          <div class="st"><span class="js-sb" {t("rc_ready","Prêt à démarrer","Ready to start")}</span><b class="js-tb">0 min</b></div>
        </div>
      </div>
      <div class="rbtm"><div class="sum"><b {t("rc_s","10× plus vite","10× faster")}</b><span {t("rc_s2","et environ 29 000 FCFA économisés chaque mois sur les logiciels.","and about 29,000 FCFA saved every month on software.")}</span></div><button class="btn btn-red js-race" type="button"><span {t("rc_go","▶ Lancer la comparaison","▶ Start the comparison")}</span></button></div>
      <p class="race-n" {t("rc_n","Durées indicatives pour un spot de 90 secondes. Adobe Creative Cloud Pro (Photoshop, Premiere, After Effects) : 69,99 $/mois ; Claude Pro : 20 $/mois. Prix variables selon le pays.","Indicative times for a 90-second ad. Adobe Creative Cloud Pro (Photoshop, Premiere, After Effects): $69.99/month; Claude Pro: $20/month. Prices vary by country.")}</p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="head c rv"><span class="eye" {t("ba_eye","Avant / Après","Before / After")}</span><h2 class="h2" {t("ba_h","Des heures de montage.<br><em>Ou 24 minutes.</em>","Hours of editing.<br><em>Or 24 minutes.</em>")}</h2></div>
    <div class="ba">
      <div class="bac rv"><span class="tg" {t("ba_bt","Avant · montage classique","Before · classic editing")}</span><h3 {t("ba_bh","Lourd, lent et cher.","Heavy, slow and expensive.")}</h3>
        <ul data-i18n="ba_bl"><li>Des logiciels compliqués qui demandent des mois</li><li>Un ordinateur puissant presque obligatoire</li><li>Chaque titre et transition fait à la main</li><li>Un monteur à payer pour chaque vidéo</li></ul></div>
      <div class="bac after rv d1"><span class="tg" {t("ba_at","Après · avec ma méthode","After · with my method")}</span><h3 {t("ba_ah","Vous décrivez. L'IA monte.","You describe. AI edits.")}</h3>
        <ul data-i18n="ba_al"><li>Vous dictez votre idée, Claude Opus 5.5 construit la vidéo</li><li>Titres, transitions et animations en quelques minutes</li><li>Voix off, musique et effets sonores avec iziVoice</li><li>Sur smartphone ou ordinateur</li></ul></div>
    </div>
  </div>
</section>
''')
EN['ro_l']='<li><b>A single video sold</b> pays for the month\'s subscription.</li><li>Ads, motion designs, animated posters, long videos: <b>all made with the same subscription.</b></li><li>Voice-overs with <b>iziVoice</b>: credits as you go, and Eco quality to save (module 7).</li>'
EN['ba_bl']='<li>Complicated software that takes months to learn</li><li>A powerful computer almost required</li><li>Every title and transition done by hand</li><li>An editor to pay for every video</li>'
EN['ba_al']='<li>You dictate your idea, Claude Opus 5.5 builds the video</li><li>Titles, transitions and animations in minutes</li><li>Voice-over, music and sound effects with iziVoice</li><li>On a smartphone or a computer</li>'

STEPS=[('1','Modules 1 à 5','Installer et préparer',"Claude, l'extension Chrome, votre compte Pro et le dossier de projet qui guide l'IA.",'Modules 1 to 5','Install and set up',"Claude, the Chrome extension, your Pro account and the project folder that guides the AI."),
 ('2','Modules 6 et 7','Prompt et voix off',"Ma méthode des 8 ingrédients, mon modèle de prompt et les voix off iziVoice.",'Modules 6 and 7','Prompt and voice-over',"My 8-ingredient method, my prompt template and iziVoice voice-overs."),
 ('3','Modules 8 à 11','Créer vos vidéos',"Cas pratique en direct, motion depuis un lien, affiches animées, vidéos longues.",'Modules 8 to 11','Create your videos',"Live case study, motion from a link, animated posters, long videos."),
 ('4','Modules 12 à 14','Livrer et encaisser',"Retouches, livraison pro, inspiration, puis trouver vos clients et fixer vos prix.",'Modules 12 to 14','Deliver and get paid',"Edits, pro delivery, inspiration, then finding clients and setting prices.")]
steps=''.join(f'<div class="stp rv d{i}"><span class="n">{n}</span><span class="m" {t(f"sp{i}k",k,ek)}</span><h3 {t(f"sp{i}h",h,eh)}</h3><p {t(f"sp{i}p",p,ep)}</p></div>' for i,(n,k,h,p,ek,eh,ep) in enumerate(STEPS))
BENTO=[('🔗','Une vidéo motion à partir d\'un simple lien',"Donnez le lien d'un site : Claude l'analyse et construit une vidéo motion aux couleurs de la marque, en 16:9 et 9:16.",'Module 8 · 9','A motion video from a single link',"Give a website link: Claude analyses it and builds a motion video in the brand's colours, in 16:9 and 9:16.",True),
 ('🖼️','Des affiches animées','Transformez une affiche de concert, de croisade ou de promo en vidéo pour les statuts WhatsApp.','Module 10','Animated posters','Turn a concert, crusade or promo poster into a video for WhatsApp statuses.',False),
 ('🎙️','Des voix off pro','Voix naturelles, accents, voix clonée, musique et sons avec iziVoice, directement depuis Claude.','Module 7','Pro voice-overs','Natural voices, accents, cloned voice, music and sounds with iziVoice, right from Claude.',False),
 ('💍','Des vidéos longues','Mariages, anniversaires, YouTube, spots avec rushs : Claude place vos séquences.','Module 11','Long videos','Weddings, birthdays, YouTube, ads with footage: Claude places your shots.',False),
 ('📐','Tous les formats','16:9 pour YouTube, 9:16 pour les Shorts et les statuts, 1 min 30 pour WhatsApp, et même d\'autres langues.','Module 12','Every format','16:9 for YouTube, 9:16 for Shorts and statuses, 1 min 30 for WhatsApp, and even other languages.',False),
 ('💰','Vendre vos services','Quoi vendre, à quel prix, message WhatsApp prêt à envoyer, parcours client et plan d\'action sur 5 jours.','Module 14','Sell your services','What to sell, at what price, a ready-to-send WhatsApp message, client journey and a 5-day action plan.',True)]
bento=''.join(f'<div class="bx{(" wide big" if i==len(BENTO)-1 else " big") if big else ""} rv d{i%3}"><span class="ic" aria-hidden="true">{e}</span><h3 {t(f"bx{i}h",h,eh)}</h3><p {t(f"bx{i}p",p,ep)}</p><span class="tag">{tag}</span></div>' for i,(e,h,p,tag,eh,ep,big) in enumerate(BENTO))

A(f'''
<section style="background:var(--bg2);border-block:1px solid var(--line)">
  <div class="wrap">
    <div class="head c rv"><span class="eye" {t("bx_eye","Compétences","Skills")}</span><h2 class="h2" {t("bx_h","Ce que vous saurez faire<br><em>à la fin de la formation.</em>","What you'll be able to do<br><em>by the end of the course.</em>")}</h2></div>
    <div class="bento">{bento}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head rv"><span class="eye" {t("sp_eye","Le parcours","The path")}</span><h2 class="h2" {t("sp_h","De l'installation à<br><em>vos premiers clients.</em>","From setup to<br><em>your first clients.</em>")}</h2><p class="lead" {t("sp_p","15 vidéos courtes et concrètes, dans le bon ordre. Vous avancez à votre rythme et vous revoyez chaque étape autant que vous voulez.","15 short, practical videos in the right order. Move at your own pace and replay any step as often as you like.")}</p></div>
    <div class="steps">{steps}</div>
    <div class="more"><a class="btn btn-ghost" href="#formation" data-v="formation"><span {t("sp_more","Voir le programme complet","See the full programme")}</span>{arr()}</a></div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <details class="whd rv"><summary><span class="wi" aria-hidden="true">🎯</span><span class="wt"><b {t("wh_b","Cette formation est faite pour qui ?","Who is this course for?")}</b><span {t("wh_s","Entrepreneurs, églises, communicants, créateurs, graphistes, étudiants…","Entrepreneurs, churches, communicators, creators, designers, students…")}</span></span><i class="chev" aria-hidden="true"></i></summary>
      <div class="wb"><div class="wg">{who_html}</div></div></details>
  </div>
</section>

<section style="background:var(--bg2);border-block:1px solid var(--line)">
  <div class="wrap tr">
    <div class="pw rv"><div class="por island"><span class="rg"></span><span class="rg"></span><span class="rg"></span><span class="tg2">{spark("x")}Claude Opus 5.5</span><span class="tg2 b"><img class='izi' src='izivoice-icon.png' alt='' width='22' height='22'>iziVoice</span><img src="roger.webp" alt="Roger BOUJIEKA" width="1000" height="1000" loading="lazy" decoding="async"><div class="nm"><div><b>Roger BOUJIEKA</b><span {t("tr_role","Votre formateur","Your trainer")}</span></div></div></div></div>
    <div class="rv d1">
      <span class="eye" {t("tr_eye","Le formateur","The trainer")}</span>
      <h2 class="h2" {t("tr_h","Je vous transmets<br><em>ce qui marche.</em>","I pass on<br><em>what works.</em>")}</h2>
      <p class="lead" {t("tr_p","Entrepreneur web, expert en intelligence artificielle, en montage vidéo, en motion design et en marketing digital. Je crée chaque jour des vidéos et des campagnes pour des marques, des entreprises et des églises.","Web entrepreneur, expert in artificial intelligence, video editing, motion design and digital marketing. Every day I create videos and campaigns for brands, companies and churches.")}</p>
      <div class="roles"><span {t("r1","Intelligence artificielle","Artificial intelligence")}</span><span {t("r2","Montage vidéo","Video editing")}</span><span {t("r3","Motion design","Motion design")}</span><span {t("r4","Marketing digital","Digital marketing")}</span></div>
      <div style="margin-top:26px"><a class="lnk" href="#formateur" data-v="formateur" {t("tr_more","Découvrir mon parcours","Discover my story")}</a></div>
    </div>
  </div>
</section>
''')
# remove odd badge in portrait name card
H[-1]=H[-1].replace('<span class="nw" style="position:static" aria-hidden="true">✳</span>','')

INC_FR=["<b>La formation complète</b> : 15 vidéos, 14 modules, 1 h 14","À suivre sur <b>smartphone ou ordinateur</b>","Le <b>cas pratique en direct</b> d'une vidéo motion de A à Z","Mon <b>modèle de prompt</b> et ma méthode des 8 ingrédients","Le <b>bonus monétisation</b> : offres, prix, premiers clients","Le <b>PDF</b> des présentations et les ressources"]
INC_EN=["<b>The full course</b>: 15 videos, 14 modules, 1 h 14","Follow it on a <b>smartphone or a computer</b>","The <b>live case study</b> of a motion video from A to Z","My <b>prompt template</b> and 8-ingredient method","The <b>monetisation bonus</b>: offers, prices, first clients","The slides <b>PDF</b> and resources"]
EN['inc_l']=''.join(f'<li><span>{x}</span></li>' for x in INC_EN)
A(f'''
<section id="offre">
  <div class="wrap">
    <div class="head c rv"><span class="eye" {t("of_eye","Votre accès","Your access")}</span><h2 class="h2" {t("of_h","Tout ce qu'il faut.<br><em>Un seul paiement.</em>","Everything you need.<br><em>One payment.</em>")}</h2></div>
    <div class="offer">
      <div>
        <div class="inc rv"><h3 {t("inc_h","Ce que vous recevez","What you get")}</h3><ul data-i18n="inc_l">{''.join(f'<li><span>{x}</span></li>' for x in INC_FR)}</ul><p class="inc-n" {t("inc_n","À prévoir pour créer : l'abonnement <b>Claude Pro</b> (≈ 12 000 FCFA/mois), présenté pas à pas au module 4. <a href=\"#abonnement\">Voir le calcul →</a>","To create, plan for the <b>Claude Pro</b> subscription (≈ 12,000 FCFA/month), shown step by step in module 4. <a href=\"#abonnement\">See the maths →</a>")}</p></div>
        {guarantees("gx")}
      </div>
      <div class="pc rv d1">
        <div class="top2"><span class="nm"><i class="pi">★</i><span {t("pc_nm","Formation Vibe Motion","Vibe Motion course")}</span></span><span class="off">−57 %</span></div>
        <div class="pr"><b>15 000</b><em>FCFA</em><s>35 000 FCFA</s></div>
        <p class="once" {t("pc_once","Paiement unique · accès à vie · sans abonnement","One-time payment · lifetime access · no subscription")}</p>
        {cdbox("o")}
        {btn("pc_cta","J'accède à la formation","Get the course","btn btn-red btn-lg btn-full")}
        <p class="after" {t("pc_after","🔒 Paiement sécurisé · accès immédiat après le paiement","🔒 Secure payment · instant access after payment")}</p>
        {METHODS}
        <div class="fxbox"><span class="js-fx2"></span><label class="fxsel"><span {t("fx_lbl","Voir le prix dans votre devise :","See the price in your currency:")}</span><select id="fx-cur"></select></label><small class="fxnote" hidden {t("fx_note","Montant indicatif. Le paiement se fait en FCFA ; la conversion finale dépend de votre moyen de paiement.","Indicative amount. Payment is made in FCFA; the final conversion depends on your payment method.")}</small><span class="js-fx" hidden></span></div>
      </div>
    </div>
  </div>
</section>


<section style="padding-top:0">
  <div class="wrap"><div class="commh rv">
    <span class="big"><svg viewBox="0 0 24 24" fill="currentColor"><use href="#i-wa"/></svg></span>
    <div><h2 {t("cm2_h","Rejoignez la communauté gratuite","Join the free community")}</h2><p {t("cm2_p","<b>LE DIGITAL POUR TOUS</b> : un groupe WhatsApp gratuit pour apprendre l'IA, le marketing digital et la création de contenu avec d'autres passionnés.","<b>LE DIGITAL POUR TOUS</b>: a free WhatsApp group to learn AI, digital marketing and content creation with other enthusiasts.")}</p>
      <div class="tags"><span {t("cm2_t1","Intelligence artificielle","Artificial intelligence")}</span><span {t("cm2_t2","Marketing digital","Digital marketing")}</span><span {t("cm2_t3","Création de contenu","Content creation")}</span></div></div>
    <a class="btn btn-green btn-lg" href="{WA_GROUP}" target="_blank" rel="noopener">{WAI}<span {t("cm2_b","Rejoindre gratuitement","Join for free")}</span></a>
  </div></div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="head c rv"><span class="eye">FAQ</span><h2 class="h2" {t("fq_h","Vos questions,<br><em>mes réponses.</em>","Your questions,<br><em>my answers.</em>")}</h2></div>
    <div class="faq rv">{faq_html([FAQ[0],FAQ[1],FAQ[5],FAQ[3],FAQ[2]],"fa")}</div>
    <div class="more"><a class="lnk" href="#faq" data-v="faq" {t("fq_more","Toutes les questions","All questions")}</a></div>
  </div>
</section>

<section class="final" style="padding-top:0">
  <div class="wrap"><div class="box island rv"><div class="clouds" aria-hidden="true"><i class="k1"></i><i class="k2"></i><i class="k3"></i><i class="k4"></i></div>
    <h2 {t("fn_h","Votre prochaine vidéo<br>peut être la meilleure.","Your next video<br>can be your best.")}</h2>
    <p {t("fn_p","Rejoignez Vibe Motion aujourd'hui : 15 000 FCFA au lieu de 35 000, accès à vie, mises à jour gratuites et accompagnement WhatsApp.","Join Vibe Motion today: 15,000 FCFA instead of 35,000, lifetime access, free updates and WhatsApp support.")}</p>
    {btn("fn_cta","Je rejoins la formation","Join the course","btn btn-lg")}
    <p class="mini"><span {t("fn_mini","⏳ L'offre se termine dans","⏳ Offer ends in")}</span> <b class="js-cd-hms">10:00:00</b></p>
  </div></div>
</section>
</div>
''')

# ================= FORMATION =================
A(f'''
<div class="view" id="v-formation" data-view="formation">
<section class="phead"><div class="wrap"><div class="head c" style="margin-bottom:0"><span class="eye" {t("pf_eye","Programme de la formation","Course programme")}</span><h1 class="h1" {t("pf_h","Vibe Motion : de zéro<br><em>à vos premiers clients.</em>","Vibe Motion: from zero<br><em>to your first clients.</em>")}</h1><p class="lead" {t("pf_p","Créez des vidéos motion, des affiches animées et des montages professionnels avec l'IA, sans logiciel de montage compliqué. Touchez un module pour voir son contenu.","Create motion videos, animated posters and professional edits with AI, without complicated editing software. Tap a module to see what's inside.")}</p></div></div></section>
<section style="padding-top:20px"><div class="wrap">
  <div class="pstats"><div><b>15</b><span {t("ps1","vidéos","videos")}</span></div><div><b>14</b><span {t("ps2","modules","modules")}</span></div><div><b>1 h 14</b><span {t("ps3","de formation","of training")}</span></div><div><b>2</b><span {t("ps4","outils IA : Claude et iziVoice","AI tools: Claude and iziVoice")}</span></div></div>
  <div class="mods">{mods_html}</div>
  <div class="need"><span class="eye" {t("nd_h","Ce dont vous avez besoin","What you need")}</span><ul data-i18n="nd_l"><li>Un smartphone ou un ordinateur (Windows ou Mac)</li><li>Une bonne connexion internet</li><li>Un compte Google</li><li>Le navigateur Google Chrome</li></ul><p {t("nd_p","Pour les vidéos longues avec beaucoup de rushs, l'ordinateur est plus confortable.","For long videos with lots of footage, a computer is more comfortable.")}</p></div>
  <div class="ctar">{btn("pf_cta","Je commence maintenant","Start now","btn btn-red btn-lg")}<p {t("pf_cp","<b>15 000 FCFA</b> au lieu de 35 000 · accès immédiat aux 15 vidéos","<b>15,000 FCFA</b> instead of 35,000 · instant access to all 15 videos")}</p></div>
</div></section>
</div>
''')
EN['nd_l']='<li>A smartphone or a computer (Windows or Mac)</li><li>A good internet connection</li><li>A Google account</li><li>The Google Chrome browser</li>'

# ================= FORMATEUR =================
A(f'''
<div class="view" id="v-formateur" data-view="formateur">
<section class="phead"><div class="wrap tr">
  <div class="pw"><div class="por island"><span class="rg"></span><span class="rg"></span><span class="rg"></span><span class="tg2">{spark("x")}Claude Opus 5.5</span><span class="tg2 b"><img class='izi' src='izivoice-icon.png' alt='' width='22' height='22'>iziVoice</span><img src="roger.webp" alt="Roger BOUJIEKA" width="1000" height="1000" decoding="async"><div class="nm"><div><b>Roger BOUJIEKA</b><span {t("fm_role","Fondateur de Boujieka Academy","Founder of Boujieka Academy")}</span></div></div></div></div>
  <div>
    <span class="eye" {t("fm_eye","Le formateur","The trainer")}</span>
    <h1 class="h1" style="font-size:clamp(40px,5.6vw,68px)">Roger<br><em>BOUJIEKA</em></h1>
    <p class="lead" {t("fm_p","Entrepreneur web, expert en intelligence artificielle, en montage vidéo, en motion design et en marketing digital. Je crée chaque jour des vidéos et des campagnes pour des marques, des entreprises et des églises, et je vous transmets exactement ce qui marche.","Web entrepreneur, expert in artificial intelligence, video editing, motion design and digital marketing. Every day I create videos and campaigns for brands, companies and churches, and I pass on exactly what works.")}</p>
    <div class="roles"><span {t("r1","Intelligence artificielle","Artificial intelligence")}</span><span {t("r2","Montage vidéo","Video editing")}</span><span {t("r3","Motion design","Motion design")}</span><span {t("r4","Marketing digital","Digital marketing")}</span></div>
    <div class="cos"><div><small>PDG</small>Boujieka Group</div><div><small>PDG</small>Boujieka Agency</div><div><small>PDG</small>Boujieka Academy</div></div>
    <p class="quote" {t("fm_q","« Responsable, et enfant de Dieu. »","“Responsible, and a child of God.”")}</p>
  </div>
</div></section>
<section style="padding-top:20px"><div class="wrap">
  <div class="head rv"><span class="eye" {t("fm_w_eye","Quelques réalisations","Some of my work")}</span><h2 class="h2" {t("fm_w_h","Des marques, des églises,<br><em>des événements.</em>","Brands, churches,<br><em>events.</em>")}</h2></div>
  <div class="rail js-rail">{works_html.replace('class="nw"','class="nw" hidden')}</div>
  <div class="ctar">{btn("fm_cta","Apprendre ma méthode","Learn my method","btn btn-red btn-lg")}</div>
</div></section>
</div>
''')

# ================= VISION =================
A(f'''
<div class="view" id="v-vision" data-view="vision">
<section class="phead"><div class="wrap"><div class="head c" style="margin-bottom:0"><span class="eye" {t("vi_eye","La vision","The vision")}</span><h1 class="h1" {t("vi_h","Le digital<br><em>pour tous.</em>","Digital<br><em>for everyone.</em>")}</h1><p class="lead" {t("vi_p","Une vidéo professionnelle ne devrait pas être réservée à ceux qui ont un gros budget ou un studio. Avec l'IA, chacun peut créer, communiquer et vivre de son talent.","A professional video shouldn't be reserved for those with a big budget or a studio. With AI, anyone can create, communicate and earn from their talent.")}</p></div></div></section>
<section style="padding-top:30px"><div class="wrap">
  <p class="mani rv" {t("vi_m","J'ai créé Vibe Motion pour que chaque entrepreneur, chaque église et chaque jeune puisse <em>raconter son histoire</em> avec la même qualité que les grandes marques, depuis l'appareil qu'il a déjà.","I created Vibe Motion so that every entrepreneur, every church and every young person can <em>tell their story</em> with the same quality as big brands, from the device they already have.")}</p>
  <div class="pillars" style="margin-top:50px">
    <div class="pil rv"><b>01</b><h3 {t("vi1h","Accessible","Accessible")}</h3><p {t("vi1p","Smartphone ou ordinateur, un prix juste et un paiement par Mobile Money. Personne ne doit rester à la porte.","Smartphone or computer, a fair price and Mobile Money payment. Nobody should be left out.")}</p></div>
    <div class="pil rv d1"><b>02</b><h3 {t("vi2h","Exigeant","Demanding")}</h3><p {t("vi2p","Des vidéos au niveau professionnel, pas des montages approximatifs. La même méthode que pour mes clients.","Professional-level videos, not rough edits. The same method I use for my clients.")}</p></div>
    <div class="pil rv d2"><b>03</b><h3 {t("vi3h","Libérateur","Empowering")}</h3><p {t("vi3p","Une compétence qui se vend : vous apprenez à créer, puis à trouver vos clients et à en vivre.","A skill that sells: you learn to create, then to find clients and earn from it.")}</p></div>
  </div>
  <div class="comm rv" style="margin-top:50px"><div><h3 {t("vi_ch","Rejoignez la communauté LE DIGITAL POUR TOUS","Join the LE DIGITAL POUR TOUS community")}</h3><p {t("vi_cp","Groupe WhatsApp gratuit : intelligence artificielle, marketing digital, création de contenu et bien plus.","Free WhatsApp group: artificial intelligence, digital marketing, content creation and more.")}</p></div><a class="btn btn-green" href="{WA_GROUP}" target="_blank" rel="noopener">{WAI}<span {t("vi_cb","Rejoindre gratuitement","Join for free")}</span></a></div>
  <div class="ctar">{btn("vi_cta","Je rejoins Vibe Motion","Join Vibe Motion","btn btn-red btn-lg")}</div>
</div></section>
</div>
''')

ADV=[('⚡','Accès immédiat','Vous commencez juste après le paiement.','Instant access','Start right after payment.'),
 ('📱','Smartphone ou ordinateur',"Avec l'appareil que vous avez déjà.",'Smartphone or computer','With the device you already have.'),
 ('🧭','Pas à pas, de zéro','Aucune expérience requise.','Step by step, from zero','No experience required.'),
 ('🎥','Cas pratique en direct','Une vraie vidéo réalisée devant vous.','Live case study','A real video made in front of you.'),
 ('🧩','Modèle de prompt','Prêt à réutiliser pour vos projets.','Prompt template','Ready to reuse for your projects.'),
 ('📄','PDF et ressources','Tout ce qu\'il faut pour avancer.','PDF and resources','Everything you need to move forward.'),
 ('💳','Mobile Money ou carte','Orange Money, MoMo, Moov, Visa, Mastercard.','Mobile Money or card','Orange Money, MoMo, Moov, Visa, Mastercard.'),
 ('💰','Bonus monétisation','Trouver vos clients et fixer vos prix.','Monetisation bonus','Find clients and set your prices.')]
adv=''.join(f'<div class="rv d{i%4}"><span class="e" aria-hidden="true">{e}</span><h3 {t(f"av{i}h",h,eh)}</h3><p {t(f"av{i}p",p,ep)}</p></div>' for i,(e,h,p,eh,ep) in enumerate(ADV))
CMP=[('Délai pour un spot de 90 s','4 à 8 heures','Plusieurs jours','≈ 24 minutes','Time for a 90-second ad','4 to 8 hours','Several days','≈ 24 minutes'),
 ('Coût','Logiciels + ordinateur puissant','Un paiement à chaque vidéo','15 000 FCFA, une fois','Cost','Software + powerful computer','A payment for every video','15,000 FCFA, once'),
 ('Voix off','À enregistrer soi-même','En supplément','Incluse avec iziVoice','Voice-over','Record it yourself','Extra charge','Included with iziVoice'),
 ('Formats 16:9 et 9:16','À refaire à la main','En supplément','Générés ensemble','16:9 and 9:16 formats','Redo by hand','Extra charge','Generated together'),
 ('Vous en vivez','Non','Non','Oui, module 14','You earn from it','No','No','Yes, module 14')]
rows=''.join(f'<tr><td {t(f"cm{i}a",a,ea)}</td><td {t(f"cm{i}b",b_,eb)}</td><td {t(f"cm{i}c",c,ec)}</td><td class="us" {t(f"cm{i}d",d,ed)}</td></tr>' for i,(a,b_,c,d,ea,eb,ec,ed) in enumerate(CMP))
A(f'''
<div class="view" id="v-avantages" data-view="avantages">
<section class="phead"><div class="wrap"><div class="head c" style="margin-bottom:0"><span class="eye" {t("av_eye","Avantages","Benefits")}</span><h1 class="h1" {t("av_h","Tout est pensé<br><em>pour que vous réussissiez.</em>","Everything is designed<br><em>for your success.</em>")}</h1></div></div></section>
<section style="padding-top:30px"><div class="wrap">
  <div class="gbig">
    <div class="g rv"><span class="gi">{INF}</span><h3 {t("g1h","Accès à vie","Lifetime access")}</h3><p {t("gb1","Payez une seule fois et gardez la formation pour toujours. Regardez et revoyez chaque vidéo autant que vous voulez.","Pay once and keep the course forever. Watch and rewatch every video as often as you like.")}</p></div>
    <div class="g rv d1"><span class="gi">{UPD}</span><h3 {t("g2h","Mises à jour gratuites à vie","Free lifetime updates")}</h3><p {t("gb2","La formation évolue avec les outils d'IA. Chaque nouveau module et chaque mise à jour vous sont offerts, sans rien payer de plus.","The course evolves with AI tools. Every new module and update is yours, at no extra cost.")}</p></div>
    <div class="g rv d2"><span class="gi">{WAI}</span><h3 {t("g3h","Accompagnement garanti","Guaranteed support")}</h3><p {t("gb3","Dans le groupe WhatsApp privé, vous posez vos questions et je vous accompagne pendant toute votre progression.","In the private WhatsApp group, you ask questions and I support you all the way.")}</p></div>
  </div>
  <div class="head c rv" style="margin-top:80px"><span class="eye" {t("av2_eye","Inclus","Included")}</span><h2 class="h2" {t("av2_h","Et aussi…","And also…")}</h2></div>
  <div class="adv">{adv}</div>
  <div class="head c rv" style="margin-top:80px"><span class="eye" {t("cm_eye","Comparatif","Comparison")}</span><h2 class="h2" {t("cm_h","Pourquoi <em>Vibe Motion</em> ?","Why <em>Vibe Motion</em>?")}</h2></div>
  <div class="cmpw rv"><table class="cmp"><thead><tr><th></th><th {t("cmh1","Montage classique","Classic editing")}</th><th {t("cmh2","Payer un monteur","Hire an editor")}</th><th class="us">Vibe Motion</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="ctar">{btn("av_cta","Je profite de l'offre","Claim the offer","btn btn-red btn-lg")}<p {t("av_cp","<b>15 000 FCFA</b> au lieu de 35 000 · paiement unique","<b>15,000 FCFA</b> instead of 35,000 · one-time payment")}</p></div>
</div></section>
</div>

<div class="view" id="v-faq" data-view="faq">
<section class="phead"><div class="wrap"><div class="head c" style="margin-bottom:0"><span class="eye">FAQ</span><h1 class="h1" {t("fq2_h","Questions<br><em>fréquentes.</em>","Frequently asked<br><em>questions.</em>")}</h1></div></div></section>
<section style="padding-top:30px"><div class="wrap">
  <div class="faq">{faq_html(FAQ,"fb")}</div>
  <div class="ctar"><p {t("fq2_p","Une autre question ? Écrivez-moi sur WhatsApp.","Another question? Message me on WhatsApp.")}</p><a class="btn btn-green" href="{WA_DM}" target="_blank" rel="noopener">{WAI}<span {t("fq2_b","Poser ma question","Ask my question")}</span></a></div>
</div></section>
</div>
</main>

<footer class="foot"><div class="wrap island">
  <div><img class="lg lg-d" src="logo_rb.png" alt="Roger BOUJIEKA" loading="lazy"><img class="lg lg-l" src="logo_rb_dk.png" alt="Roger BOUJIEKA" loading="lazy"><p {t("ft_p","Vibe Motion · la formation de Roger BOUJIEKA pour créer des spots, des motion designs et des affiches animées avec l'intelligence artificielle, sur smartphone ou ordinateur.","Vibe Motion · Roger BOUJIEKA's course for creating ads, motion designs and animated posters with artificial intelligence, on a smartphone or a computer.")}</p><div class="cta">{btn("ft_cta","Je rejoins la formation","Join the course")}</div></div>
  <div><h4 {t("ft_nav","Navigation","Navigation")}</h4><ul>{''.join(f'<li><a href="#{k}" data-v="{k}" {t("nav_"+k,fr,en)}</a></li>' for k,fr,en in NAV)}</ul></div>
  <div><h4 {t("ft_fo","La formation","The course")}</h4><ul><li><a href="#realisations" {t("ft_l1","Réalisations","Portfolio")}</a></li><li><a href="#abonnement" {t("ft_l2","Abonnement Claude","Claude subscription")}</a></li><li><a href="#offre" {t("ft_l3","Prix et offre","Price and offer")}</a></li><li><a href="#formation" {t("ft_l4","Programme complet","Full programme")}</a></li><li><a href="{WA_GROUP}" target="_blank" rel="noopener" {t("ft_l5","Communauté WhatsApp","WhatsApp community")}</a></li></ul></div>
  <div><h4 {t("ft_ct","Contact","Contact")}</h4><ul class="ct">
    <li><a href="{WA_DM}" target="_blank" rel="noopener"><span class="i" style="background:#25d366">{WAI}</span><span>WhatsApp<small {t("ft_c1","Réponse rapide","Quick reply")}</small></span></a></li>
    <li><a href="tel:+237678594247"><span class="i" style="background:#e3061b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg></span><span {t("ft_c2","Appeler<small>Téléphone</small>","Call<small>Phone</small>")}</span></a></li>
    <li><a href="mailto:rogerboujieka237@gmail.com"><span class="i" style="background:#3d8bfd"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 6 9 7 9-7"/></svg></span><span {t("ft_c3","E-mail<small>Écrivez-moi</small>","Email<small>Write to me</small>")}</span></a></li>
  </ul></div>
  <div class="fbar"><div><span class="pl" {t("ft_pay","Paiement sécurisé","Secure payment")}</span>{METHODS}</div><div><span class="pl" {t("ft_pa","Partenaires","Partners")}</span><div class="partners"><img class="lg-d" loading="lazy" src="logo_transmission.png" alt="TRANSMISSION"><img class="lg-l" loading="lazy" src="logo_transmission_dk.png" alt="TRANSMISSION"><img class="lg-d" loading="lazy" src="logo_boujieka_agency.png" alt="Boujieka Agency"><img class="lg-l" loading="lazy" src="logo_boujieka_agency_dk.png" alt="Boujieka Agency"><img class="lg-d" loading="lazy" src="logo_izivoice.png" alt="iziVoice"><img class="lg-l" loading="lazy" src="logo_izivoice_darktext.png" alt="iziVoice"></div></div></div>
  <p class="legal" {t("ft_l","© 2026 Roger BOUJIEKA · Boujieka Academy. Claude et Opus sont des marques d'Anthropic ; formation indépendante, non affiliée à Anthropic.","© 2026 Roger BOUJIEKA · Boujieka Academy. Claude and Opus are trademarks of Anthropic; independent course, not affiliated with Anthropic.")}</p>
</div></footer>

<div class="mbar island" id="mbar"><div class="p"><span class="pr">15 000 FCFA<small>⏳ <span class="js-cd-hms">10:00:00</span></small></span><small {t("mb_s","AU LIEU DE 35 000 FCFA","INSTEAD OF 35,000 FCFA")}</small></div>{btn("mb_cta","Je m'inscris","Enrol now")}</div>
<a class="wa" href="{WA_DM}" target="_blank" rel="noopener" aria-label="WhatsApp">{WAI}</a>
<div class="toast island" id="toast" role="status" aria-live="polite" hidden><span class="t-ic"></span><span class="t-tx"><b></b><small></small></span><button class="t-x" type="button" aria-label="Fermer">✕</button></div>
''')
html='\n'.join(H)
# keep numbers like "12 000 FCFA" on one line
def _nb(m):
    s=m.group(0)
    s=re.sub(r'(?<=\d) (?=000\b)', ' ', s)
    return re.sub(r'(?<=000) (?=FCFA)', ' ', s)
html=re.sub(r'>[^<]+<', _nb, html)
html=re.sub(r'>[^<]*≈ [^<]*<', lambda m: m.group(0).replace('≈ ', '≈\u00a0'), html)  # visible text only, never inside tags or SVG paths
js=open(f'{SP}/v2/app.js').read()
js=js.replace('/*EN*/{}', json.dumps(EN,ensure_ascii=False)).replace('/*ROTFR*/[]',json.dumps(ROT_FR,ensure_ascii=False)).replace('/*ROTEN*/[]',json.dumps(ROT_EN,ensure_ascii=False)).replace('/*CTA*/""',json.dumps(CTA))
js=js.replace('/*YT*/',open(f'{SP}/yt.js').read()).replace('/*FX*/',open(f'{SP}/fx.js').read()).replace('/*TOAST*/',open(f'{SP}/toast.js').read().replace("document.getElementById('offre').scrollIntoView({ behavior: 'smooth' })","goTo('offre')"))
html+=f'<script>\n{js}\n</script>\n</body>\n</html>\n'
open(f'{REPO}/index.html','w',encoding='utf-8').write(html)
print('written', len(html), 'keys', len(EN))
