# Facebook / Instagram ad visuals in the site's style: 4 formats x 2 themes, written as HTML pages to render.
import math, json
import os
OUT = os.path.dirname(os.path.abspath(__file__)) + '/ads-out/'
os.makedirs(OUT, exist_ok=True)
rays = ''.join(f'<line x1="{50+14*math.cos(a):.1f}" y1="{50+14*math.sin(a):.1f}" x2="{50+(46 if i%2==0 else 40)*math.cos(a):.1f}" y2="{50+(46 if i%2==0 else 40)*math.sin(a):.1f}"/>' for i, a in enumerate([k*math.pi/6+0.13 for k in range(12)]))
SPARK = f'<svg viewBox="0 0 100 100"><g stroke="currentColor" stroke-width="9" stroke-linecap="round">{rays}</g></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PAY = ['pay/momo.webp', 'pay/wave.webp', 'moov-money.svg', 'pay/tmoney.webp', 'orange-money.svg', 'pay/celtiis.webp', 'pay/airtel.webp', 'pay/freemoney.webp', 'mastercard.svg', 'visa.svg']
BG = {'moov-money.svg': '#ea6607', 'orange-money.svg': '#000', 'mastercard.svg': '#fff', 'visa.svg': '#fff'}
def pays(): return ''.join(f'<span class="pm" style="background:{BG.get(f, "transparent")}"><img src="{f}" style="width:{"100%" if f.startswith("pay/") else ("94%" if "orange" in f else "116%")}"></span>' for f in PAY)
STAMP = ('<div class="stamp"><svg class="t" viewBox="0 0 120 120"><defs><path id="p" d="M60,60 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs>'
         '<text dominant-baseline="central" fill="#fff" font-family="U" font-weight="500" font-size="9.6"><textPath href="#p" textLength="301" lengthAdjust="spacing">ACCÈS À VIE – ACCÈS À VIE – ACCÈS À VIE –&#160;</textPath></text></svg>'
         f'<span class="r"></span><span class="c">{SPARK}</span></div>')

BASE = '''
@font-face{font-family:U;src:url(fonts/urbanist.woff2) format("woff2");font-weight:100 900}
*{box-sizing:border-box;margin:0}
:root{--bg:#f6f4f1;--ink:#121214;--muted:#5e5b58;--red:#e3061b;--rink:#cf0418;--glow:rgba(227,6,27,.20);--pill:#fff;--pricebg:#121214;--pricefg:#fff;--soft:#fbe6e8}
.dark{--bg:#0b0b0e;--ink:#f3f2f0;--muted:#b3b0ab;--rink:#ff4558;--glow:rgba(227,6,27,.34);--pill:#18181e;--pricebg:#fff;--pricefg:#121214;--soft:rgba(227,6,27,.18)}
body{position:relative;overflow:hidden;background:var(--bg);color:var(--ink);font-family:U,sans-serif}
.glow{position:absolute;inset:0}
.giant{position:absolute;left:50%;transform:translateX(-50%);font-weight:300;line-height:1;letter-spacing:-.07em;white-space:nowrap;background:linear-gradient(180deg,#ff3347,#e3061b 55%,#9c0212);-webkit-background-clip:text;color:transparent}
.ph{position:absolute;max-width:none}
.chip{position:absolute;display:inline-flex;align-items:center;gap:.55em;padding:.5em .95em .5em .5em;border-radius:999px;background:#fff;color:#121214;font-weight:500;box-shadow:0 .7em 1.8em rgba(0,0,0,.18);white-space:nowrap}
.chip i{display:grid;place-items:center;width:2em;height:2em;border-radius:50%;background:#fdf0ea;color:#e07a56}
.chip i svg,.chip i img{width:1.2em;height:1.2em}
.stamp{position:absolute;display:grid;place-items:center;border-radius:50%;background:radial-gradient(circle at 32% 26%,#ff4d5e,#e3061b 55%,#a50314);box-shadow:0 12px 28px rgba(227,6,27,.38),0 0 0 7px rgba(227,6,27,.12)}
.stamp>*{grid-area:1/1}.stamp svg.t{width:100%;height:100%}
.stamp .r{width:58%;height:58%;border-radius:50%;border:1.5px dashed rgba(255,255,255,.6)}
.stamp .c{display:grid;place-items:center;width:40%;height:40%;border-radius:50%;background:#fff;color:#e07a56}.stamp .c svg{width:68%;height:68%}
.pill{display:inline-flex;align-items:center;gap:.7em;padding:.75em 1.15em;border-radius:999px;background:var(--pill);color:var(--ink);font-weight:500;letter-spacing:.15em;box-shadow:0 1px 2px rgba(18,18,20,.06),0 10px 28px rgba(18,18,20,.10)}
.pill i{width:.6em;height:.6em;border-radius:50%;background:var(--red)}
.logo{position:absolute}
h1{font-weight:300;line-height:.98;letter-spacing:-.055em}
h1 em{font-style:normal;color:var(--rink)}
.sub{font-weight:400;line-height:1.4;color:var(--muted)}.sub b{font-weight:500;color:var(--ink)}
.row{display:flex;align-items:center;gap:.6em}
.price{display:inline-flex;align-items:baseline;gap:.35em;padding:.42em .85em;border-radius:999px;background:var(--pricebg);color:var(--pricefg)}
.price b{font-weight:400;font-size:1.55em;letter-spacing:-.03em}.price small{font-weight:500;font-size:.8em;opacity:.7}
.price s{font-size:.9em;opacity:.55;text-decoration-color:#ff3347}
.off{padding:.45em .7em;border-radius:999px;background:var(--soft);color:var(--rink);font-weight:500}
.cta{display:inline-flex;align-items:center;gap:.8em;padding:.3em .3em .3em 1.2em;border-radius:999px;background:var(--red);color:#fff;font-weight:500;box-shadow:0 .8em 2em rgba(227,6,27,.35);white-space:nowrap}
.cta .a{display:grid;place-items:center;width:2.1em;height:2.1em;border-radius:50%;background:#fff;color:var(--red)}.cta .a svg{width:1em;height:1em}
.pays{display:flex}
.pm{display:grid;place-items:center;border-radius:50%;overflow:hidden;flex:none}
.pm img{max-width:none;height:auto}
.url{font-weight:500;color:var(--muted)}
'''

