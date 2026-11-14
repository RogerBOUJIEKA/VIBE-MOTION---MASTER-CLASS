# Vibe Motion — dossier de reprise du projet

Landing page de la formation **Vibe Motion** (montage vidéo et motion design avec l'IA), en ligne sur **www.rogerboujieka.com**.
Ce dossier contient tout ce qu'il faut pour continuer le travail depuis un autre compte, sans rien perdre.

> Pour reprendre avec un assistant (Claude Code) : ouvrir ce dépôt, puis lui dire
> **« Lis source/README.md et continue le projet. »**

## 1. Comment le site est fabriqué

Le site est **un seul fichier statique `index.html`**, généré par `source/build.py`. Il n'y a pas de `package.json` à la racine : Vercel publie les fichiers tels quels (et ne compile rien).

```
index.html            ← généré, ne pas modifier à la main
api/checkout.js       ← fonction serveur Vercel (paiement SasPay)
assets/ fonts/ pay/   ← bibliothèques (GSAP, Lenis, Three.js), polices, logos de paiement
source/
  build.py            ← construit index.html (textes FR/EN, structure, images)
  style.css           ← tout le design
  app.js              ← tout le comportement (lecteur vidéo, paiement, promo, compte à rebours…)
  data/               ← programme, FAQ, bandeau défilant, petits scripts (compte à rebours, devises, notifications, audio)
  icons/              ← les icônes Hugeicons utilisées (copiées, pas besoin de npm)
  tests/              ← tests automatiques (Playwright)
  tools/              ← image de partage, visuels publicitaires, pastilles de paiement
```

`source/` n'est **pas publié** sur le site (voir `.vercelignore`).

### Reconstruire et prévisualiser

```bash
python3 source/build.py                 # écrit index.html à la racine
python3 -m http.server 8765             # puis ouvrir http://localhost:8765
```

### Publier

Vercel déploie automatiquement la branche **`main`** du dépôt. Après `build.py` : commit, puis `git push origin main`. Le déploiement prend environ 1 minute.

### Tests (Playwright)

```bash
npm i playwright && npx playwright install chromium     # une seule fois
python3 -m http.server 8765 &                            # serveur local, depuis la racine du dépôt
node source/tests/ft4.js          # site complet (119 vérifications)
node source/tests/cotest.js out   # parcours de paiement + page « Merci » (24)
node source/tests/apitest.js      # fonction serveur api/checkout.js (18)
node source/tests/promo.js out    # fenêtre promo (20)
node source/tests/vptest.js out   # lecteur vidéo ordinateur (26)
node source/tests/vptest-phone.js out   # lecteur vidéo téléphone (16)
node source/tests/hero2.js out    # haut de page, plusieurs largeurs
node source/tests/cls.js          # décalages de mise en page (doit rester à 0)
node source/tests/contrast.js 4.5 # lisibilité (les 2 alertes « Montage classique » sont des faux positifs connus)
```

Le dossier de sortie (`out`) doit exister. YouTube et les sites externes sont bloqués ou simulés dans les tests.

## 2. Secrets : jamais dans le code

Le dépôt est **public**. Aucune clé n'y figure et aucune ne doit y entrer.
Les réglages se font dans **Vercel → projet `vibemotion` → Settings → Environment Variables**, puis **Redeploy** :

| Variable | Rôle |
|---|---|
| `SASPAY_SECRET_KEY` | clé secrète SasPay `sk_live_…` (droit **PAYIN** seulement) |
| `COURSE_ACCESS_URL` | lien de la formation, affiché **uniquement** après un paiement confirmé |
| `COURSE_GROUP_URL` | lien du groupe WhatsApp des élèves, idem |
| `SASPAY_AMOUNT` | (facultatif) prix en FCFA, défaut **5500** |
| `SASPAY_CURRENCY` | (facultatif) devise, défaut `XOF` |

Si la clé a été collée dans un chat ou un document, la **supprimer et en créer une nouvelle** dans SasPay (app.saspay.me → Développeur).

## 3. Paiement (SasPay)

- Les boutons « Je m'inscris » ouvrent un petit formulaire (prénom, nom, e-mail, WhatsApp facultatif) puis `POST /api/checkout` : le serveur crée une session SasPay (`/checkout-sessions/`, prix fixé côté serveur) et renvoie `checkout_url`.
- Retour : `https://www.rogerboujieka.com/?paiement=merci`. Le site interroge `GET /api/checkout?session=<id>` (qui appelle `/checkout-sessions/{id}/status/`). **Seul un paiement `PAID` + `SUCCESS` révèle** le lien de la formation et celui du groupe.
- Tant que `SASPAY_SECRET_KEY` n'est pas défini, les boutons envoient vers le lien **Chariow** de secours (constante `CTA` dans `build.py`). Penser à y aligner le prix.
- Documentation SasPay : https://docs.saspay.me (`/llms.txt` et `/api-reference/openapi.json` font foi).
- À savoir : pas de base de données ; les infos du formulaire vont chez SasPay (Transactions / Sessions de checkout, export CSV).

## 4. État actuel du site

- **Grande promo :** 5 500 FCFA, prix barré 25 000 (−78 %), compte à rebours de 24 h par visiteur (localStorage + cookie). Textes dans `build.py` (chercher `5 500`, `25 000`, `−78`).
- **Fenêtre promo carrée** (`#pp`) : 12 s après l'arrivée, puis 40 s après chaque fermeture ; jamais sur un formulaire, une vidéo ou le menu (`app.js`, bloc « Promo card »).
- **Bandeau « communauté gratuite » du haut : en pause.** Pour le rallumer : dans `app.js`, `const SHOW_COMMUNITY_BAR = true;`.
- **Haut de page téléphone = version ordinateur** (titre, vidéo de présentation YouTube `Ew-ZgqctuxQ`, boutons, atouts, offre), sans la photo.
- **Lecteur vidéo sur mesure** (`#vp`) : aperçu muet automatique (sauf connexion 2G / économiseur de données), son au clic, ±10 s, vitesse, plein écran, écran de fin avec bouton.
- **Pixel Meta** `1454801303232892` : PageView, InitiateCheckout, AddPaymentInfo, Purchase (valeur 5500), Lead, Contact.
- Liens WhatsApp (groupe gratuit, message direct) : constantes `WA_GROUP` et `WA_DM` dans `build.py`.
- Image de partage : `og-vibe-motion.jpg` (régénérée par `tools/og.py` puis `tools/ogshot.js`).
- Visuels publicitaires Facebook/Instagram : `tools/ads.py` + `tools/ads-render.js` — **ils affichent encore l'ancien prix (15 000 FCFA)**, à refaire au prix 5 500.

## 5. Décisions et préférences du propriétaire

- Réponses **courtes, en français**, résultat d'abord ; envoyer des aperçus (captures).
- Mise en page professionnelle, centrée, alignée ; pas de mot seul en fin de ligne ; tout doit rester lisible (clair et sombre).
- Le téléphone est la cible principale (la majorité des visiteurs viennent de Facebook).
- **Pas de faux achats / faux témoignages** (noms, photos ou drapeaux inventés) : refusé. Alternative proposée : notifications **réelles** alimentées par les paiements SasPay confirmés, avec l'accord de l'acheteur (case à cocher).

## 6. À faire / en attente

1. Notifications d'achats **réelles** (prénom + drapeau du vrai pays + « il y a X min ») — en attente d'un feu vert.
2. Espace membre sur le site (cours hébergés, connexion par e-mail, accès automatique après paiement) — le serveur d'hébergement reste à choisir ; développement local d'abord, mise en ligne après l'achat du serveur.
3. Refaire les visuels publicitaires au prix 5 500.
4. Envoyer chaque formulaire rempli vers un Google Sheet pour relancer ceux qui n'ont pas payé.
5. Prix par pays (ex. diaspora) : possible, le prix est fixé côté serveur.

## 7. Changer de compte (Claude, GitHub, Vercel)

1. **GitHub :** le code est dans le dépôt `RogerBOUJIEKA/VIBE-MOTION---MASTER-CLASS`. Avec un nouveau compte GitHub : *Settings → Transfer ownership* du dépôt, ou ajouter le nouveau compte comme collaborateur. Penser à passer le dépôt en **privé** (Settings → Danger Zone).
2. **Vercel :** dans le nouveau compte, *Add New → Project → Import* le dépôt (aucune commande de build, aucun réglage). Remettre les variables d'environnement du §2, puis déplacer le domaine `rogerboujieka.com` (le retirer de l'ancien projet, l'ajouter au nouveau ; le fichier `CNAME` est déjà là).
3. **Claude :** nouveau compte → connecter GitHub avec accès à ce dépôt → ouvrir une session sur le dépôt → « Lis source/README.md et continue ».
4. **Point de restauration :** le commit **`c56a192`** (état du site à la date de cette sauvegarde : paiement SasPay, promo 5 500 FCFA, haut de page téléphone). Pour y revenir : `git checkout c56a192` (ou, dans GitHub, *Commits* → ce numéro → *Browse files*).

## 8. Notes techniques

- `data/v2_build.py` et `tools/badges.py` contiennent d'anciens chemins : `build.py` ne lit `v2_build.py` que comme du texte (FAQ, profils), il n'est jamais exécuté. `badges.py` a servi à créer `pay/*.webp` à partir de logos tirés de dépôts GitHub publics (voir la liste en tête de fichier) ; les images finales sont déjà dans `pay/`.
- Les tests simulent l'API YouTube et bloquent les sites externes ; seule la vraie vidéo et le vrai SasPay ne sont pas testables hors ligne : **faire un achat test** après chaque changement du paiement.

## 9. Où se trouve chaque chose (inventaire complet)

**Dans ce dépôt GitHub**
- `index.html`, `api/`, `assets/`, `fonts/`, `pay/`, logos, `thumbs/` : le site publié.
- **Vidéos du site** (fichiers à la racine) : `spot-16x9.mp4`, `spot-9x16.mp4`, `motion-kwiva.mp4`, `motion-mboa.mp4`, `motion-snapia.mp4`, `motion-volta.mp4`, `work-bovann.mp4`, `work-camairco.mp4` (+ leurs images `.jpg`), et l'audio `presentation-formation.mp3`.
- `source/` : le code de fabrication, les tests et les outils (voir §1) ; `source/tunnel/` : le code d'origine du tunnel 3D (`assets/tunnel.js` et `assets/scene.js` en sont la version compilée avec esbuild + three.js 0.187).
- `archive/visuels-publicitaires/` : les 8 visuels Facebook/Instagram (4 formats × clair/sombre) et leur zip — **au prix 15 000 FCFA, à refaire à 5 500**.
- `archive/fonds-animes/` : les propositions de fonds animés (aurore, ondes, projecteur…) créées et essayées pour le haut de page.
- `archive/images-originales/` : photo d'origine de Roger (`roger-orig.webp`, `roger-clean.png`, `roger900.webp`).
- `archive/documentation-saspay/` : copie de la documentation SasPay (`full.txt`, `llms.txt`, `openapi.json`).

**Vidéos sur YouTube** (affichées dans « Réalisations ») — identifiants :
`IHRFvM2n8Ws` (Spectacle Cabrel Tindo), `4abyQA1a9h8` (Croisade Bafoussam pour Jésus), `IMaHC8wFzuM` (Pub motion design), `U2wMu5KrVnQ` (Camair-Co), `zbV6wVUsFxU` (Bus gratuits), `oVP2kVm4lMs` (Grande Nuit de Clôture), `Web3N01yUVA` (App Mr N).
Vidéo de présentation du haut de page : `Ew-ZgqctuxQ`.

**À conserver soi-même, hors du dépôt** (le dépôt est public, ces éléments doivent rester privés) :
- le **lien de la vidéo de la formation** (vidéo YouTube non répertoriée) ;
- le **lien d'invitation du groupe WhatsApp des élèves** ;
- les **clés** SasPay (et l'ancienne clé Maketou si elle existe encore) ;
- la vidéo originale de chaque cours, sur votre ordinateur ou votre Drive : YouTube n'est pas une sauvegarde.

**Volontairement non copié :** les logos de paiement d'origine tirés de dépôts GitHub tiers (leurs images finales sont dans `pay/`), les captures d'écran de travail et le profil de navigateur de test.
