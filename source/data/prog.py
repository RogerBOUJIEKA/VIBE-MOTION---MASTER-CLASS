import re, json
p='/home/user/vibe-motion---master-class/index.html'; s=open(p,encoding='utf-8').read()
def rep(a,b,c=1):
    global s
    assert s.count(a)==c,(a[:80],s.count(a)); s=s.replace(a,b)
M=[ # num, dur, fr title, fr sub, fr desc, en title, en sub, en desc, flag
('00','0 min 52','Bienvenue dans Vibe Motion','Introduction',
 "Découvrez votre formateur, ce que vous serez capable de réaliser à la fin de la formation, les deux outils que nous allons utiliser (Claude et iziVoice) et le programme complet des 14 modules.",
 'Welcome to Vibe Motion','Introduction',"Meet your trainer, see what you will be able to make by the end, the two tools we will use (Claude and iziVoice) and the full 14-module programme.",''),
('01','1 min 20','Installer Claude',"L'application sur votre ordinateur",
 "On vérifie d'abord les 4 prérequis : un ordinateur, une bonne connexion, un compte Google et Google Chrome. Ensuite, vous téléchargez et installez l'application Claude, étape par étape.",
 'Install Claude','The app on your computer',"First we check the 4 requirements: a computer, a good connection, a Google account and Google Chrome. Then you download and install the Claude app, step by step.",''),
('02','2 min 06',"L'extension Claude",'Claude dans Google Chrome',
 "Comprenez à quoi sert l'extension et en quoi elle diffère de l'application : l'application crée les vidéos, l'extension vous accompagne sur le web, par exemple pour analyser le site d'un client. Puis installez-la depuis le Chrome Web Store et épinglez-la.",
 'The Claude extension','Claude in Google Chrome',"Understand what the extension is for and how it differs from the app: the app creates the videos, the extension helps you on the web, for example to analyse a client's website. Then install it from the Chrome Web Store and pin it.",''),
('03','7 min 59','Organiser votre projet','Le dossier qui guide Claude',
 "Le cœur de la méthode. Vous créez le dossier de projet que Claude va lire, avec ses 5 sous-dossiers numérotés : vidéos de référence, fonds sonores, éléments, rushs et effets sonores. Vous comprenez pourquoi la vidéo de référence est essentielle et comment bien nommer vos fichiers, avec deux exemples concrets : un spot publicitaire et un film de mariage.",
 'Organise your project','The folder that guides Claude',"The heart of the method. You build the project folder Claude reads, with its 5 numbered sub-folders: reference videos, soundtracks, elements, footage and sound effects. You learn why the reference video matters and how to name your files, with two real examples: an ad and a wedding film.",'key'),
('04','5 min 42','Votre compte et le forfait Pro','Se connecter et s’abonner',
 "La différence entre Claude Web et l'application, la connexion avec votre compte Google (et dans quel ordre la faire pour éviter les blocages), puis la comparaison des forfaits Gratuit, Pro et Max. Vous souscrivez au forfait Pro pas à pas, avec une astuce pour payer par carte Visa virtuelle (Orange Money, Mobile Money) et une checklist pour réussir votre paiement du premier coup.",
 'Your account and the Pro plan','Sign in and subscribe',"Claude Web versus the app, signing in with Google (and in which order to avoid blocks), then Free, Pro and Max compared. You subscribe to Pro step by step, with a tip to pay with a virtual Visa card (Orange Money, Mobile Money) and a checklist to get the payment right first time.",''),
('05','1 min 17',"Activer l'extension",'Relier Claude dans Chrome à votre compte',
 "Connectez l'extension Chrome à votre compte Claude avec le même compte Google. Si elle refuse de se connecter, vous avez les 4 vérifications qui règlent le problème dans la grande majorité des cas.",
 'Activate the extension','Link Claude in Chrome to your account',"Connect the Chrome extension to your Claude account with the same Google account. If it won't connect, you get the 4 checks that fix it in most cases.",''),
('06','10 min 29','Claude Code : dossier et prompt','Votre dossier + votre prompt',
 "Place à la pratique dans l'onglet Code : vous sélectionnez votre dossier de projet et écrivez votre prompt. Vous apprenez à le dicter au micro, ma méthode des 8 ingrédients d'un bon prompt, mon modèle prêt à réutiliser, la différence entre un prompt faible et un prompt efficace, et comment ajouter des consignes pendant que Claude travaille.",
 'Claude Code: folder and prompt','Your folder + your prompt',"Hands-on in the Code tab: you select your project folder and write your prompt. You learn to dictate it, my 8-ingredient method for a good prompt, my reusable template, weak versus effective prompts, and how to add instructions while Claude works.",'key'),
('07','8 min 54','Connecter iziVoice','Des voix off professionnelles',
 "Donnez des voix off naturelles et professionnelles à vos vidéos. Vous découvrez les connecteurs de Claude, la plateforme iziVoice et ses forfaits, puis vous connectez iziVoice à Claude en 5 étapes. En bonus : décrire la voix off idéale (genre, ton, langue, accent, voix clonée) et gérer vos crédits (qualité HD ou Eco).",
 'Connect iziVoice','Professional voice-overs',"Give your videos natural, professional voice-overs. You discover Claude connectors, the iziVoice platform and its plans, then connect iziVoice to Claude in 5 steps. Bonus: describing the ideal voice (gender, tone, language, accent, cloned voice) and managing credits (HD or Eco).",''),
('08','7 min 49','Cas pratique : vidéo motion','Une vidéo motion de A à Z',
 "Le cas pratique en direct : une vidéo motion d'1 min 20 créée uniquement à partir du lien du site Allociné et d'une vidéo de référence, en version YouTube (16:9) et Short (9:16). Vous me voyez dicter le prompt, envoyer la référence, répondre aux questions de Claude et ajouter la voix off, jusqu'au résultat final.",
 'Case study: motion video','A motion video from A to Z',"The live case study: a 1 min 20 motion video made only from the Allociné website link and a reference video, in YouTube (16:9) and Short (9:16) versions. You watch me dictate the prompt, send the reference, answer Claude's questions and add the voice-over, right to the final result.",'live'),
('09','6 min 09','Ma méthode : motion à partir d’un lien',"Pas à pas, de l'analyse à la livraison",
 "La méthode complète en 7 étapes pour reproduire le cas pratique sur n'importe quel site : analyser le site, choisir la bonne référence, écrire le prompt, ajouter les détails qui font la différence (couleurs, logo, arrière-plan animé, effets sonores, appel à l'action), suivre la création, vérifier le rendu comme un client et demander des retouches précises.",
 'My method: motion from a link','Step by step, from analysis to delivery',"The full 7-step method to repeat the case study on any website: analyse the site, pick the right reference, write the prompt, add the details that make the difference (colours, logo, animated background, sound effects, call to action), follow the build, check it like a client and ask for precise edits.",''),
('10','4 min 09','Motion à partir d’une affiche','Transformer une image en vidéo',
 "Un service très demandé : transformer l'affiche d'un client (concert, conférence, promotion, croisade…) en vidéo animée pour les réseaux sociaux et les statuts WhatsApp. Préparation du dossier, prompt pour « découper » l'affiche, exemple scène par scène et conseils pour une affiche animée réussie.",
 'Motion from a poster','Turn an image into a video',"A service in high demand: turning a client's poster (concert, conference, promotion, crusade…) into an animated video for social media and WhatsApp statuses. Folder prep, the prompt to “cut up” the poster, a scene-by-scene example and tips for a great animated poster.",''),
('11','7 min 22','Réaliser une vidéo longue','Mariages, YouTube, spots avec rushs',
 "Montez des vidéos à partir de vos propres images : mariages, anniversaires, vidéos YouTube, spots avec rushs, formations. Vous préparez vos rushs, choisissez le son principal, écrivez le prompt et guidez Claude sur le placement des séquences. Avec des exemples concrets et les limites à connaître.",
 'Make a long video','Weddings, YouTube, ads with footage',"Edit videos from your own footage: weddings, birthdays, YouTube videos, ads with footage, courses. You prepare your footage, choose the main audio, write the prompt and guide Claude on placing the shots. With real examples and the limits to know.",''),
('12','3 min 09','Retouches et livraison','Livrer comme un professionnel',
 "Formuler des retours précis pour tout corriger en une seule fois, choisir les versions à livrer (16:9, 9:16, 1 min 30 pour les statuts, autres langues), signer votre travail avec une signature animée, votre checklist de livraison et la bonne façon de gérer les demandes de modification.",
 'Edits and delivery','Deliver like a pro',"Write precise feedback to fix everything in one go, choose the versions to deliver (16:9, 9:16, 1 min 30 for statuses, other languages), sign your work with an animated signature, your delivery checklist and how to handle change requests.",''),
('13','1 min 43','Trouver l’inspiration','Où chercher vos vidéos de référence',
 "Où trouver vos vidéos de référence sur TikTok, Instagram et Facebook, quels mots-clés taper, pourquoi travailler depuis votre ordinateur, et comment construire votre bibliothèque d'inspiration classée par type de projet.",
 'Find inspiration','Where to find reference videos',"Where to find reference videos on TikTok, Instagram and Facebook, which keywords to type, why to work from your computer, and how to build your own inspiration library by project type.",''),
('14','5 min 22','Monétiser votre compétence','Transformer ce savoir en revenus',
 "Qui a besoin de vidéos, quelles offres vendre (de l'affiche animée au pack mensuel), comment fixer vos prix et trouver vos premiers clients. Avec un exemple de message WhatsApp pour présenter votre offre, le parcours client professionnel (brief, devis, acompte, livraison), les clés pour fidéliser et votre plan d'action sur 5 jours.",
 'Monetise your skill','Turn this know-how into income',"Who needs videos, which offers to sell (from animated posters to monthly packs), how to set your prices and find your first clients. With a sample WhatsApp message to pitch your offer, the professional client journey (brief, quote, deposit, delivery), the keys to keep clients and your 5-day action plan.",'money'),
]
EN={}
flagFR={'key':'Essentiel','live':'Cas pratique','money':'Revenus'}
flagEN={'key':'Key','live':'Case study','money':'Income'}
items=[]
for i,(n,d,ft,fs,fd,et,es,ed,fl) in enumerate(M):
    k=f'pm{i}'
    kick=('Introduction' if n=='00' else f'Module {int(n)}')
    EN[k+'t']=et; EN[k+'s']=es; EN[k+'d']=ed
    badge=f'<span class="pm-f pm-{fl}" data-i18n="pmf_{fl}">{flagFR[fl]}</span>' if fl else ''
    items.append(
f'''        <details class="pm{' pm-hl' if fl=='money' else ''}"{' open' if i==0 else ''}><summary><span class="pm-n">{n}</span><span class="pm-b"><span class="pm-k">{kick} · {d}{badge}</span><b data-i18n="{k}t">{ft}</b><span class="pm-s" data-i18n="{k}s">{fs}</span></span><i class="pm-x" aria-hidden="true"></i></summary><p data-i18n="{k}d">{fd}</p></details>''')
for f in flagEN: EN['pmf_'+f]=flagEN[f]
sec=f'''<!-- COURSE PROGRAMME -->
<section id="programme" class="pgx">
  <div class="wrap">
    <div class="head center rv"><span class="eyebrow" data-i18n="px_eye">Programme de la formation</span><h2 data-i18n="px_h">Vibe Motion : de zéro à vos premiers clients.</h2><p class="lead" data-i18n="px_p">Créez des vidéos motion, des affiches animées et des montages professionnels avec l'IA, sans logiciel de montage compliqué. 14 modules pas à pas, de l'installation jusqu'à vos premiers clients.</p></div>
    <div class="px-stats rv">
      <div><b>15</b><span data-i18n="px_s1">vidéos</span></div>
      <div><b>14</b><span data-i18n="px_s2">modules</span></div>
      <div><b>1 h 14</b><span data-i18n="px_s3">de formation</span></div>
      <div><b>2</b><span data-i18n="px_s4">outils IA : Claude et iziVoice</span></div>
    </div>
    <div class="px-list rv">
      <i class="px-line" aria-hidden="true"><i class="js-pxfill"></i></i>
{chr(10).join(items)}
    </div>
    <div class="px-need rv"><span class="px-nl" data-i18n="px_need">Ce dont vous avez besoin</span><ul data-i18n="px_need_l"><li>Un ordinateur (Windows ou Mac)</li><li>Une bonne connexion internet</li><li>Un compte Google</li><li>Le navigateur Google Chrome</li></ul></div>
    <div class="px-cta rv"><a class="btn btn-red js-cta" href="https://rogerboujieka237.mychariow.shop/prd_gy9104l1/checkout"><span data-i18n="px_cta">Je commence maintenant</span><span class="arr">→</span></a><p data-i18n="px_cta_p"><b>15 000 FCFA</b> au lieu de 25 000 · accès immédiat aux 15 vidéos</p></div>
  </div>
</section>

'''
rep('<!-- WHAT YOU NEED: PHONE -->', sec+'<!-- WHAT YOU NEED: PHONE -->')
EN.update({'px_eye':'Course programme','px_h':'Vibe Motion: from zero to your first clients.',
 'px_p':"Create motion videos, animated posters and professional edits with AI, without complicated editing software. 14 step-by-step modules, from setup to your first clients.",
 'px_s1':'videos','px_s2':'modules','px_s3':'of training','px_s4':'AI tools: Claude and iziVoice','px_need':'What you need',
 'px_need_l':'<li>A computer (Windows or Mac)</li><li>A good internet connection</li><li>A Google account</li><li>The Google Chrome browser</li>',
 'px_cta':'Start now','px_cta_p':'<b>15,000 FCFA</b> instead of 25,000 · instant access to all 15 videos'})