def tall(W, H, ph_top, giant_top, giant_size, fade_a, fade_b, txt_top, h1_size, stamp, chip1, chip2, bottom_y, top_y):
    """phone-like layout: portrait photo across the full width (its cut sides sit on the canvas edges), text below."""
    pad = 64
    css = f'''body{{width:{W}px;height:{H}px}}
.glow{{background:radial-gradient(60% {int(W*.5)}px at 50% {ph_top+int(W*.24)}px,var(--glow),transparent 72%)}}
.giant{{top:{giant_top}px;font-size:{giant_size}px}}
.ph{{left:0;top:{ph_top}px;width:{W}px;height:{W}px;-webkit-mask-image:linear-gradient(#000 0,#000 {fade_a}px,transparent {fade_b}px)}}
.logo{{left:{pad}px;top:{top_y}px;height:52px}}
.tp{{position:absolute;right:{pad}px;top:{top_y}px;font-size:21px}}
.stamp{{left:{stamp[0]}px;top:{stamp[1]}px;width:{stamp[2]}px;height:{stamp[2]}px}}
.c1{{left:{chip1[0]}px;top:{chip1[1]}px;font-size:{chip1[2]}px}}.c2{{left:{chip2[0]}px;top:{chip2[1]}px;font-size:{chip2[2]}px}}
.tx{{position:absolute;left:{pad}px;right:{pad}px;top:{txt_top}px}}
h1{{font-size:{h1_size}px}}
.sub{{margin-top:22px;font-size:{int(h1_size*.34)}px}}
.row{{margin-top:30px;font-size:{int(h1_size*.33)}px;justify-content:space-between}}
.ft{{position:absolute;left:{pad}px;right:{pad}px;top:{bottom_y}px;display:flex;align-items:center;justify-content:space-between}}
.pays{{gap:8px}}.pm{{width:40px;height:40px}}.url{{font-size:24px}}
'''
    body = f'''<div class="glow"></div><div class="giant">MOTION</div>
<img class="ph" src="roger-v3.webp">
<img class="logo" src="LOGO">
<span class="pill tp"><i></i>FORMATION EN LIGNE</span>
{STAMP}
<span class="chip c1"><i>{SPARK}</i>Claude Opus 5.5</span><span class="chip c2"><i><img src="izivoice-icon.png"></i>iziVoice</span>
<div class="tx"><h1>Créez des vidéos pro<br><em>avec l'IA.</em></h1>
<p class="sub"><b>Claude Opus 5.5</b> monte. <b>iziVoice</b> prête sa voix.<br>Vous dirigez, sur smartphone ou ordinateur.</p>
<div class="row"><span class="row" style="margin:0;gap:.5em"><span class="price"><b>15 000</b><small>FCFA</small><s>35 000</s></span><span class="off">−57 %</span></span><span class="cta">Je m'inscris<span class="a">{ARROW}</span></span></div></div>
<div class="ft"><div class="pays">{pays()}</div><span class="url">rogerboujieka.com</span></div>'''
    return css, body

FORMATS = {
    # name: (W, H, builder args)
    'portrait-4x5-1080x1350': (1080, 1350, dict(ph_top=150, giant_top=104, giant_size=272, fade_a=560, fade_b=720, txt_top=850, h1_size=88,
                                                  stamp=(842, 400, 132), chip1=(40, 610, 24), chip2=(812, 700, 24), bottom_y=1262, top_y=40)),
    'story-9x16-1080x1920': (1080, 1920, dict(ph_top=360, giant_top=316, giant_size=272, fade_a=600, fade_b=790, txt_top=1090, h1_size=100,
                                                stamp=(842, 610, 132), chip1=(40, 830, 26), chip2=(806, 920, 26), bottom_y=1590, top_y=236)),
    'carre-1x1-1080x1080': (1080, 1080, dict(ph_top=118, giant_top=62, giant_size=240, fade_a=430, fade_b=560, txt_top=640, h1_size=74,
                                               stamp=(850, 330, 116), chip1=(40, 470, 22), chip2=(818, 520, 22), bottom_y=1000, top_y=32)),
}

def landscape():
    W, H = 1200, 628
    css = f'''body{{width:{W}px;height:{H}px}}
.glow{{background:radial-gradient(34% 52% at 24% 58%,var(--glow),transparent 70%)}}
.giant{{left:18px;transform:none;top:-14px;font-size:236px}}
.ph{{left:0;bottom:0;width:612px;height:612px}}
.c1{{left:24px;top:390px;font-size:16px}}.c2{{left:418px;top:468px;font-size:16px}}
.stamp{{left:478px;top:236px;width:86px;height:86px}}
.tx{{position:absolute;left:628px;top:186px;width:560px}}
.pill{{font-size:14px}}
h1{{margin-top:16px;font-size:58px}}
.sub{{margin-top:12px;font-size:18px}}
.row{{margin-top:16px;font-size:17px}}
.strip{{position:absolute;left:0;right:0;bottom:0;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;background:#0b0b0e}}
.dark .strip{{background:#18181e}}
.strip .lg{{height:28px}}.pays{{gap:6px}}.pm{{width:28px;height:28px}}.strip .url{{font-size:17px;color:#fff}}
'''
    body = f'''<div class="glow"></div><div class="giant">MOTION</div>
<img class="ph" src="roger-v3.webp">
<span class="chip c1"><i>{SPARK}</i>Claude Opus 5.5</span><span class="chip c2"><i><img src="izivoice-icon.png"></i>iziVoice</span>
{STAMP}
<div class="tx"><span class="pill"><i></i>FORMATION VIBE MOTION</span>
<h1>Créez des<br><em>vidéos pro</em> avec l'IA.</h1>
<p class="sub"><b>Claude Opus 5.5</b> monte. <b>iziVoice</b> prête sa voix. Vous dirigez.</p>
<div class="row"><span class="price"><b>15 000</b><small>FCFA</small><s>35 000</s></span><span class="off">−57 %</span><span class="cta">Je m'inscris<span class="a">{ARROW}</span></span></div></div>
<div class="strip"><img class="lg" src="logo_rb.png"><div class="pays">{pays()}</div><span class="url">rogerboujieka.com</span></div>'''
    return W, H, css, body

jobs = []
for name, (W, H, args) in FORMATS.items():
    css, body = tall(W, H, **args)
    for theme in ['clair', 'sombre']:
        logo = 'logo_rb_dk.png' if theme == 'clair' else 'logo_rb.png'
        html = f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{css}</style></head><body class="{"dark" if theme == "sombre" else ""}">{body.replace("LOGO", logo)}</body></html>'
        fn = f'{name}-{theme}'
        open(OUT + fn + '.html', 'w', encoding='utf-8').write(html); jobs.append([fn, W, H])
W, H, css, body = landscape()
for theme in ['clair', 'sombre']:
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{css}</style></head><body class="{"dark" if theme == "sombre" else ""}">{body}</body></html>'
    fn = f'paysage-1200x628-{theme}'
    open(OUT + fn + '.html', 'w', encoding='utf-8').write(html); jobs.append([fn, W, H])
json.dump(jobs, open(OUT + 'jobs.json', 'w'))
print(len(jobs), 'pages')