add=', '.join(f'{k}:{json.dumps(v,ensure_ascii=False)}' for k,v in EN.items())
rep('f7s:"Mobile app · motion design"','f7s:"Mobile app · motion design", '+add)
css=r'''/* course programme: glass cards on a dark brand background */
.pgx{color:#fff;background:radial-gradient(60% 50% at 0% 0%,rgba(227,6,27,.28),transparent 70%),radial-gradient(50% 45% at 100% 60%,rgba(227,6,27,.2),transparent 70%),linear-gradient(180deg,#0b0b10,#07070a);overflow:hidden}
.pgx .eyebrow{color:#ff5a68}.pgx h2{color:#fff}.pgx .lead{color:rgba(255,255,255,.72)}
.px-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:860px;margin:0 auto 34px}
@media (min-width:760px){.px-stats{grid-template-columns:repeat(4,1fr)}}
.px-stats div{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:16px 10px;border-radius:18px;text-align:center;background:rgba(255,255,255,.06);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12),inset 0 1px 0 rgba(255,255,255,.14)}
.px-stats b{font:400 30px/1 var(--display);color:#fff}
.px-stats span{font:600 12.5px/1.3 var(--body);color:rgba(255,255,255,.7)}
.px-list{position:relative;display:grid;gap:12px;max-width:860px;margin:0 auto;padding-left:22px}
.px-line{position:absolute;left:6px;top:24px;bottom:24px;width:3px;border-radius:3px;background:rgba(255,255,255,.12)}
.px-line i{display:block;width:100%;height:0;border-radius:inherit;background:linear-gradient(#ff5a68,#e3061b);box-shadow:0 0 14px rgba(227,6,27,.8)}
.pm{position:relative;border-radius:18px;background:rgba(255,255,255,.055);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.11),inset 0 1px 0 rgba(255,255,255,.12);transition:background .25s,box-shadow .25s}
.pm::before{content:"";position:absolute;left:-21px;top:30px;width:11px;height:11px;border-radius:50%;background:#0b0b10;box-shadow:0 0 0 2px rgba(255,255,255,.35)}
.pm[open]{background:rgba(255,255,255,.085);box-shadow:inset 0 0 0 1px rgba(227,6,27,.6),0 16px 40px rgba(0,0,0,.35)}
.pm[open]::before,.pm.done::before{background:#e3061b;box-shadow:0 0 0 2px #e3061b,0 0 12px rgba(227,6,27,.9)}
.pm.pm-hl{background:linear-gradient(135deg,rgba(227,6,27,.22),rgba(255,255,255,.05));box-shadow:inset 0 0 0 1px rgba(227,6,27,.55)}
.pm summary{display:flex;align-items:center;gap:14px;padding:16px 16px;cursor:pointer;list-style:none}
.pm summary::-webkit-details-marker{display:none}
.pm-n{flex:none;display:grid;place-items:center;width:46px;height:46px;border-radius:14px;font:400 18px/1 var(--display);color:#fff;background:linear-gradient(180deg,#f0182c,#c00418);box-shadow:0 8px 20px rgba(227,6,27,.35),inset 0 1px 0 rgba(255,255,255,.3)}
.pm-b{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px}
.pm-k{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font:700 11px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.55)}
.pm-b b{font:800 17px/1.25 var(--body);color:#fff}
.pm-s{font:500 13.5px/1.35 var(--body);color:rgba(255,255,255,.66)}
.pm-f{padding:4px 8px;border-radius:999px;font:800 10px/1 var(--body);letter-spacing:.04em;text-transform:none;color:#fff;background:rgba(255,255,255,.14)}
.pm-f.pm-live{background:#e3061b}.pm-f.pm-money{background:#1ea952}.pm-f.pm-key{background:rgba(255,255,255,.18)}
.pm-x{flex:none;position:relative;width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.1);transition:transform .3s var(--ease),background .25s}
.pm-x::before,.pm-x::after{content:"";position:absolute;left:50%;top:50%;width:12px;height:2px;margin:-1px 0 0 -6px;border-radius:2px;background:#fff}
.pm-x::after{transform:rotate(90deg)}
.pm[open] .pm-x{transform:rotate(45deg);background:#e3061b}
.pm p{margin:0;padding:0 18px 18px 76px;font:500 15px/1.6 var(--body);color:rgba(255,255,255,.78)}
@media (max-width:520px){.pm p{padding-left:18px}.pm summary{gap:12px;padding:14px}.pm-n{width:40px;height:40px;font-size:16px}.pm-b b{font-size:16px}}
.px-need{max-width:860px;margin:26px auto 0;padding:18px 20px;border-radius:18px;background:rgba(255,255,255,.05);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)}
.px-nl{font:700 12px/1.2 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#ff5a68}
.px-need ul{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;margin:12px 0 0;padding:0;list-style:none}
.px-need li{position:relative;padding-left:22px;font:600 14px/1.4 var(--body);color:rgba(255,255,255,.85)}
.px-need li::before{content:"";position:absolute;left:0;top:3px;width:14px;height:14px;border-radius:50%;background:#e3061b}
@media (max-width:520px){.px-need ul{grid-template-columns:1fr}}
.px-cta{display:flex;flex-direction:column;align-items:center;gap:12px;margin-top:30px;text-align:center}
.px-cta .btn{margin-top:0}
.px-cta p{margin:0;font:600 14px/1.4 var(--body);color:rgba(255,255,255,.7)}.px-cta p b{color:#fff}
/* latest works, shown high on the page */'''
rep('/* latest works, shown high on the page */',css)
js=r'''/* ---------- programme: one module open at a time, red line fills while scrolling ---------- */
(function () {
  const list = document.querySelector('.px-list'); if (!list) return;
  const mods = [...list.querySelectorAll('.pm')], fill = list.querySelector('.js-pxfill');
  list.addEventListener('toggle', e => { const d = e.target; if (!d.classList || !d.classList.contains('pm') || !d.open) return; mods.forEach(o => { if (o !== d) o.open = false; }); }, true);
  let raf = 0;
  function upd() { raf = 0; const r = list.getBoundingClientRect(), mid = innerHeight * 0.6;
    const k = Math.max(0, Math.min(1, (mid - r.top) / r.height)); fill.style.height = (k * 100) + '%';
    mods.forEach(m => m.classList.toggle('done', m.getBoundingClientRect().top + 30 < mid)); }
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true }); upd();
})();

/* ---------- "see all my work" opens the works tab ---------- */'''
rep('/* ---------- "see all my work" opens the works tab ---------- */',js)
open(p,'w',encoding='utf-8').write(s)
print('ok')
